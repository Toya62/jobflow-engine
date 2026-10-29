"""
tests/test_auto_generation.py

Unit tests for automated ATS application generation pipeline (auto_generate_approved_applications).
"""

import os
import sqlite3
import pytest
from unittest.mock import patch, MagicMock

from src.generators.auto_generate import auto_generate_approved_applications


@pytest.fixture
def mock_db(tmp_path):
    db_file = tmp_path / "test_karriere.db"
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        title TEXT,
        url TEXT,
        location TEXT,
        description TEXT,
        scraped_at TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        status TEXT,
        score INTEGER,
        archetype TEXT,
        evaluated_at TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        cv_pdf_path TEXT,
        cover_pdf_path TEXT,
        status TEXT DEFAULT 'Prepared',
        applied_at TEXT,
        notes TEXT
    );
    """)

    # Job 1: 90% score, scraped today, no application
    cur.execute("INSERT INTO jobs VALUES (1, 'TechCorp', 'Senior Python Engineer', 'https://techcorp.com/job/1', 'Berlin', 'A full description with lots of details about python and backend', datetime('now'));")
    cur.execute("INSERT INTO evaluations VALUES (1, 1, 'APPROVED', 90, 'backend_platform', datetime('now'));")

    # Job 2: 75% score (below 85%), scraped today
    cur.execute("INSERT INTO jobs VALUES (2, 'LowCorp', 'Frontend Dev', 'https://lowcorp.com/job/2', 'Munich', 'A full description with lots of details about react', datetime('now'));")
    cur.execute("INSERT INTO evaluations VALUES (2, 2, 'APPROVED', 75, 'frontend', datetime('now'));")

    # Job 3: 88% score, already generated
    cur.execute("INSERT INTO jobs VALUES (3, 'OldCorp', 'DevOps Specialist', 'https://oldcorp.com/job/3', 'Hamburg', 'A full description with lots of details about kubernetes', datetime('now'));")
    cur.execute("INSERT INTO evaluations VALUES (3, 3, 'APPROVED', 88, 'devsecops', datetime('now'));")
    cur.execute("INSERT INTO applications VALUES (1, 3, 'applications/2026-10-29/oldcorp_devops_cv.pdf', 'applications/2026-10-29/oldcorp_devops_cover.pdf', 'Prepared', NULL, NULL);")

    conn.commit()
    conn.close()
    return str(db_file)


def test_auto_generate_approved_applications_flow(mock_db):
    with patch("src.generators.auto_generate.generate_application") as mock_gen, \
         patch("src.generators.auto_generate.register_application_in_crm") as mock_crm, \
         patch("src.generators.auto_generate.send_telegram_alert") as mock_tel, \
         patch("src.generators.auto_generate.git_sync_async"):
        
        mock_gen.return_value = {
            "success": True,
            "cv_path": "applications/2026-10-29/techcorp_senior-python-engineer_cv.pdf",
            "cover_path": "applications/2026-10-29/techcorp_senior-python-engineer_cover.pdf",
            "ats_keywords": ["Python", "FastAPI", "Docker"],
            "meta_path": "applications/2026-10-29/techcorp_senior-python-engineer.meta.json",
        }

        res = auto_generate_approved_applications(
            min_score=85,
            max_age_days=1,
            limit=10,
            notify_telegram=True,
            db_path=mock_db,
        )

        assert res["total_candidates"] == 1
        assert res["generated_count"] == 1
        assert res["remaining_count"] == 0
        assert res["failed_count"] == 0
        assert len(res["generated_jobs"]) == 1
        assert res["generated_jobs"][0]["company"] == "TechCorp"

        mock_gen.assert_called_once()
        mock_crm.assert_called_once()
        mock_tel.assert_called_once()

        # Check telegram message content
        alert_msg = mock_tel.call_args[0][0]
        assert "Generated Packages:* 1" in alert_msg
        assert "Remaining in Queue (85%+):* 0" in alert_msg
        assert "Senior Python Engineer" in alert_msg
