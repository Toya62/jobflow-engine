"""
scrapers/indeed.py  —  Indeed Germany scraper wrapper 

Public API:
    scrape_indeed(title, results_wanted, hours_old) -> pd.DataFrame | None

Uses jobspy under the hood. Returns a raw DataFrame (no filtering applied).
"""

import pandas as pd
# pyrefly: ignore [missing-import]
from jobspy import scrape_jobs

from src.config import INDEED_RESULTS_WANTED, get_indeed_hours_old


def scrape_indeed(
    title: str,
    results_wanted: int = INDEED_RESULTS_WANTED,
    hours_old: int | None = None,
    offset: int = 0,
) -> pd.DataFrame | None:
    """
    Scrape Indeed Germany for a single job title.
    Supports offset parameter for pagination.

    Returns a raw DataFrame from jobspy, or empty DataFrame on failure.
    Caller is responsible for concatenating results and running filters.
    """
    if hours_old is None:
        hours_old = get_indeed_hours_old()
    try:
        return scrape_jobs(
            site_name=["indeed"],
            search_term=title,
            location="Germany",
            results_wanted=results_wanted,
            hours_old=hours_old,
            offset=offset,
            job_type="fulltime",
            country_indeed="germany",
            indeed_fetch_description=True,
        )
    except Exception as exc:
        print(f"[WARNING] Indeed scrape for '{title}' (offset={offset}) failed: {exc}")
        return pd.DataFrame()
