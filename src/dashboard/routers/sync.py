"""Git synchronization endpoints for the dashboard."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.core.logger import get_logger
from src.dashboard.git_ops import git_root, safe_pull_rebase
from src.dashboard.state import CACHE

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["sync"])


@router.get("/pull")
@router.get("/sync")
def pull_and_sync():
    """Pull ``origin/main`` and ingest new jobs into SQLite."""
    root_dir = git_root()
    try:
        ok, detail = safe_pull_rebase(root_dir)
        if not ok:
            return JSONResponse(status_code=400, content={
                "success": False,
                "message": f"Sync failed: {detail}",
                "output": detail,
            })

        # Automatically ingest newly pulled jobs and evaluations into database.
        try:
            from src.db import sync_remote_git_db
            sync_remote_git_db()
        except Exception as sync_err:
            logger.warning(f"Database sync after git pull encountered warning: {sync_err}")

        CACHE["jobs"].clear()
        from src.db.database import is_postgres
        db_type = "PostgreSQL" if is_postgres() else "SQLite"
        return {
            "success": True,
            "message": f"Successfully synchronized with GitHub origin/main and updated {db_type} database!",
            "output": detail,
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get("/health")
def get_system_health():
    """System health check: reports DB connection, application counts, pending evaluations, and AI router status."""
    from src.db.database import get_db_connection, is_postgres
    from src.ai.router import get_router_status
    import json
    import os

    db_type = "PostgreSQL" if is_postgres() else "SQLite"
    status_payload = {
        "status": "healthy",
        "database": {
            "type": db_type,
            "connected": False,
            "jobs_count": 0,
            "applications_count": 0,
            "prepared_count": 0,
            "applied_count": 0,
            "interview_count": 0,
            "pending_evaluations": 0,
        },
        "ai_router": get_router_status(),
        "latest_run": None,
    }

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        status_payload["database"]["connected"] = True

        cur.execute("SELECT COUNT(*) FROM jobs;")
        status_payload["database"]["jobs_count"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM applications;")
        status_payload["database"]["applications_count"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'Prepared';")
        status_payload["database"]["prepared_count"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'Applied';")
        status_payload["database"]["applied_count"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM applications WHERE status LIKE '%Interview%';")
        status_payload["database"]["interview_count"] = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM jobs j
            WHERE NOT EXISTS (SELECT 1 FROM evaluations e WHERE e.job_id = j.id)
        """)
        status_payload["database"]["pending_evaluations"] = cur.fetchone()[0]
        conn.close()
    except Exception as dbe:
        status_payload["status"] = "degraded"
        status_payload["database"]["error"] = str(dbe)

    # Read latest run summary if available
    summary_path = "data/latest_run_summary.json"
    if os.path.exists(summary_path):
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                status_payload["latest_run"] = json.load(f)
        except Exception:
            pass

    return status_payload
