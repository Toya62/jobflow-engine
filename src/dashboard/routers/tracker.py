"""CRM tracker endpoints: applications CRUD and tracker views."""

import os
import re
import sqlite3
import time

import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.core.logger import get_logger
from src.db.database import get_db_connection, is_postgres
from src.dashboard.applications import autoresolve_cv_pdf
from src.dashboard.crm import (
    UNSET,
    clean_cell,
    load_tracker_df,
    upsert_tracker_row,
)
from src.dashboard.dismissals import add_to_dismissed
from src.dashboard.git_ops import git_sync_async
from src.dashboard.schemas import (
    ApplicationDeleteRequest,
    ApplicationPatchRequest,
    ApplicationUpsertRequest,
    MessageResponse,
    SuccessResponse,
)
from src.dashboard.state import CACHE, CACHE_TTL_SECONDS, clear_data_caches

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["tracker"])

DB_PATH = os.path.join('data', 'karriere.db')

_EMAIL_MAP_CACHE = None


def _get_email_map():
    global _EMAIL_MAP_CACHE
    if _EMAIL_MAP_CACHE is not None:
        return _EMAIL_MAP_CACHE
    try:
        from src.generators.email import _get_jobs_df, extract_email
        jobs_df = _get_jobs_df()
        m = {}
        if jobs_df is not None and not jobs_df.empty:
            for _, r in jobs_df.iterrows():
                em = extract_email(str(r.get('job_url', ''))) or extract_email(str(r.get('description', '')))
                if em:
                    u = str(r.get('job_url', '')).strip()
                    c = re.sub(r'[^a-z0-9]', '', str(r.get('company', '')).lower())
                    if u:
                        m[u] = em
                    if c:
                        m[c] = em
        _EMAIL_MAP_CACHE = m
    except Exception as e:
        logger.warning(f"Failed to build email map cache: {e}")
        _EMAIL_MAP_CACHE = {}
    return _EMAIL_MAP_CACHE


@router.get("/tracker")
@router.get("/crm-data")
def get_tracker():
    """Return CRM tracker rows, newest application first, with contact emails."""
    try:
        now = time.time()
        if CACHE["tracker"] is not None and (now - CACHE["tracker"]["time"]) < CACHE_TTL_SECONDS:
            return CACHE["tracker"]["data"]

        df = load_tracker_df()
        if not df.empty:
            df = df.astype(object).where(pd.notnull(df), None)
            records = df.to_dict(orient='records')
            email_map = _get_email_map()
            from src.generators.email import extract_email
            for idx, rec in enumerate(records):
                rec['_csv_index'] = idx
                job_u = str(rec.get('job_url') or '').strip()
                comp_c = re.sub(r'[^a-z0-9]', '', str(rec.get('company') or '').lower())
                if job_u and ('@' in job_u or job_u.lower().startswith('mailto:')):
                    rec['email_contact'] = extract_email(job_u)
                elif job_u and job_u in email_map:
                    rec['email_contact'] = email_map[job_u]
                elif comp_c and comp_c in email_map:
                    rec['email_contact'] = email_map[comp_c]
                elif 'innogpt' in comp_c:
                    rec['email_contact'] = 'hello@innogpt.de'
        else:
            records = []

        records.sort(key=lambda x: (x.get("date_applied", "") or "", x.get("_csv_index", 0)), reverse=True)
        CACHE["tracker"] = {"data": records, "time": time.time()}
        return records
    except Exception as e:
        logger.error(f"  [tracker] Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tracker/refresh", response_model=MessageResponse)
def refresh_tracker():
    """Clear the in-memory tracker/job caches."""
    try:
        clear_data_caches()
        logger.info("[refresh] Cleared in-memory cache")
        return {"success": True, "message": "Cache cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/applied-urls")
def applied_urls():
    """Return every job URL already present in the CRM tracker."""
    try:
        urls = []
        df = load_tracker_df()
        if not df.empty and 'job_url' in df.columns:
            urls = df['job_url'].dropna().tolist()
        return urls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/applications", response_model=SuccessResponse)
def create_or_update_application(body: ApplicationUpsertRequest):
    """Insert or update a CRM application row."""
    try:
        if not body.cv_pdf_path:
            resolved = autoresolve_cv_pdf(body.company, body.position)
            if resolved:
                body.cv_pdf_path = resolved

        notes_val = body.notes if "notes" in body.model_fields_set else UNSET
        upsert_tracker_row(
            company=body.company,
            position=body.position,
            job_url=body.job_url,
            cv_path=body.cv_pdf_path or UNSET,
            cover_path=body.cover_pdf_path or UNSET,
            notes=notes_val,
            date_applied=clean_cell(body.date_applied) or UNSET,
        )
        clear_data_caches()
        git_sync_async("feat: crm add/update application [auto]")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/applications")
@router.patch("/applications/notes")
def patch_application(body: ApplicationPatchRequest):
    """Update only the matched CRM row (notes and/or status)."""
    try:
        notes_val = body.notes if "notes" in body.model_fields_set else UNSET
        status_val = body.status if "status" in body.model_fields_set else UNSET

        updated = upsert_tracker_row(
            company=body.company or "",
            position=body.position or "",
            job_url=body.job_url or "",
            notes=notes_val,
            status=status_val,
            create=False,
        )
        if updated:
            clear_data_caches()
            git_sync_async("feat: crm update application status [auto]")
            return {"success": True}
        return JSONResponse(
            status_code=404,
            content={"error": "Application record not found.", "job_url": body.job_url, "company": body.company},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/applications")
def delete_application(payload: ApplicationDeleteRequest | None = None, keep_job: bool = False):
    """Delete an application's files and CRM rows.

    By default the job is also recorded as dismissed (legacy behaviour). With
    ``keep_job=true`` only the CRM row and its files are removed: the ``jobs``
    row is untouched and nothing is dismissed, so the job stays in Job Finder.
    """
    try:
        cv_pdf_path = getattr(payload, 'cv_pdf_path', None)
        company = getattr(payload, 'company', None)
        position = getattr(payload, 'position', None)
        job_url = getattr(payload, 'job_url', None)

        if cv_pdf_path and cv_pdf_path not in ("N/A", "", "null"):
            cv_pdf_clean = cv_pdf_path.replace("\\", "/").strip()
            if not (".." in cv_pdf_clean or not cv_pdf_clean.startswith("applications/")):
                related_files = [
                    cv_pdf_clean,
                    cv_pdf_clean.replace("_cv.pdf", "_cover.pdf"),
                    cv_pdf_clean.replace("_cv.pdf", ".meta.json"),
                    cv_pdf_clean.replace("_cv.pdf", "_cv.tex"),
                    cv_pdf_clean.replace("_cv.pdf", "_cover.tex"),
                ]
                for rel_file in related_files:
                    if os.path.exists(rel_file):
                        try:
                            os.remove(rel_file)
                        except Exception as del_err:
                            logger.error(f"Failed to delete {rel_file}: {del_err}")

        if is_postgres() or os.path.exists(DB_PATH):
            try:
                conn = get_db_connection(DB_PATH)
                cur = conn.cursor()
                if cv_pdf_path and str(cv_pdf_path).strip() not in ("N/A", "", "null"):
                    clean_cv = str(cv_pdf_path).replace("\\", "/").strip().lstrip('/')
                    cur.execute(
                        "DELETE FROM applications WHERE ltrim(replace(cv_pdf_path, '\\', '/'), '/') = ?",
                        (clean_cv,),
                    )
                if company and position:
                    cur.execute(
                        "DELETE FROM applications WHERE job_id IN "
                        "(SELECT id FROM jobs WHERE company = ? AND title = ?)",
                        (str(company).strip(), str(position).strip()),
                    )
                elif job_url and str(job_url).strip() not in ("N/A", "", "null"):
                    cur.execute(
                        "DELETE FROM applications WHERE job_id IN (SELECT id FROM jobs WHERE url = ?)",
                        (str(job_url).strip(),),
                    )
                conn.commit()
                conn.close()
            except Exception as dbe:
                logger.error(f"Failed deleting application from DB: {dbe}")

        if not keep_job:
            add_to_dismissed(job_url=job_url, company=company, position=position)
        clear_data_caches()
        git_sync_async("feat: crm delete application [auto]")
        return {"success": True}
    except Exception as e:
        logger.error(f"Delete application error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/funnel-stats")
def get_funnel_stats():
    """Return application funnel metrics, weekly breakdown, and top recommended jobs."""
    try:
        from collections import defaultdict
        from datetime import datetime
        df = load_tracker_df()
        stages = {
            "draft": 0,
            "applied": 0,
            "screening": 0,
            "interview": 0,
            "offer": 0,
            "rejected": 0,
            "total": 0,
        }
        if not df.empty:
            stages["total"] = len(df)
            for _, r in df.iterrows():
                st = str(r.get("status", "")).strip().lower()
                if st in ("prepared", "draft", "not applied"):
                    stages["draft"] += 1
                elif st in ("applied", "sent"):
                    stages["applied"] += 1
                elif st in ("screening", "assessment"):
                    stages["screening"] += 1
                elif st in ("interview", "technical interview"):
                    stages["interview"] += 1
                elif st in ("offer", "accepted"):
                    stages["offer"] += 1
                elif st in ("rejected", "declined", "user_dismissed", "ghosted"):
                    stages["rejected"] += 1
                else:
                    stages["draft"] += 1

        active_funnel = stages["applied"] + stages["screening"] + stages["interview"] + stages["offer"] + stages["rejected"]
        applied_to_interview = round(((stages["interview"] + stages["offer"]) / max(1, active_funnel)) * 100, 1)
        interview_to_offer = round((stages["offer"] / max(1, stages["interview"] + stages["offer"])) * 100, 1)

        weekly = defaultdict(lambda: {"applied": 0, "prepared": 0})
        if not df.empty:
            for _, r in df.iterrows():
                dt_str = str(r.get("date_applied") or r.get("applied_at") or "").strip()
                if dt_str and len(dt_str) >= 10:
                    try:
                        d = datetime.strptime(dt_str[:10], "%Y-%m-%d")
                        w_key = f"W{d.isocalendar()[1]} ({d.strftime('%b')})"
                        st = str(r.get("status", "")).strip().lower()
                        if st in ("applied", "sent", "interview", "offer"):
                            weekly[w_key]["applied"] += 1
                        else:
                            weekly[w_key]["prepared"] += 1
                    except Exception:
                        pass

        top_recommendations = []
        try:
            conn = get_db_connection(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT j.id, j.company, j.title, j.url, j.location, e.score, e.archetype, e.matched_skills, e.gaps, j.scraped_at
                FROM jobs j
                JOIN evaluations e ON j.id = e.job_id
                LEFT JOIN applications a ON j.id = a.job_id
                WHERE a.id IS NULL AND e.status = 'APPROVED' AND e.score >= 70
                ORDER BY e.score DESC, j.id DESC
                LIMIT 5
            """)
            rows = cur.fetchall()
            for row in rows:
                top_recommendations.append({
                    "id": row[0],
                    "company": row[1],
                    "title": row[2],
                    "url": row[3],
                    "location": row[4],
                    "score": row[5],
                    "archetype": row[6],
                    "matched_skills": row[7],
                    "gaps": row[8],
                    "scraped_at": row[9],
                })
            conn.close()
        except Exception as e_top:
            logger.warning(f"Failed fetching top recommendations: {e_top}")

        return {
            "stages": stages,
            "conversions": {
                "applied_to_interview": applied_to_interview,
                "interview_to_offer": interview_to_offer,
            },
            "weekly_activity": [{"week": k, **v} for k, v in list(weekly.items())[-6:]],
            "top_recommendations": top_recommendations,
        }
    except Exception as e:
        logger.error(f"Failed to calculate funnel stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
