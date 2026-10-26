#!/usr/bin/env python3
"""
scripts/generate_selected_jobs.py — Batch generator for user-selected jobs.
Generates ATS-tailored CV (2 pages) + Cover Letter (1 page) for each approved job.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Add repo root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generators.application import generate_application
from src.core.logger import get_logger

logger = get_logger("batch_generator")

JOBS = [
    {
        "company": "KB Marketing GmbH",
        "position": "Softwareentwickler (m/w/d) für KI & Automatisierung",
        "location": "Essen, NW, DE",
        "url": "https://de.indeed.com/viewjob?jk=9eb1ae99412e9b0a",
        "language": "de",
        "description": """
Du denkst analytisch, arbeitest dich gerne in komplexe Themen ein und hast Freude daran, technische Lösungen für echte wirtschaftliche Herausforderungen zu entwickeln?
Du möchtest KI nicht nur anwenden, sondern mit modernen Entwicklungswerkzeugen wie Claude Code eigene Systeme aufbauen, Geschäftsprozesse automatisieren und neue digitale Dienstleistungen mitentwickeln?
Dann suchen wir genau dich zur Weiterentwicklung unserer internen Systeme und KI-basierten Dienstleistungen bei uns in Essen!
Als eine der schnell wachsenden Unternehmensberatungen für technische Industrieunternehmen verbinden wir datengetriebenes Marketing, messbare Prozessoptimierung und moderne KI-Technologien.
Von unserem Standort in Essen betreuen wir rund 150 mittelständische Industrieunternehmen aus ganz Deutschland, darunter zahlreiche Hidden Champions.
Bereits heute arbeiten wir mit einem außergewöhnlich hohen Automatisierungsgrad und setzen dafür eigene KI-Systeme, Dateninfrastrukturen und intelligente Workflows ein. Diese entwickeln wir kontinuierlich weiter und nutzen unser technologisches Know-how zunehmend auch für neue digitale Dienstleistungen unserer Kunden.
* Analyse und Automatisierung von Geschäftsprozessen
Du arbeitest dich in unterschiedliche fachliche Themen ein, verstehst bestehende Abläufe, erkennst Automatisierungspotenziale und entwickelst technische Lösungen, die Prozesse vereinfachen und effizienter machen.
* Entwicklung eigener KI-gestützter Anwendungen
Du konzipierst und entwickelst mithilfe von Claude Code eigene Anwendungen, interne Tools und automatisierte Workflows. Dabei verstehst, überprüfst und verbesserst du den generierten Code, statt Ergebnisse ungeprüft zu übernehmen.
* Datenbanken und Knowledgebases
Du arbeitest mit PostgreSQL, strukturierten Datenmodellen, APIs und KI-gestützten Wissensdatenbanken. Du sorgst dafür, dass Informationen zuverlässig verarbeitet, miteinander verknüpft und für unsere Anwendungen nutzbar gemacht werden.
* Weiterentwicklung unserer internen Systeme
Du entwickelst beispielsweise unsere CRM-Systeme, Rechercheprozesse, KI-Assistenten und Automatisierungen weiter.
* Technische Konzeption und Qualitätssicherung
Du übersetzt fachliche Anforderungen in technische Konzepte, prüfst die Funktionsfähigkeit deiner Lösungen und entwickelst bestehende Systeme kontinuierlich weiter.
Dein Profil:
* Analytisches Denken und ausgeprägte Problemlösungskompetenz
* Technisches Grundverständnis in Programmierung, Datenbanken, SQL, APIs
* Interesse an KI-gestützter Softwareentwicklung (Claude Code, RAG-Systeme)
* Schnelle Auffassungsgabe und eigenständige Recherche
* Strukturierte und sorgfältige Arbeitsweise
* Ausbildung oder Studium der Informatik, Wirtschaftsinformatik, Data Science
Von Vorteil: Erste praktische Erfahrung mit Claude Code, PostgreSQL, SQL, Python, APIs, KI-Agenten, RAG-Systemen oder Knowledgebases.
"""
    },
    {
        "company": "Goodman Masson Deutschland",
        "position": "Site Reliability Engineer (m/w/d)",
        "location": "Bochum, North Rhine-Westphalia, Germany",
        "url": "https://www.linkedin.com/jobs/view/4482046873",
        "language": "de",
        "description": """
Für ein etabliertes Softwareunternehmen im Ruhrgebiet suchen wir einen Site Reliability Engineer (m/w/d), der die Stabilität, Verfügbarkeit und Skalierbarkeit einer modernen Softwareplattform aktiv mitgestaltet. In dieser Rolle bewegst Du Dich an der Schnittstelle zwischen Softwareentwicklung und IT-Betrieb und trägst maßgeblich dazu bei, Betriebsprozesse zu automatisieren, Systemlandschaften weiterzuentwickeln und eine hohe Servicequalität sicherzustellen.
Deine Aufgaben:
* Verantwortung für die Sicherstellung einer hohen Verfügbarkeit, Stabilität und Performance geschäftskritischer Anwendungen
* Entwicklung und Umsetzung von Monitoring-, Alerting- und Observability-Konzepten zur frühzeitigen Erkennung von Störungen
* Automatisierung von Deployments, Releases und wiederkehrenden Betriebsprozessen
* Weiterentwicklung moderner CI/CD-Strukturen und Unterstützung eines effizienten Software-Lifecycles
* Analyse bestehender Betriebsprozesse und Identifikation von Optimierungspotenzialen
* Enge Zusammenarbeit mit Entwicklungsteams, Infrastrukturverantwortlichen und weiteren Stakeholdern zur kontinuierlichen Verbesserung der Plattform
* Mitwirkung bei der Gestaltung cloudbasierter Betriebsmodelle sowie moderner Sicherheits- und Infrastrukturkonzepte
Anforderungen:
* Erfolgreich abgeschlossenes Studium im Bereich Informatik, Wirtschaftsinformatik, Mathematik oder eine vergleichbare Qualifikation
* Erfahrung im Betrieb und der Weiterentwicklung moderner Software- und Plattformlandschaften
* Kenntnisse im Bereich Monitoring, Observability und Performance-Analyse komplexer Systeme (Prometheus, Grafana, ELK/Splunk)
* Praxiserfahrung mit Container-Technologien (Docker) und Orchestrierungslösungen (Kubernetes)
* Erfahrung mit Infrastructure-as-Code-Ansätzen (Terraform) und Automatisierungswerkzeugen (CI/CD, Jenkins, GitLab CI)
* Solide Kenntnisse in mindestens einer modernen Programmiersprache (Python, Bash) sowie Verständnis für Softwareentwicklungsprozesse
* Sicherer Umgang mit Linux-basierten Systemen sowie grundlegendes Verständnis von Netzwerktechnologien (TCP/IP, Firewalls)
* Gute Deutsch- und Englischkenntnisse
"""
    },
    {
        "company": "ZEISS Group",
        "position": "Software Development Engineer in Test (SDET) (m/w/x)",
        "location": "Jena, Thuringia, Germany",
        "url": "https://www.linkedin.com/jobs/view/4482041863",
        "language": "de",
        "description": """
Durch den weltweiten und branchenübergreifenden Einsatz unserer Produkte und Lösungen sind wir, die Carl Zeiss Spectroscopy GmbH, die globale Marke und der erste Ansprechpartner für neue Herausforderungen auf dem Gebiet der Spektroskopie.
Gestalten Sie die Qualität anspruchsvoller Soft- und Hardwareprodukte von Anfang an mit. In dieser Rolle entwickeln Sie moderne Testautomatisierungslösungen entlang der gesamten technischen Kette – von Firmware-nahen Komponenten und vernetzten Geräten bis hin zu Cloud-basierten End-to-End-Workflows.
Ihre Aufgaben:
* Entwicklung und Weiterentwicklung automatisierter Testlösungen über den gesamten Produktlebenszyklus hinweg
* Konzeption und Implementierung von Tests für Embedded Software, Komponenten, Integration, Hardware-Software-Integration, Systeme und Cloud-Services
* Aufbau und Betrieb skalierbarer Testumgebungen für vernetzte Systeme und Geräte (Raspberry Pi, Embedded Linux, Testboxen)
* Entwicklung von Testframeworks, Tools, Simulationen, Mocks und Stubs für reproduzierbare Testergebnisse
* Integration automatisierter Tests in CI/CD-Pipelines sowie kontinuierliche Optimierung der Testarchitektur
* Beratung interdisziplinärer Entwicklungsteams zu Testbarkeit, Teststrategien und nachhaltiger Softwarequalität
Ihr Profil:
* Abgeschlossenes Studium oder Ausbildung in Informatik, Elektrotechnik, Technischer Informatik oder vergleichbare Qualifikation
* Mehrjährige Erfahrung in Softwareentwicklung und Testautomatisierung, idealerweise über verschiedene Testebenen hinweg
* Sehr gute Programmierkenntnisse in C++, Python, C# oder Java
* Praxis mit modernen Testautomatisierungsframeworks, CI/CD (Jenkins, GitLab CI), Git sowie Entwicklungsumgebungen unter Linux und Windows
* Analytische, strukturierte Arbeitsweise und Freude daran, komplexe technische Zusammenhänge systemübergreifend zu durchdringen
* Gute Deutsch- und Englischkenntnisse; Kenntnisse in Embedded Linux, Hardware-in-the-Loop, Cloud-Technologien oder Performance- und Security-Tests sind ein Plus
"""
    },
    {
        "company": "DIS AG",
        "position": "AI Engineer / KI-Spezialist für Produktintegration (m/w/d)",
        "location": "Mainz, Rhineland-Palatinate, Germany",
        "url": "https://www.linkedin.com/jobs/view/4471740001",
        "language": "de",
        "description": """
Für unseren Kunden in Mainz suchen wir in unbefristeter Festanstellung einen erfahrenen KI-Experte (m/w/d) mit fundierter Praxis darin, smarte KI-Agenten und Large Language Models (LLMs) direkt in bestehende Softwareprodukte einzubauen und voll funktionsfähig zu integrieren.
Ihre Aufgaben:
* KI-Produktintegration: Sie fokussieren sich voll und ganz darauf, intelligente KI-Agenten und LLMs in unsere bestehenden Produkte und Architekturen einzubauen (wie z. B. für KI-basierten Support, smarte Chatbots oder die automatisierte Zusammenfassung von Statistiken).
* Automatisierung & Use-Cases: Sie identifizieren, konzipieren und realisieren smarte Anwendungsfälle, um Produkte durch künstliche Intelligenz direkt aufzuwerten und repetitive Abläufe zu automatisieren.
* Schnittstellen & Architektur: Sie entwerfen die passenden Daten- und Schnittstellenarchitekturen (REST APIs, GraphQL), um KI-Modelle reibungslos an bestehende Backends anzubinden.
* Testing & Optimierung: Sie evaluieren die Performance und Antwortqualität der eingesetzten KI-Agenten, optimieren Prompts und RAG-Pipelines und feilen kontinuierlich an der Benutzererfahrung.
* Zusammenarbeit mit Dev-Teams: Sie arbeiten eng mit dem klassischen Entwicklungsteam zusammen, das die regulären Software- und Backend-Tätigkeiten übernimmt, und fungieren als treibende Kraft für unsere KI-Features.
Ihr Profil:
* Qualifikation: Ein erfolgreich abgeschlossenes IT-Studium (M.Sc./B.Sc. Informatik) oder vergleichbare technische Qualifikation.
* Kernkompetenz KI: Praktische Erfahrung in der Entwicklung von KI-Agenten, RAG-Systemen und der Automatisierung von Aufgaben mithilfe von LLMs (Gemini, OpenAI, Hybrid Retrieval).
* Technischer Hintergrund: Solide Programmierkenntnisse in Python, REST APIs, FastAPI/Flask sowie Verständnis von Datenstrukturen und Datenbanken (PostgreSQL/SQL), um KI nahtlos an Softwareprodukte anzubinden.
* Arbeitsweise: Analytische Denkweise, starke Hands-on-Mentalität und die Fähigkeit, eigenständig KI-Lösungen von der Idee bis in den Produktivbetrieb zu bringen.
"""
    },
    {
        "company": "European Tech Recruit",
        "position": "Graduate Software Engineer - STEM Graduate (MSc/PhD)",
        "location": "Munich, Bavaria, Germany",
        "url": "https://www.linkedin.com/jobs/view/4482062290",
        "language": "en",
        "description": """
Graduate Software Engineer / Tech Consultant (MSc / PhD)
Location: Munich, Germany
Role Type: Permanent, Full-time
A leading, partnership-based IT consultancy in Munich is looking for bright, academically minded STEM graduates to join their growing team. Working across a wide array of industries—including Automotive, AI, Telecoms, Fintech, and Security Technology—you will have the opportunity to solve complex technical challenges while developing software for both high-growth start-ups and large corporations.
If you have a strong mathematical or scientific background and are eager to master multiple programming languages and modern software architectures, this is the ideal environment to launch your career.
What You Will Do:
* Develop & Optimise: Analyse customer requirements and build large, complex software systems across Cloud, DevOps, AI, and Big Data.
* Problem Solve: Work alongside collaborative teams to design agile software solutions and automated testing environments.
* Continuously Learn: Adapt and apply various programming languages (such as Python, C/C++, Java, SQL, Rust, Go) based on project needs.
Requirements:
* Education: A first-class or high-upper degree (MSc or PhD) in a STEM discipline (Computer Science, Informatics, etc.) with exemplary academic marks (e.g. TU Ilmenau M.Sc. Computer Science).
* Technical Aptitude: Core IT knowledge with hands-on coding experience (Python, C/C++, Java, SQL, Linux, Git, Docker, CI/CD).
* Mindset: Strong analytical thinking, critical problem-solving skills, and a genuine passion for technical learning.
* Language: Good German language skills (B2) alongside fluent English (C1).
"""
    },
    {
        "company": "Nokia",
        "position": "Junior C++ Software Engineer",
        "location": "Nuremberg, Bavaria, Germany",
        "url": "https://www.linkedin.com/jobs/view/4478951605",
        "language": "en",
        "description": """
You will be an integral part of the software organization that develops the embedded software for large-scale optical telecommunication systems. To support the needs of our customers we operate complex ASICs and FPGAs, run software in an embedded computer network of multicore CPUs, provide board support packages and carrier-grade application code, and maintain a CI/CD pipeline.
We empower our engineers to be proactive problem-solvers: If you identify a bottleneck or a potential system improvement, you are encouraged to bring it forward and learn how to contribute to its resolution.
How You Will Contribute And What You Will Learn:
* Develop & Implement: Develop and maintain high-performance embedded applications for Intel and ARM architectures using Modern C++.
* Learn & Apply: Understand and apply STL, Boost, and asynchronous programming concepts to solve concurrency challenges under guidance.
* Quality Contribution: Assist in writing and executing unit, E2E, and stress tests to ensure robustness (GTest, Python).
* Collaborate & Learn: Participate in code reviews and contribute to team design discussions in a global environment.
Key Skills And Experience:
* Education & Experience: Bachelor's or Master's degree in Computer Science, Electrical Engineering, or a related discipline, and 0–2 years of relevant professional experience.
* C++ Expertise: Strong Modern C/C++ and object-oriented programming skills, with knowledge of inter-process communication, multi-threading, CMake, and data structures.
* Continuous Learning: Enthusiasm for Modern C++ standards (C++17) and keeping up with emerging industry developments.
* Development Tools: Working knowledge of Git, Python, Linux, and GTest.
* Domain Knowledge: Experience in embedded software development, testing and debugging across hardware-software interfaces (Raspberry Pi, Linux systems, CAN bus/SocketCAN).
* Teamwork & Communication: Effective English communication skills (C1) and good German (B2) or willingness to learn.
"""
    },
    {
        "company": "Occhio GmbH",
        "position": "Data Engineer (m/w/d)",
        "location": "Munich, Bavaria, Germany",
        "url": "https://www.linkedin.com/jobs/view/4479406367",
        "language": "de",
        "description": """
Occhio ist Marktführer im Bereich hochwertiger Designleuchten und eine der führenden Premium-Marken Deutschlands. Unsere Produkte stehen europaweit für ikonisches Design, herausragende Lichtqualität und maximalen Joy of Use.
Die Rolle:
Als Data Engineer bist Du für die Weiterentwicklung und den Betrieb unserer Dateninfrastruktur verantwortlich. Du gestaltest Datenbanken und Datenpipelines, optimierst ETL-Prozesse und stellst sicher, dass unsere Daten effizient und zuverlässig erfasst, gespeichert und verarbeitet werden.
Deine Aufgaben:
* Du entwickelst implementierst und wartest die Dateninfrastruktur.
* Du gestaltest und optimierst Datenbanken, ETL-Prozesse (Extract, Transform, Load) und Datenpipelines.
* Du sorgst gemeinsam mit Controlling und Business-Analysten für eine effiziente und zuverlässige Datenerfassung, -speicherung und -verarbeitung.
Du bringst mit:
* Du hast ein abgeschlossenes Studium der Informatik, Wirtschaftsinformatik, Mathematik oder eine vergleichbare Qualifikation (M.Sc./B.Sc. Informatik).
* Du hast 2–5 Jahre Berufserfahrung als Data Engineer oder in einer vergleichbaren Rolle (z. B. ETL/Stream Processing Forschung & Werkstudententätigkeiten).
* Du hast gute Kenntnisse in SQL sowie in relationalen und nicht-relationalen Datenbanken (PostgreSQL, MySQL).
* Du hast Erfahrung mit ETL-/ELT-Frameworks und Datenpipeline-Technologien (Nextflow, Kafka, Apache Flink, PyFlink, Python Pipelines). Grundkenntnisse in Cloud-Datenplattformen (AWS S3, Lambda, ECS).
* Du hast sehr gute Kenntnisse in Python.
* Du hast analytisches Denkvermögen und arbeitest strukturiert.
* Du hast gutes Deutsch (B2) und gutes Englisch (C1) in Wort und Schrift.
"""
    },
    {
        "company": "amber",
        "position": "DevOps Engineer (F/M/*)",
        "location": "Aachen, North Rhine-Westphalia, Germany",
        "url": "https://www.linkedin.com/jobs/view/4481570839",
        "language": "de",
        "description": """
Aus Europa, für Europa - wir entwickeln Europas Business-KI. Wir sind das größte KI-Start-up in Aachen.
KMUs profitieren davon, wenn internes Wissen sofort nutzbar wird und intelligente Agenten darauf reagieren können. Wir glauben an eine Zukunft, in der Business-KI auf einer gemeinsamen Kontextschicht arbeitet.
Wir suchen eine:n DevOps Engineer, der die Leidenschaft und das Know-how mitbringt, unsere systemübergreifende KI-Plattform auf die nächste Stufe zu heben.
Aufgaben:
* Du unterstützt dabei, unser Produkt und interne Setup-Prozesse zu automatisieren und manuelle Arbeit zu reduzieren.
* Gemeinsam mit dem Development-Team verbesserst du Deployments und hilfst, technische Probleme zu analysieren und zu beheben.
* Du wirkst daran mit, unsere Sicherheitsmaßnahmen für Kunden und externe Audits weiterzuentwickeln, umzusetzen und zu dokumentieren.
* Du unterstützt beim Betrieb und bei der Skalierung unserer Deployments für verschiedene Kunden – auch mit größeren Datenbanken, Containern und Cloud-nativen Tools.
* Bei Incidents hilfst du bei der Analyse der Ursache und bei der Wiederherstellung unserer Dienste.
* Du betreibst und verbesserst unser Monitoring und Alerting (Grafana, Prometheus, Kibana).
Qualifikation:
* Du hast praktische Erfahrung mit Linux-basierten Systemen (Debian/Ubuntu).
* Du hast Erfahrung damit, Workloads in Cloud-Umgebungen bereitzustellen und zu betreiben (AWS S3/ECS/Lambda).
* Du kennst Kubernetes, Container-Orchestrierung und weitere Cloud-native Technologien (Docker) aus der Praxis.
* Du verstehst die Abläufe in Entwicklung und Betrieb und hast mit CI/CD-Pipelines gearbeitet (GitLab CI, Jenkins).
* Du hast mit Infrastructure-as-Code-Tools wie Terraform gearbeitet oder möchtest deine Kenntnisse darin vertiefen.
* Du hast Erfahrung mit Monitoring- und Logging-Tools wie Grafana, Kibana, Splunk oder Prometheus.
* Du kommunizierst klar und verbindlich auf Deutsch und Englisch.
* Du verfügst über solide Programmierkenntnisse in Python oder Java.
"""
    },
    {
        "company": "Marvel Fusion GmbH",
        "position": "Research Software Engineer - Scientific Computing & GPU Infrastructure",
        "location": "München, BY, DE",
        "url": "https://de.indeed.com/viewjob?jk=e2215ef54c045f22",
        "language": "en",
        "description": """
Founded in 2019, Marvel Fusion is Europe’s leading fusion energy company, uniting 120 scientists, engineers, and entrepreneurs across our locations in Munich and Colorado.
Backed by over €385 million in public and private funding, we’re driven by a shared mission: to deliver clean, abundant energy to the world.
The impact you will make:
As part of our multidisciplinary research and engineering team, you will shape how we tackle computational challenges in fusion research. You will combine your software expertise with the team’s knowledge of physics and engineering to develop new approaches, make technical decisions and turn ideas into reliable scientific software. From advancing numerical performance to enabling shared GPU computing on NVIDIA servers or AWS, you will own meaningful technical challenges and contribute directly to our scientific progress.
Your responsibilities:
* Develop and maintain scientific Python software, turning research requirements into reusable, tested features and clear interfaces.
* Work with scientists to define acceptance criteria and verify numerical results against reference cases and agreed accuracy requirements.
* Use profiling to identify bottlenecks; compare algorithms, code translations and CPU/GPU implementations through reproducible benchmarks.
* Prepare and deploy scientific workloads on NVIDIA GPU servers or AWS using reproducible environments and automated execution workflows (Docker, Linux, Nextflow).
* Connect computational services to internal applications through stable APIs for job submission, status tracking and result retrieval.
* Improve testing, continuous integration, packaging and documentation (CI/CD, pytest, CMake).
What you bring:
* A degree in Computer Science, Physics, Applied Mathematics, Engineering or related field (M.Sc. Computer Science TU Ilmenau).
* Strong Python software engineering skills and a track record of independently delivering maintainable software within an existing codebase.
* Experience with scientific or numerical computing, data pipelines (Nextflow DSL2, ETL), and collaborating with domain experts.
* Hands-on experience deploying scientific Python or GPU workloads on remote Linux servers or cloud infrastructure (AWS, Docker).
* A structured approach to debugging, version control, automated testing and documentation.
* Excellent written and verbal communication skills in English (C1).
"""
    }
]

def check_pdf_pages(filepath: str) -> int:
    try:
        out = subprocess.check_output(["mdls", "-name", "kMDItemNumberOfPages", filepath]).decode()
        for line in out.splitlines():
            if "=" in line:
                return int(line.split("=")[-1].strip())
    except Exception:
        pass
    return -1

def main():
    print(f"\n{'='*70}")
    print(f"  Karriere Pipeline — Batch Application Generator (9 Jobs)")
    print(f"{'='*70}\n")
    
    total = len(JOBS)
    results = []

    for idx, job in enumerate(JOBS, start=1):
        company = job["company"]
        position = job["position"]
        print(f"\n[{idx}/{total}] 🚀 Processing: {company} — {position} ({job['language'].upper()})")
        
        start_t = time.time()
        try:
            res = generate_application(
                company=company,
                position=position,
                description=job["description"],
                job_url=job["url"],
                location=job["location"],
                language=job["language"],
                compile_pdf=True,
                clean_tex=True
            )
            elapsed = time.time() - start_t
            if res.get("success"):
                cv_p = res.get("cv_path", "")
                cl_p = res.get("cover_path", "")
                cv_pages = check_pdf_pages(cv_p)
                cl_pages = check_pdf_pages(cl_p)
                print(f"  ✓ Success ({elapsed:.1f}s)!")
                print(f"    - CV: {cv_p} (Pages: {cv_pages})")
                print(f"    - CL: {cl_p} (Pages: {cl_pages})")
                results.append((company, position, True, cv_pages, cl_pages, ""))
            else:
                err = res.get("error", "Unknown error")
                print(f"  ✗ Failed ({elapsed:.1f}s): {err}")
                results.append((company, position, False, 0, 0, err))
        except Exception as e:
            elapsed = time.time() - start_t
            print(f"  ✗ Exception ({elapsed:.1f}s): {e}")
            results.append((company, position, False, 0, 0, str(e)))
        
        # Polite delay between LLM calls to respect API rate limits
        if idx < total:
            time.sleep(2)

    print(f"\n{'='*70}")
    print(f"  Batch Generation Summary")
    print(f"{'='*70}")
    for comp, pos, ok, cv_pgs, cl_pgs, err in results:
        status_sym = "✅" if ok else "❌"
        pg_info = f"[CV: {cv_pgs}p | CL: {cl_pgs}p]" if ok else f"Error: {err}"
        print(f"{status_sym} {comp} | {pos} -> {pg_info}")

if __name__ == "__main__":
    main()
