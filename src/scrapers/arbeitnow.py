"""
src/scrapers/arbeitnow.py — Arbeitnow API Job Scraper for Germany

Pulls fresh tech, engineering, and remote jobs in Germany from Arbeitnow's public API:
  https://www.arbeitnow.com/api/job-board-api?page={n}

Features:
- Direct JSON REST API (no scraping blocks, fast execution)
- Germany & DACH regional filtering via _is_allowed_region
- HTML description cleanup via BeautifulSoup
- Unix timestamp conversion for accurate date_posted
- Pipeline core filters (seniority, CS relevance, noise, score)
"""

import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup
import pandas as pd

from src.core.logger import get_logger
from src.core.config import get_max_days, get_window_tag
from src.core.filters import apply_filters
from src.scrapers.personio import _is_allowed_region

logger = get_logger(__name__)
GERMAN_TZ = ZoneInfo("Europe/Berlin")


def fetch_arbeitnow_jobs(max_pages: int = 3) -> pd.DataFrame:
    """Fetch jobs from Arbeitnow public REST API across multiple pages."""
    all_jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    for page in range(1, max_pages + 1):
        url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
        logger.info(f"  Fetching Arbeitnow page {page}/{max_pages}...")
        try:
            resp = requests.get(url, headers=headers, timeout=12)
            if resp.status_code != 200:
                logger.warning(f"  Arbeitnow page {page} returned HTTP {resp.status_code}")
                break
            data = resp.json()
            items = data.get("data", [])
            if not items:
                logger.info(f"  No more jobs on Arbeitnow page {page}")
                break

            for item in items:
                loc = str(item.get("location", "") or "").strip()
                is_remote = bool(item.get("remote", False))

                # Regional gate: Germany, German cities, or Remote with German context
                is_german_loc = _is_allowed_region(loc)
                is_german_remote = is_remote and any(
                    g in loc.lower() for g in ("germany", "deutschland", "berlin", "munich", "münchen", "hamburg", "")
                )
                if not (is_german_loc or is_german_remote):
                    continue

                title = str(item.get("title", "") or "").strip()
                company = str(item.get("company_name", "") or "").strip()
                job_url = str(item.get("url", "") or "").strip()

                if not title or not company:
                    continue

                # Clean HTML description
                raw_desc = item.get("description", "") or ""
                soup = BeautifulSoup(raw_desc, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                clean_desc = soup.get_text(separator="\n").strip()
                clean_desc = re.sub(r"\n{3,}", "\n\n", clean_desc)

                ts = item.get("created_at", 0)
                try:
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(GERMAN_TZ)
                    date_posted = dt.strftime("%Y-%m-%d")
                except Exception:
                    date_posted = datetime.now(GERMAN_TZ).strftime("%Y-%m-%d")

                job_types = item.get("job_types", [])
                job_type_str = ", ".join(job_types) if isinstance(job_types, list) else str(job_types)

                all_jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc or ("Remote (Germany)" if is_remote else "Germany"),
                    "job_url": job_url,
                    "date_posted": date_posted,
                    "description": clean_desc,
                    "job_type": job_type_str,
                    "applicant_count": 0,
                    "scraped_at": datetime.now(GERMAN_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                })
        except Exception as e:
            logger.error(f"  Error fetching Arbeitnow page {page}: {e}")
            break

    logger.info(f"Total raw Arbeitnow jobs collected (Germany/DACH): {len(all_jobs)}")
    return pd.DataFrame(all_jobs) if all_jobs else pd.DataFrame()


def run_scrape_arbeitnow() -> None:
    """Orchestrator runner for Arbeitnow scraper."""
    from src.scrapers.orchestrator import finalise

    max_days = get_max_days()
    window_tag = get_window_tag()

    logger.info("\n" + "=" * 46)
    logger.info("  Arbeitnow Tech & Engineering Scraper")
    logger.info(f"  Window : last {max_days} day(s) ({window_tag})")
    logger.info("  Output : data/karriere.db (direct SQLite)")
    logger.info("=" * 46 + "\n")

    # Fetch top 3 pages (up to 900 jobs)
    df = fetch_arbeitnow_jobs(max_pages=3)
    if not df.empty:
        logger.info(f"\n  Raw Arbeitnow jobs before filtering: {len(df)}")
        df = apply_filters(df, max_days=max_days, is_linkedin=False)

    finalise(df, "Arbeitnow", is_linkedin=False)


if __name__ == "__main__":
    run_scrape_arbeitnow()
