"""Scraper control endpoints: status, logs, start, and stop."""

import os
import subprocess
import sys

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.core.logger import get_logger
from src.dashboard import state
from src.dashboard.git_ops import git_root, reap_zombies
from src.dashboard.schemas import MatcherRunRequest, ScraperRunRequest

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["scraper"])


def _scraper_log_path() -> str:
    log_path = os.path.join('data', 'scraper_run.log')
    if not os.path.exists(log_path):
        log_path = os.path.join(git_root(), 'data', 'scraper_run.log')
    return log_path


@router.get("/scraper-status")
@router.get("/scraper/status", include_in_schema=False)
def scraper_status():
    """Report whether the local scraper subprocess is still running."""
    is_running = False
    exit_code = None
    proc = state.SCRAPER_PROCESS
    if proc is not None:
        poll = proc.poll()
        if poll is None:
            is_running = True
        else:
            exit_code = poll
            # Process completed - clear job cache so fresh scraped data loads.
            state.CACHE["jobs"] = {}
            state.SCRAPER_PROCESS = None
    return {"running": is_running, "exit_code": exit_code}


@router.get("/scraper-logs")
@router.get("/scraper/logs", include_in_schema=False)
def scraper_logs():
    """Return the tail of the local scraper log, if present."""
    log_path = _scraper_log_path()
    if not os.path.exists(log_path):
        return {"success": True, "logs": "No scraper log file found yet.", "total_lines": 0}
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            last_lines = "".join(lines[-300:])
        return {"success": True, "logs": last_lines, "total_lines": len(lines)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger-github-scraper")
@router.post("/run-scraper")
def run_scraper(body: ScraperRunRequest):
    """Spawn the local scraper subprocess (rejecting a concurrent run)."""
    portal = (body.portal or "all").lower()
    days = str(body.days)

    try:
        if state.SCRAPER_PROCESS is not None and state.SCRAPER_PROCESS.poll() is None:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "A scraper process is already running locally. Please wait or stop it first.",
                },
            )

        root_dir = git_root()
        venv_python = os.path.abspath(os.path.join(root_dir, '.venv', 'bin', 'python'))
        python_bin = venv_python if os.path.exists(venv_python) else sys.executable
        cmd = [python_bin, 'main.py', 'scrape', '--portal', portal, '--days', days]

        reap_zombies()
        logger.info(f"Launching local scraper: {' '.join(cmd)}")
        log_path = os.path.join(root_dir, 'data', 'scraper_run.log')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        log_file = open(log_path, 'w', encoding='utf-8')  # overwrite — fresh log per run
        state.SCRAPER_PROCESS = subprocess.Popen(
            cmd,
            cwd=root_dir,
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        state.CACHE["jobs"] = {}
        return {
            "success": True,
            "mode": "local",
            "message": f"⚡ Local scraper started for {portal.upper()} ({days}d).",
            "log_path": log_path,
        }
    except Exception as e:
        logger.error(f"Failed to start local scraper: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop-scraper")
def stop_scraper():
    """Terminate the running scraper subprocess, if any."""
    proc = state.SCRAPER_PROCESS
    if proc and proc.poll() is None:
        try:
            proc.kill()
            state.SCRAPER_PROCESS = None
            state.SCRAPER_STATUS["running"] = False
            state.SCRAPER_STATUS["message"] = "Scraper stopped by user."
            state.SCRAPER_STATUS["error"] = "Terminated by user."
            return {"success": True, "message": "Scraper process terminated."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    state.SCRAPER_STATUS["running"] = False
    return {"success": True, "message": "No active scraper process running."}


@router.post("/run-matcher")
def run_matcher(body: MatcherRunRequest = None):
    """Spawn the local AI matcher subprocess (sharing the scraper log)."""
    max_age = str(body.max_age_days if body and body.max_age_days is not None else 2)
    portal = body.portal if body and body.portal else None

    try:
        if state.SCRAPER_PROCESS is not None and state.SCRAPER_PROCESS.poll() is None:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "A process (scraper or matcher) is already running. Please wait or stop it first.",
                },
            )

        root_dir = git_root()
        venv_python = os.path.abspath(os.path.join(root_dir, '.venv', 'bin', 'python'))
        python_bin = venv_python if os.path.exists(venv_python) else sys.executable
        cmd = [python_bin, 'main.py', 'match', '--max-age-days', max_age]
        if portal and portal.lower() != "all":
            cmd.extend(['--portal', portal.lower()])

        reap_zombies()
        logger.info(f"Launching AI matcher: {' '.join(cmd)}")
        log_path = os.path.join(root_dir, 'data', 'scraper_run.log')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        log_file = open(log_path, 'w', encoding='utf-8')
        state.SCRAPER_PROCESS = subprocess.Popen(
            cmd,
            cwd=root_dir,
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        state.CACHE["jobs"] = {}
        return {
            "success": True,
            "mode": "local",
            "message": f"⚡ AI Matcher started for last {max_age} days.",
            "log_path": log_path,
        }
    except Exception as e:
        logger.error(f"Failed to start AI matcher: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pending-matches")
def get_pending_matches(max_age_days: int = 2):
    """Return count of recent pending jobs that need AI evaluation."""
    from datetime import datetime, timedelta
    from src.core.utils import GERMAN_TZ
    from src.db.database import get_db_connection

    try:
        conn = get_db_connection()
        cutoff = (datetime.now(GERMAN_TZ) - timedelta(days=max_age_days)).strftime("%Y-%m-%d %H:%M:%S")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM jobs j
            LEFT JOIN evaluations e ON j.id = e.job_id
            WHERE e.id IS NULL AND length(j.description) > 30
            AND j.scraped_at IS NOT NULL AND j.scraped_at != '' AND j.scraped_at >= ?
            """,
            (cutoff,),
        )
        row = cursor.fetchone()
        pending = row[0] if row else 0
        conn.close()
        return {"pending_count": pending, "max_age_days": max_age_days}
    except Exception as e:
        logger.error(f"Failed to fetch pending matches count: {e}")
        return {"pending_count": 0, "max_age_days": max_age_days, "error": str(e)}
