import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os
import sys

SQLITE_PATH = os.getenv("SQLITE_PATH", "data/karriere.db")
PG_URL = os.getenv("DATABASE_URL", "postgresql://karriere_user:karriere_secure_pass_2026@localhost:5432/karriere_db")

def migrate():
    print(f"Connecting to SQLite: {SQLITE_PATH}")
    if not os.path.exists(SQLITE_PATH):
        print(f"Error: {SQLITE_PATH} not found.")
        sys.exit(1)

    s_conn = sqlite3.connect(SQLITE_PATH)
    s_cur = s_conn.cursor()

    print(f"Connecting to PostgreSQL: {PG_URL.split('@')[-1]}")
    p_conn = psycopg2.connect(PG_URL)
    p_cur = p_conn.cursor()

    # 1. Create Tables
    print("Creating tables in PostgreSQL...")
    p_cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL PRIMARY KEY,
        company TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT,
        location TEXT,
        description TEXT,
        scraped_at TEXT,
        CONSTRAINT unq_jobs_url_company_title UNIQUE (url, company, title)
    );
    CREATE INDEX IF NOT EXISTS idx_jobs_scraped_at ON jobs(scraped_at);
    CREATE INDEX IF NOT EXISTS idx_jobs_url ON jobs(url);

    CREATE TABLE IF NOT EXISTS evaluations (
        id SERIAL PRIMARY KEY,
        job_id INTEGER UNIQUE REFERENCES jobs(id) ON DELETE CASCADE,
        status TEXT,
        score INTEGER,
        chance TEXT,
        archetype TEXT,
        matched_skills TEXT,
        gaps TEXT,
        summary TEXT,
        evaluated_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_evaluations_job_status ON evaluations(job_id, status);
    CREATE INDEX IF NOT EXISTS idx_evaluations_status ON evaluations(status);

    CREATE TABLE IF NOT EXISTS applications (
        id SERIAL PRIMARY KEY,
        job_id INTEGER UNIQUE REFERENCES jobs(id) ON DELETE CASCADE,
        cv_pdf_path TEXT,
        cover_pdf_path TEXT,
        status TEXT DEFAULT 'Prepared',
        applied_at TEXT,
        notes TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_applications_job_status ON applications(job_id, status);
    """)
    p_conn.commit()

    # 2. Migrate Jobs
    print("Migrating 'jobs' table...")
    s_cur.execute("SELECT id, company, title, url, location, description, scraped_at FROM jobs ORDER BY id")
    jobs = s_cur.fetchall()
    if jobs:
        execute_values(p_cur, """
            INSERT INTO jobs (id, company, title, url, location, description, scraped_at)
            VALUES %s
            ON CONFLICT (id) DO NOTHING
        """, jobs, page_size=1000)
        p_conn.commit()
        p_cur.execute("SELECT setval('jobs_id_seq', COALESCE((SELECT MAX(id) FROM jobs), 1));")
        p_conn.commit()
    print(f"  -> Migrated {len(jobs)} jobs.")

    # 3. Migrate Evaluations
    print("Migrating 'evaluations' table...")
    s_cur.execute("""
        SELECT id, job_id, status, score, chance, archetype, matched_skills, gaps, summary, evaluated_at 
        FROM evaluations ORDER BY id
    """)
    evals = s_cur.fetchall()
    if evals:
        execute_values(p_cur, """
            INSERT INTO evaluations (id, job_id, status, score, chance, archetype, matched_skills, gaps, summary, evaluated_at)
            VALUES %s
            ON CONFLICT (id) DO NOTHING
        """, evals, page_size=1000)
        p_conn.commit()
        p_cur.execute("SELECT setval('evaluations_id_seq', COALESCE((SELECT MAX(id) FROM evaluations), 1));")
        p_conn.commit()
    print(f"  -> Migrated {len(evals)} evaluations.")

    # 4. Migrate Applications
    print("Migrating 'applications' table...")
    s_cur.execute("""
        SELECT id, job_id, cv_pdf_path, cover_pdf_path, status, applied_at, notes 
        FROM applications ORDER BY id
    """)
    apps = s_cur.fetchall()
    if apps:
        execute_values(p_cur, """
            INSERT INTO applications (id, job_id, cv_pdf_path, cover_pdf_path, status, applied_at, notes)
            VALUES %s
            ON CONFLICT (id) DO NOTHING
        """, apps, page_size=1000)
        p_conn.commit()
        p_cur.execute("SELECT setval('applications_id_seq', COALESCE((SELECT MAX(id) FROM applications), 1));")
        p_conn.commit()
    print(f"  -> Migrated {len(apps)} applications.")

    # Verification
    p_cur.execute("SELECT count(*) FROM jobs")
    pg_jobs = p_cur.fetchone()[0]
    p_cur.execute("SELECT count(*) FROM evaluations")
    pg_evals = p_cur.fetchone()[0]
    p_cur.execute("SELECT count(*) FROM applications")
    pg_apps = p_cur.fetchone()[0]

    print(f"\nMigration Complete!")
    print(f"PostgreSQL counts: {pg_jobs} jobs, {pg_evals} evaluations, {pg_apps} applications.")

    s_conn.close()
    p_conn.close()

if __name__ == "__main__":
    migrate()
