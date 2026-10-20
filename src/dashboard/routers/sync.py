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
