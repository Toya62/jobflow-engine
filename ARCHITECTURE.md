# Karriere Pipeline Architecture

## Purpose

The pipeline collects German job listings, scores them against the verified candidate profile, supports human review in a local dashboard, and tracks tailored application documents.

## Runtime Flow

```text
Local scrapers (main.py scrape)
                 |
                 v
     src/scraper.py orchestrator
       |       |        |       |
       v       v        v       v
   LinkedIn  Indeed    BA   Bund / XING / Personio
       \       |        |       /
        \      v        v      /
          filters.py and scoring
                    |
                    v
          SQLite Database (data/karriere.db)
                    |
          +---------+----------+
          |                    |
          v                    v
 local dashboard (SPA)     AI matcher / review (Gemini/Groq)
          |                    |
          +----------+---------+
                     v
          applications/YYYY-MM-DD/
          TeX, PDF, metadata, job_links.md
                     |
                     v
              Git repository
```

## Storage and Synchronization

- **PostgreSQL (`karriere-postgres` / `DATABASE_URL`)**: Primary relational database containing `jobs`, `evaluations`, and `applications` tables in production.
- `data/karriere.db`: Embedded SQLite database (WAL mode) fallback for offline and local test environments.
- `applications/`: Generated source documents, compiled PDFs, sidecar metadata, and per-date job links.
- `data/*.yaml`: Configuration files (`exclusion_rules.yaml`, `target_profiles.yaml`, `job_taxonomy.yaml`).
- Git is the durable synchronization mechanism between the developer workspace and automation runners.
- No cloud object store or cloud storage credentials are part of the runtime.

## Main Components

| Component | Responsibility |
|---|---|
| `main.py` | CLI entry points for scraping, matching, dashboard, Git pull, and compilation |
| `src/scraper.py` | Portal orchestration, normalization, filtering, scoring, and DB ingestion |
| `src/scrapers/` | LinkedIn, Indeed, Bundesagentur, service.bund.de/Interamt, XING, and Personio collection |
| `src/core/filters.py` | Repost/noise filtering, profile matching, date filtering, and score rules |
| `src/ai/matcher.py` and `src/ai/router.py` | AI-assisted job evaluation stored directly in relational `evaluations` |
| `src/dashboard/server.py` | FastAPI dashboard app (uvicorn entrypoint, routers, and CRM API) |
| `src/generators/application.py` | Tailored CV/cover-letter source and PDF generation |
| `src/generators/compiler.py` | Local TeX compilation, metadata updates, CRM synchronization, and optional Git push |
| `src/db/database.py` | Unified relational database layer (PostgreSQL primary via `DATABASE_URL`, SQLite fallback) |
| `scripts/migrate_sqlite_to_pg.py` | Bulk sync utility between SQLite (`karriere.db`) and PostgreSQL instance |

## Deployment & Hosting

The system runs in dual mode:
- **Local Development**: CLI workflows and local Vite/FastAPI development server via `main.py` (with SQLite fallback or local Postgres).
- **Cloud Production (Oracle Cloud ARM Ampere)**:
  - Containerized deployment (`karriere-dashboard`) via Docker Compose.
  - Primary PostgreSQL instance (`karriere-postgres`) on port 5432 on shared `web-proxy` container network.
  - Reverse-proxied through Caddy with automatic SSL (`https://karriere-pipeline.duckdns.org/`).

1. Select a job in the dashboard or provide job details to the application generator.
2. Generate the tailored TeX sources and `.meta.json` under `applications/YYYY-MM-DD/`.
3. Compile to PDFs with Tectonic or XeLaTeX. Successful PDFs remain beside their metadata in the repository.
4. Update SQLite database `data/karriere.db` and the date folder's `job_links.md`.
5. Local developer or GitHub Actions synchronizes resulting files.

The dashboard serves application files directly from the local `applications/` directory and queries `data/karriere.db` for CRM and job lists.

## GitHub Actions

- `.github/workflows/ci.yml` runs automated regression tests (`pytest`) across scrapers, filters, and SQLite databases on pushes and pull requests.
- `.github/workflows/docker.yml` builds and publishes the container image to GHCR (manual dispatch or on Dockerfile changes).

Workflow changes should keep generated data and PDFs in the repository workspace and should not add cloud storage credentials.

## Local Development

```bash
.venv/bin/python main.py dashboard
.venv/bin/python main.py scrape --portal all --days 1
.venv/bin/python main.py compile --no-push
.venv/bin/python -m pytest -q
```
