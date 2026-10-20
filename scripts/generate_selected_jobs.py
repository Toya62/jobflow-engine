import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.generators.application import generate_application

jobs = [
    {
        "company": "DLR - Deutsches Zentrum für Luft- und Raumfahrt",
        "position": "Informatiker*in (w/m/d) im Bereich GeoAI - Schwerpunkt multilinguales Geoparsing",
        "location": "Jena, TH, DE",
        "job_url": "https://de.indeed.com/viewjob?jk=4de7a23076db6335",
        "language": "de",
        "description": """
Institut für Datenwissenschaften in Jena (DMO-MIR).
DFG-Projekt GeoMMCorpus+Eval:
- Einarbeitung in den aktuellen Stand der Forschung im Bereich GeoAI, z.B. zu multilingualem Geoparsing, zur Erstellung und Annotation geographischer Textkorpora sowie zu LLM-gestützten Annotations- und Qualitätssicherungsverfahren.
- Konzeption wissenschaftlicher Methoden und Arbeitsabläufe zur Gewinnung, Aufbereitung, Auswahl und Annotation großer, heterogener und multilingualer Textdatenbestände.
- Entwicklung und Anwendung datenwissenschaftlicher Verfahren zur Gewinnung, Bereinigung, Filterung und strukturierten Aufbereitung großer multilingualer Textbestände aus unterschiedlichen Textgenres.
- Planung experimenteller Untersuchungen zur LLM-gestützten Annotation und zur iterativen Qualitätssicherung mit Human-in-the-Loop-Verfahren.
- Konzipierung und Anwendung von geeigneten Qualitätsmaßen zur Bewertung der Ergebnisse.
Anforderungen:
- Abgeschlossenes wissenschaftliches Hochschulstudium (Master / Diplom Uni) im Bereich Informatik, Data Science, Geoinformatik, Computerlinguistik.
- Fundierte Kenntnisse und praktische Erfahrungen in den Bereichen Natural Language Processing (NLP), Informationsextraktion und maschinelles Lernen.
- Erfahrungen im Umgang mit Large Language Models (LLMs), insbesondere in deren Anwendung und Anpassung (Prompting, Fine-Tuning).
- Programmiererfahrung in Python sowie Erfahrung mit Versionskontrolle (Git).
- Sehr gute Englischkenntnisse in Wort und Schrift.
Kennziffer: 6423, Ansprechpartnerin: Dr. Friederike Klan.
"""
    },
    {
        "company": "LivEye GmbH",
        "position": "Cloud Platform Engineer (m/w/d) - Infrastructure & Automation",
        "location": "Föhren bei Trier 54343",
        "job_url": "https://www.arbeitsagentur.de/jobsuche/jobdetail/13635-8f40008f_JB5275023-S",
        "language": "de",
        "description": """
LivEye baut sein Platform Team auf. Zur Verstärkung unseres Teams suchen wir einen Cloud & Network Infrastructure Engineer (m/w/d).
Fokus: AWS Cloud Networking, hybride Infrastrukturen und sichere Verbindung der Cloud Platform mit Kamera-, Sensor- und IoT-Systemen.
Aufgaben:
- Konzeption, Aufbau und Weiterentwicklung unserer Cloud- und Netzwerk-Infrastruktur in AWS.
- Aufbau und Betrieb sicherer Netzwerkarchitekturen mit Amazon VPC, Subnetzen, Routing, DNS, Security Groups und Load Balancing.
- Konzeption und Betrieb hybrider Verbindungen sowie Site-to-Site VPN, IPsec, AWS Client VPN.
- Network Security und Segmentierung mit Firewalls wie OPNsense sowie sicheren Kommunikations- und Zertifikatskonzepten.
- Weiterentwicklung der Connectivity mobiler Kamera- und IoT-Systeme zur Cloud (AWS IoT Connectivity).
- Migration der bestehenden IONOS-Cloud-Infrastruktur nach AWS.
- Automatisierung und Weiterentwicklung von AWS Cloud Infrastructure mit OpenTofu/Terraform.
- Analyse komplexer Cloud-, Netzwerk- und Connectivity-Probleme, Monitoring und Security.
Profil:
- Mehrjährige praktische Erfahrung mit Cloud-, Netzwerk- oder hybriden Infrastrukturen und sehr gutes Verständnis von TCP/IP, Subnetting, Routing, NAT und DNS.
- Praktische Erfahrung mit Cloud Networking (AWS VPC) sowie VPN-Technologien (IPsec, Site-to-Site VPN, WireGuard).
- Erfahrung mit Firewall- und Network-Security-Konzepten sowie gutes Verständnis Linux-basierter Infrastrukturen.
- Erfahrung mit Infrastructure as Code (OpenTofu/Terraform).
- Sehr gute Deutschkenntnisse (mindestens B2) und gute Englischkenntnisse.
- Führungszeugnis erforderlich.
"""
    },
    {
        "company": "Technische Universität Hamburg",
        "position": "Research Associate (m/f/d) at the Institute of Embedded Systems",
        "location": "Hamburg",
        "job_url": "https://www.xing.com/jobs/hamburg-research-associate-institute-embedded-systems-158634100",
        "language": "en",
        "description": """
Institute for Embedded Systems (TUHH). Remuneration EG 13 TV-L.
Computer Engineering group focused on advancing Electronic Design Automation (EDA) for embedded and cyber-physical systems. Projects in security analysis, testing of digital systems and AI-based modelling of cyber-physical systems. Research training group CAUSE.
Tasks:
- Conduct independent and collaborative research projects.
- Design and implement new software tools for system design, modeling, testing, verification, diagnosis, and debugging.
- Incorporate recent Generative AI (GenAI) into novel design automation methods.
- Present research results at conferences and publish articles in peer-reviewed academic journals.
- Engage in teaching activities and contribute to funding applications.
Requirements:
- Completed scientific university studies (master's degree) in Computer Science or tightly related field.
- Strong skills in software engineering and computer science theory.
- Interest in system and automation tool development with background in dependability.
- Proficiency in both German and English in bilingual teaching environment.
- Note regarding Section 34a Hamburg Security Clearance Act.
Contact: Prof. Görschwin Fey.
"""
    }
]

for idx, j in enumerate(jobs, start=1):
    print(f"\n[{idx}/3] Generating application for: {j['company']} — {j['position']}...")
    res = generate_application(
        company=j["company"],
        position=j["position"],
        description=j["description"],
        job_url=j["job_url"],
        location=j["location"],
        language=j["language"],
        compile_pdf=True,
        clean_tex=True
    )
    if res.get("success"):
        print(f"  ✓ SUCCESS: {res.get('cv_path')} and {res.get('cover_path')}")
    else:
        print(f"  ✗ FAILED: {res.get('error')}")
