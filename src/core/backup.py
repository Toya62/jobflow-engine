"""
src/core/backup.py — Automated Database & Applications Backup to S3 / Cloudflare R2.
Uploads:
  1. PostgreSQL dump (compressed .sql.gz) or SQLite snapshot
  2. Generated applications archive (.tar.gz of applications/ directory)
Works with Cloudflare R2, AWS S3, or Backblaze B2 via standard S3 API.
"""

import os
import sys
import gzip
import shutil
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

# Ensure repo root is on sys.path
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from src.core.logger import get_logger
from src.core.notifier import send_telegram_alert
from src.db.database import is_postgres, get_database_url

logger = get_logger(__name__)

# S3 / R2 Configuration from environment
R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY = os.environ.get("R2_ACCESS_KEY_ID", os.environ.get("AWS_ACCESS_KEY_ID", ""))
R2_SECRET_KEY = os.environ.get("R2_SECRET_ACCESS_KEY", os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
R2_BUCKET = os.environ.get("R2_BUCKET_NAME", "karriere-backups")
R2_ENDPOINT = os.environ.get(
    "R2_ENDPOINT_URL",
    f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com" if R2_ACCOUNT_ID else ""
)


def is_r2_configured() -> bool:
    """Check if S3 / Cloudflare R2 credentials are present."""
    return bool(R2_ACCESS_KEY and R2_SECRET_KEY and (R2_ENDPOINT or os.environ.get("AWS_REGION")))


def create_postgres_dump(output_path: str) -> bool:
    """Dump PostgreSQL database to compressed .sql.gz file."""
    try:
        # Try direct host pg_dump first (works when pg_dump is installed on host)
        pg_url = get_database_url()
        if pg_url and shutil.which("pg_dump"):
            # If pg_url uses docker hostname 'db', convert to localhost on host
            host_url = pg_url.replace("@db:5432", "@localhost:5432")
            cmd = ["pg_dump", "-d", host_url]
            with open(output_path, "wb") as f_out, gzip.open(f_out, "wb") as gz_out:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if p.returncode == 0 and stdout:
                    gz_out.write(stdout)
                    return True

        # Fallback to docker exec if docker CLI is available
        if shutil.which("docker"):
            cmd = ["docker", "exec", "karriere-postgres", "pg_dump", "-U", "karriere_user", "karriere_db"]
            with open(output_path, "wb") as f_out, gzip.open(f_out, "wb") as gz_out:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if p.returncode == 0 and stdout:
                    gz_out.write(stdout)
                    return True
                logger.warning(f"Docker pg_dump failed: {stderr.decode('utf-8', errors='ignore')}")

        logger.error("[Backup] Neither host pg_dump nor docker exec succeeded.")
        return False
    except Exception as e:
        logger.error(f"[Backup] Failed creating postgres dump: {e}")
        return False


def create_applications_archive(output_path: str, apps_dir: str = "applications") -> bool:
    """Create compressed tar.gz archive of applications folder."""
    try:
        apps_path = _root / apps_dir
        if not apps_path.exists():
            return False
        shutil.make_archive(output_path.replace(".tar.gz", ""), "gztar", str(apps_path))
        return True
    except Exception as e:
        logger.error(f"[Backup] Failed archiving applications: {e}")
        return False


def upload_to_r2(local_file: str, remote_key: str) -> bool:
    """Upload local file to Cloudflare R2 / S3 bucket using boto3."""
    if not is_r2_configured():
        logger.warning("[Backup] R2/S3 credentials not configured in environment. Skipping upload.")
        return False
    
    try:
        import boto3
        from botocore.config import Config

        session = boto3.session.Session()
        client = session.client(
            service_name="s3",
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            endpoint_url=R2_ENDPOINT if R2_ENDPOINT else None,
            config=Config(signature_version="s3v4"),
        )
        client.upload_file(local_file, R2_BUCKET, remote_key)
        logger.info(f"[Backup] Successfully uploaded {remote_key} to bucket {R2_BUCKET}")
        return True
    except ImportError:
        logger.error("[Backup] 'boto3' library not installed. Run: pip install boto3")
        return False
    except Exception as e:
        logger.error(f"[Backup] Upload failed: {e}")
        return False


def run_full_backup(send_alert: bool = True) -> dict:
    """Execute full backup workflow: database dump + applications archive -> cloud."""
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    results = {"database": False, "applications": False}
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_dump_file = os.path.join(tmpdir, f"postgres_{date_str}.sql.gz")
        apps_tar_file = os.path.join(tmpdir, f"applications_{date_str}.tar.gz")
        
        # 1. Database dump
        if is_postgres():
            logger.info("[Backup] Dumping PostgreSQL database...")
            if create_postgres_dump(db_dump_file):
                key = f"db/postgres_{date_str}.sql.gz"
                results["database"] = upload_to_r2(db_dump_file, key)
        else:
            # SQLite copy
            sqlite_db = _root / "data" / "karriere.db"
            if sqlite_db.exists():
                gz_sqlite = os.path.join(tmpdir, f"sqlite_{date_str}.db.gz")
                with open(sqlite_db, "rb") as f_in, gzip.open(gz_sqlite, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                key = f"db/sqlite_{date_str}.db.gz"
                results["database"] = upload_to_r2(gz_sqlite, key)
        
        # 2. Applications archive
        logger.info("[Backup] Archiving applications folder...")
        if create_applications_archive(apps_tar_file):
            key = f"applications/applications_{date_str}.tar.gz"
            results["applications"] = upload_to_r2(apps_tar_file, key)

    if send_alert and is_r2_configured():
        status_icon = "✓" if all(results.values()) else "⚠️"
        msg = (
            f"{status_icon} *Karriere Pipeline Cloud Backup*\n\n"
            f"📅 Timestamp: {date_str}\n"
            f"🗄️ Database Dump: {'Uploaded' if results['database'] else 'Failed/Skipped'}\n"
            f"📁 Applications Archive: {'Uploaded' if results['applications'] else 'Failed/Skipped'}\n"
            f"☁️ Destination: `{R2_BUCKET}`"
        )
        send_telegram_alert(msg)

    return results


if __name__ == "__main__":
    res = run_full_backup(send_alert=False)
    print("Backup result:", res)

