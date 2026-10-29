import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.filters import apply_filters, filter_noise

def test_filter_noise():
    df = pd.DataFrame([
        {"title": ".NET Software Engineer"},
        {"title": "Data Engineer"},
        {"title": "Fullstack React Developer"}
    ])
    res = filter_noise(df)
    assert len(res) == 1
    assert res.iloc[0]["title"] == "Data Engineer"

def test_apply_filters_unconditional_noise():
    df = pd.DataFrame([
        {
            "title": ".NET Software Engineer",
            "description": "We are looking for a C# .NET engineer with extensive knowledge in Windows desktop development and Microsoft enterprise architectures." * 2
        },
        {
            "title": "Data Engineer",
            "description": "We are seeking a proactive Data Engineer with solid experience in Python, Apache Flink, Apache Kafka, and building automated data pipelines in Linux environments." * 2
        }
    ])
    res = apply_filters(df, is_linkedin=True)
    assert len(res) == 1
    assert res.iloc[0]["title"] == "Data Engineer"

def test_user_rejection_rules():
    desc_sample = "Standard engineering job description with extensive requirements and team collaboration responsibilities across different departments." * 2
    test_jobs = pd.DataFrame([
        {"title": "Clinical CRA Monitor", "description": "GCP life sciences pharma " + desc_sample},
        {"title": "Maritime Simulation Engineer", "description": "OMNeT++ simulation " + desc_sample},
        {"title": "Data Security Architect", "description": desc_sample},
        {"title": "CSIRT Expert", "description": "CrowdStrike XDR SOAR memory forensics " + desc_sample},
        {"title": "Power Platform & AI Solutions Engineer", "description": "Power Platform D365 automation " + desc_sample},
        {"title": "Full Stack Developer", "description": "React Spring Boot .NET C# SAP ABAP " + desc_sample},
        {"title": "DevOps Engineer", "description": "C1 Deutsch fließend erforderlich " + desc_sample}
    ])
    res = apply_filters(test_jobs, is_linkedin=False)
    assert len(res) == 0


def test_compute_score_date_freshness():
    """Verify that invalid/missing dates return 0 rather than falsely scoring 25."""
    from datetime import datetime, timezone
    from src.scrapers.orchestrator import _compute_score

    assert _compute_score(None) == 0
    assert _compute_score("") == 0
    assert _compute_score("invalid-date-xyz") == 0
    assert _compute_score("NaN") == 0
    assert _compute_score("NaT") == 0

    # Real fresh date (< 24h)
    now_iso = datetime.now(timezone.utc).isoformat()
    assert _compute_score(now_iso) >= 40


def test_cross_portal_dedup_requisition_and_location():
    from src.db.file_io import dedup

    df = pd.DataFrame([
        {
            "company": "Bundesanstalt für Straßen- und Verkehrswesen",
            "title": "Wissenschaftliche Mitarbeiterin / Wissenschaftlicher Mitarbeiter (m/w/d) im Bereich Mobilitätserhebungen und Analyse von Alltagsmobilität",
            "location": "51427 Bergisch Gladbach",
            "job_url": "https://service.bund.de/123",
            "description": "Ausschreibung Referenzcode der Ausschreibung 20261895_0002"
        },
        {
            "company": "BAV Dienstsitz Aurich",
            "title": "wissenschaftliche/r Mitarbeiter/in (m/w/d) Mobilitätserhebungen und Analyse von Alltagsmobilität",
            "location": "Bergisch Gladbach 51427",
            "job_url": "https://arbeitsagentur.de/456",
            "description": "BAV Dienstsitz Aurich Referenzcode der Ausschreibung 20261895\\_9300**"
        }
    ])
    res = dedup(df)
    assert len(res) == 1
    assert "Bundesanstalt" in res.iloc[0]["company"] or "BAV" in res.iloc[0]["company"]


def test_core_target_titles_not_killed_by_incidental_keywords():
    from src.core.filters import filter_forbidden_tech

    df = pd.DataFrame([
        {"title": "Webentwickler Python", "description": "Tech stack Java, PHP, C#, Swift vorzugsweise Python und PostgreSQL"},
        {"title": "Junior Backend Developer (Python)", "description": "Backend API mit Python FastAPI. Bei Kenntnissen in React wirkst du aktiv mit."},
        {"title": "Python Backend Developer KI-Plattform", "description": "Bauen Python Microservices für bestehende React-Oberfläche"},
        {"title": "DevOps Engineer for Testing", "description": "Testing infrastructure for Defence, maritime, aerospace, automotive clients with Docker and Kubernetes"},
        {"title": "Cloud & Backend Engineer", "description": "Working with clinical data and AI to help healthcare clients in AWS and Python"},
        {"title": "Solution Engineer DevSecOps", "description": "Cloud security with Linux, Terraform, Kenntnisse im Bereich Entra ID und Active Directory"},
        {"title": "Junior Cloud Developer Kubernetes & Golang", "description": "Cloud developer with Kubernetes and Golang microservices"}
    ])

    res = filter_forbidden_tech(df)
    assert len(res) == 7, f"Expected all 7 on-profile roles to survive, got {len(res)}"



