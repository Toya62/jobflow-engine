#!/usr/bin/env python3
"""
scripts/generate_manual_batch.py — Handcraft tailored ATS application packages
for the accepted batch of 2026-10-27 without calling Gemini API.
"""

import os
import json
import subprocess
from datetime import datetime

TARGET_DATE = "2026-10-27"
APP_DIR = os.path.join("applications", TARGET_DATE)
os.makedirs(APP_DIR, exist_ok=True)

# Personal constants (from user_profile.yml)
NAME = "Toyanath Pandey"
STREET = "Kerckhoff Str. 146"
ZIP_CITY = "45144 Essen"
PHONE = "+49 159 063 77419"
EMAIL = "pandeytoya22@gmail.com"
LINKEDIN = "linkedin.com/in/pandeytoya"
GITHUB = "github.com/Toya62"

def write_file(filename: str, content: str):
    path = os.path.join(APP_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# ==============================================================================
# JOB 1: Stargazr — Software Engineer (English)
# ==============================================================================

STARGAZR_DESC = """Die Beschreibung: Software Engineer als Startup Full-Time Job
Stargazr is an AI-focused enterprise simulation startup that brings together developers and financial analysts with the mission of creating the future of finance. Founded in 2020, we are a remote global team with offices in LA, Hamburg and Seville. We work with industry leaders like Lufthansa (largest airline in Europe) and Beiersdorf (Nivea, Eucerin, Labello).
We are looking for a dedicated and experienced Software Engineer to be part of our team. Your primary responsibilities will involve developing the server-side logic of our SaaS solution, working with a Python backend stack including Flask, PostgreSQL and Pandas. You'll write efficient, reusable, and reliable code, while also supporting our front-end team when needed.
Requirements:
- Two or more years of CS experience working with Python in a similar position
- BSc or MSc in Computer Science or equivalent
- Solid experience with Python and its libraries
- Proficient in working with SQL systems, experience with PostgreSQL is a plus
- Ability to communicate fluently in English with the team
- Ability to work on an 8-hour shift overlapping 11AM - 3PM CEST
Bonus points:
- Strong analytical and mathematical skills
- Familiarity with using Python for moving and transforming data between different systems and formats
- Skills in *nix environments, especially Debian
Benefits: Access to GPT Plus + APIs since day one, access to Github Copilot after first 3 months.
Email: careers@stargazr.ai
"""

STARGAZR_CV = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=1.2cm,bottom=1.2cm,left=1.4cm,right=1.4cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\definecolor{accent}{RGB}{1,105,111}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\vspace{-4pt}\rule{\linewidth}{0.6pt}\vspace{2pt}]
\titlespacing{\section}{0pt}{5pt}{2pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.4em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt}

\begin{document}\pagestyle{empty}

\begin{center}
  {\LARGE\bfseries Toyanath Pandey}\\[3pt]
  Kerckhoff Str. 146, 45144 Essen \quad|\quad +49 159 063 77419 \quad|\quad \href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
  \href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya} \quad|\quad \href{https://github.com/Toya62}{github.com/Toya62} \quad|\quad Born 22.05.1997
\end{center}
\vspace{2pt}

\section{Professional Summary}
Software Engineer holding an M.Sc. in Computer \& Systems Engineering from TU Ilmenau with strong production-level Python backend engineering, automated data transformation, and relational database expertise (PostgreSQL, SQL). Hands-on experience developing modular REST APIs and automated ETL pipelines on Debian/Ubuntu Linux environments, integrating LLM APIs, and building reliable SaaS and data platforms. Eager to advance Stargazr's enterprise financial simulation engine.

\vspace{3pt}

\section{Work Experience}

\textbf{Hochschule Koblenz} \hfill \textit{10.2025 -- 09.2026}\\
\textit{Research Assistant -- Backend Systems \& Data Pipelines} \hfill Koblenz, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Python Backend \& Data Transformation}: Engineered scalable Python ETL pipelines for high-throughput biological data ingestion, validation, and multi-format transformation between heterogeneous data schemas.
  \item \textbf{REST \& GraphQL APIs}: Built robust integration interfaces consuming REST and GraphQL endpoints (HGNC, Ensembl V1/V2 pipelines) with structured schema validation.
  \item \textbf{Containerized Linux Architecture}: Managed reproducible deployment containers with Docker on Debian/Ubuntu servers; automated quality assurance workflows with GitLab CI.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{11.2023 -- 08.2024}\\
\textit{Working Student Software Development -- Assisted \& Automated Driving} \hfill Abstatt, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Backend Tooling in Python}: Developed Python internal software tools and automated diagnostic error log analysis (DTC interpreter) for automotive electronic control units.
  \item \textbf{API Integration \& Embedded Systems}: Integrated REST APIs for the MPCFlix video recording system on Raspberry Pi running Embedded Linux.
  \item \textbf{CI/CD \& Monitoring}: Automated continuous integration test workflows in Jenkins; performed system debugging and log analytics using Splunk.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{05.2023 -- 10.2023}\\
\textit{Intern Software Development -- Assisted \& Automated Driving} \hfill Abstatt, Germany\\[2pt]
\begin{itemize}
  \item \textbf{REST API Automation}: Automated batch data workflows interfacing directly with Atlassian Jira REST APIs for programmatic ticket and issue cloning.
  \item \textbf{UI \& Backend Tooling}: Developed responsive Python graphical interfaces for internal test APIs and backend automation tools.
\end{itemize}
\vspace{4pt}

\textbf{RE DEPOSIT Solutions GmbH (REMONDIS Group)} \hfill \textit{07.2022 -- 05.2023}\\
\textit{Working Student Software Developer} \hfill Lünen / Ilmenau, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Application Engineering}: Developed and refactored desktop applications in Python and C++/Qt under Linux (Debian/Ubuntu); implemented automated unit tests.
  \item \textbf{Agile Collaboration}: Collaborated in an agile cross-functional engineering team, maintaining code quality and continuous test coverage.
\end{itemize}
\vspace{4pt}

\textbf{CloudSewa Pvt. Ltd.} \hfill \textit{01.2021 -- 01.2022}\\
\textit{Security \& Infrastructure Analyst} \hfill Kathmandu, Nepal\\[2pt]
\begin{itemize}
  \item \textbf{Observability \& Monitoring}: Deployed centralized ELK (Elasticsearch, Logstash, Kibana) and Prometheus/Grafana monitoring pipelines for Linux server fleets.
  \item \textbf{Network Security}: Enforced secure networking configurations (firewalls, VPNs, DNS/DHCP) and conducted OWASP vulnerability assessments.
\end{itemize}

\newpage

\section{Selected Engineering Projects}

\textbf{Karriere Pipeline -- Autonomous Platform \& Backend Engine} \hfill \href{https://github.com/Toya62/karriere-pipeline}{github.com/Toya62/karriere-pipeline}\\
\textit{Python, FastAPI/Flask, PostgreSQL/SQLite (WAL), Pandas, LLM APIs (Gemini/OpenAI), Docker, Linux}\\[1pt]
Autonomous backend platform featuring multi-source data ingestion, schema validation, Pandas-based filtering pipelines, and deterministic evaluation engines. Integrates external AI APIs with structured outputs and automated document compilation.
\vspace{4pt}

\textbf{EnsOrthoPOST -- High-Throughput REST \& GraphQL Pipeline} \hfill \href{https://github.com/Toya62/EnsOrthoPOST}{github.com/Toya62/EnsOrthoPOST}\\
\textit{Python, REST APIs, GraphQL, Pandas, Nextflow DSL2, ETL Pipelines, FASTA/GTF}\\[1pt]
High-throughput data extraction and transformation pipeline querying HGNC and Ensembl REST/GraphQL endpoints to generate structured corpora for machine learning models with robust schema parsing.
\vspace{4pt}

\section{Education}

\textbf{M.Sc. Computer and Systems Engineering} \hfill \textit{10.2021 -- 02.2025}\\
\textit{Technische Universität Ilmenau} \hfill Ilmenau, Germany (Final Grade: 2.2)\\[2pt]
\textit{Master's Thesis}: ``Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks'' (PyFlink, Apache Flink, Kafka)\\
\textit{Key Coursework}: Software Architectures (\textbf{1.0}), Advanced Database Systems (\textbf{2.0}), Software Safety (\textbf{2.0})
\vspace{4pt}

\textbf{B.Tech Computer Science and Engineering} \hfill \textit{08.2017 -- 06.2021}\\
\textit{Lovely Professional University} \hfill India
\vspace{5pt}

\section{Technical Skills}

\begin{itemize}
  \item \textbf{Languages}: Python, SQL, Java, C/C++, Bash, TypeScript (basic)
  \item \textbf{Backend \& Frameworks}: Flask, FastAPI, REST APIs, GraphQL, Pandas, Microservices, Pydantic
  \item \textbf{Databases \& Storage}: PostgreSQL, MySQL, SQLite, Relational Data Modeling, SQL Optimization
  \item \textbf{DevOps \& Linux}: Linux (Debian, Ubuntu), Docker, Git, GitLab CI, Jenkins, Bash Scripting, Terraform
  \item \textbf{AI \& Tooling}: LLM API Integration (Gemini, OpenAI), Copilot, Prompt Engineering, Pytest, CMake
  \item \textbf{Observability}: Prometheus, Grafana, ELK Stack, Splunk
\end{itemize}
\vspace{4pt}

\section{Languages}

\textbf{English:} Fluent (C1) \quad|\quad \textbf{German:} B2 (aktiv in Entwicklung) \quad|\quad \textbf{Nepali / Hindi:} Native / Bilingual

\end{document}
"""

STARGAZR_CL = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{parskip}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}\pagestyle{empty}

\textbf{Toyanath Pandey}\\[2pt]
Kerckhoff Str. 146\\[2pt]
45144 Essen, Germany\\[2pt]
+49 159 063 77419\\[2pt]
\href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
\href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya}

\vspace{10pt}

\textbf{Stargazr}\\[2pt]
Engineering Recruitment Team\\[2pt]
Hamburg, Germany

\vspace{10pt}

\begin{flushright}
  Essen, 27 October 2026
\end{flushright}

\vspace{2pt}

\textbf{Application for the Position of Software Engineer (Python Backend)}

\vspace{6pt}

Dear Stargazr Team,

I am writing to express my strong enthusiasm for the Software Engineer position at Stargazr. Your mission of creating the future of enterprise finance through an AI-focused simulation engine—partnering with industry leaders like Lufthansa and Beiersdorf—strongly resonates with my technical passion. Holding a Master of Science in Computer \& Systems Engineering from TU Ilmenau and over two years of hands-on experience developing modular Python backend services, data transformation pipelines, and relational database systems, I am excited to help scale the server-side logic of your SaaS platform.

During my work as a Research Assistant at Hochschule Koblenz, I architected and maintained modular Python backend pipelines that ingests, validates, and transforms large-scale structured datasets across REST and GraphQL endpoints. Running containerized execution environments on Debian Linux servers, I ensured high code reliability through strict schema enforcement and automated testing in GitLab CI. Previously at Bosch Engineering GmbH, I developed internal Python tools for ECU diagnostic log interpretation and automated Jira REST API workflows, interfacing with distributed backend systems and test pipelines via Jenkins and Splunk.

My daily development stack centers heavily around Python, Flask/FastAPI, PostgreSQL, and Pandas. Building on my strong foundation in relational data modeling and data transformations, I readily navigate complex data pipelines between heterogeneous systems and formats. Furthermore, I have actively integrated AI APIs (OpenAI, Gemini) and coding assistants into my daily workflows, matching Stargazr's culture of leveraging GPT Plus and Copilot for high-velocity software engineering.

I thrive in collaborative, remote-first environments and am fully flexible to support Stargazr's core collaboration hours. I am ready to relocate anywhere in Germany if needed and look forward to discussing how my backend engineering experience can contribute to Stargazr's continued growth in an interview.

\vspace{12pt}

Kind regards,\\[8pt]
\textbf{Toyanath Pandey}

\end{document}
"""

STARGAZR_META = {
    "date": TARGET_DATE,
    "company": "Stargazr",
    "position": "Software Engineer",
    "location": "Hamburg",
    "apply_url": "https://www.xing.com/jobs/hamburg-startup-job-mitgruender-praktika-software-engineer-158812413",
    "role_type": "Backend Platform Engineer",
    "language": "en",
    "status": "ready_to_compile",
    "cv_file": "stargazr_software-engineer_cv.tex",
    "cover_file": "stargazr_software-engineer_cover.tex",
    "description_file": "stargazr_software-engineer_description.md",
    "notes": "Handcrafted ATS package for Stargazr (Python, Flask, PostgreSQL, Pandas, Debian). Direct email application to careers@stargazr.ai."
}

# ==============================================================================
# JOB 2: Universität Hamburg — Research Software Engineer (English)
# ==============================================================================

UNI_HAMBURG_DESC = """Research Associate as Research Software Engineer § 28 Subsection 3 HmbHG
Hub of Computing and Data Science (HCDS) at Universität Hamburg.
Start: 01.01.2027, fixed until 31.12.2028. WissZeitVG.
Duties:
- Consulting for scientists of all faculties about data science and digital solutions
- Requirements analysis with prospective users (researchers of all fields)
- Planning, implementation and maintenance of data science software
- Development of data-driven systems, from advanced data analytics to multimodal transformer models
- Creation of user-friendly interfaces tied to user needs
- DevOps tasks within application development
- Analysis and recommendation of state-of-the-art technologies for models and infrastructure
- Evaluation and quality assurance
Requirements:
- University degree in computer science, data science, information systems or related field with high share of data analytics / software development
- Interest in interdisciplinary research
- Knowledge of Elasticsearch, Jupyter Notebooks, Docker and PostgreSQL is advantageous
- Knowledge of DevOps, MLOps and Cloud Infrastructure is advantageous
- Remuneration: TV-L.
"""

UNI_HAMBURG_CV = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=1.2cm,bottom=1.2cm,left=1.4cm,right=1.4cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\definecolor{accent}{RGB}{1,105,111}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\vspace{-4pt}\rule{\linewidth}{0.6pt}\vspace{2pt}]
\titlespacing{\section}{0pt}{5pt}{2pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.4em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt}

\begin{document}\pagestyle{empty}

\begin{center}
  {\LARGE\bfseries Toyanath Pandey}\\[3pt]
  Kerckhoff Str. 146, 45144 Essen \quad|\quad +49 159 063 77419 \quad|\quad \href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
  \href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya} \quad|\quad \href{https://github.com/Toya62}{github.com/Toya62} \quad|\quad Born 22.05.1997
\end{center}
\vspace{2pt}

\section{Professional Summary}
Research Software Engineer with an M.Sc. in Computer \& Systems Engineering from TU Ilmenau and proven experience bridging academic research with production-grade scientific software. Proven expertise developing data-driven systems, automated ETL pipelines, multimodal deep learning corpora, and containerized research infrastructure (Docker, PostgreSQL, Elasticsearch, Nextflow DSL2). Passionate about supporting interdisciplinary researchers at the Hub of Computing and Data Science (HCDS).

\vspace{3pt}

\section{Work Experience}

\textbf{Hochschule Koblenz} \hfill \textit{10.2025 -- 09.2026}\\
\textit{Research Assistant -- Scientific Computing \& Data Pipelines} \hfill Koblenz, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Scientific Data Pipelines \& Machine Learning}: Developed reproducible Python ETL workflows extracting, transforming, and validating large genomic datasets for training deep learning gene models (Tiberius).
  \item \textbf{REST \& GraphQL Data Ingestion}: Implemented robust API clients querying Ensembl and HGNC REST/GraphQL endpoints; executed sequence alignment pipelines utilizing MashMap3.
  \item \textbf{Reproducible Research Infrastructure}: Containerized scientific software components with Docker; automated verification, testing, and continuous deployment in GitLab CI.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{11.2023 -- 08.2024}\\
\textit{Working Student Software Development -- Assisted \& Automated Driving} \hfill Abstatt, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Diagnostic Software Engineering}: Built internal Python and C++ software tools for diagnostic error code (DTC) interpretation across automotive control units.
  \item \textbf{Embedded Systems \& APIs}: Engineered REST interfaces for the MPCFlix video recording system on Raspberry Pi running Embedded Linux.
  \item \textbf{CI/CD \& Monitoring}: Automated continuous integration test suites using Jenkins; analyzed performance and diagnostic logs with Splunk.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{05.2023 -- 10.2023}\\
\textit{Intern Software Development -- Assisted \& Automated Driving} \hfill Abstatt, Germany\\[2pt]
\begin{itemize}
  \item \textbf{API Integration \& Automation}: Developed automated Python tooling interfacing with Jira REST APIs for programmatic issue management and data synchronization.
  \item \textbf{Internal Tool UI}: Implemented user-friendly Python graphical interfaces for test automation APIs.
\end{itemize}
\vspace{4pt}

\textbf{RE DEPOSIT Solutions GmbH (REMONDIS Group)} \hfill \textit{07.2022 -- 05.2023}\\
\textit{Working Student Software Developer} \hfill Lünen / Ilmenau, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Application Development}: Maintained and enhanced desktop and backend software using C++/Qt and Python on Debian/Ubuntu Linux systems.
  \item \textbf{Testing \& Quality Assurance}: Applied static code analysis, memory debugging (gdb), and unit tests to ensure high system reliability.
\end{itemize}
\vspace{4pt}

\textbf{CloudSewa Pvt. Ltd.} \hfill \textit{01.2021 -- 01.2022}\\
\textit{Security \& Infrastructure Analyst} \hfill Kathmandu, Nepal\\[2pt]
\begin{itemize}
  \item \textbf{Search \& Monitoring}: Maintained ELK Stack (Elasticsearch, Logstash, Kibana) and Prometheus/Grafana infrastructure for system log analytics and observability.
  \item \textbf{Infrastructure Hardening}: Managed secure Linux configurations, network firewalls, and vulnerability assessments according to OWASP guidelines.
\end{itemize}

\newpage

\section{Selected Research \& Engineering Projects}

\textbf{EnsOrthoPOST -- Scientific ETL Pipeline for Deep Learning} \hfill \href{https://github.com/Toya62/EnsOrthoPOST}{github.com/Toya62/EnsOrthoPOST}\\
\textit{Python, REST APIs, GraphQL, Nextflow DSL2, Docker, FASTA/GTF Data Modeling}\\[1pt]
Scientific data extraction and processing pipeline querying HGNC and Ensembl REST/GraphQL APIs to construct normalized training datasets for genomic deep learning models with reproducible Nextflow orchestration.
\vspace{4pt}

\textbf{Nakshatra -- Astronomical Computing Engine \& Hybrid RAG} \hfill \href{https://github.com/Toya62/nakshatra}{github.com/Toya62/nakshatra}\\
\textit{Python, Hybrid RAG (BM25 + Dense Embeddings), Reciprocal Rank Fusion, LLM Orchestration, Pytest}\\[1pt]
High-precision computational system integrating lexical search and dense vector embeddings via Reciprocal Rank Fusion (RRF), multi-provider LLM synthesis, and a comprehensive automated test suite.
\vspace{4pt}

\section{Education}

\textbf{M.Sc. Computer and Systems Engineering} \hfill \textit{10.2021 -- 02.2025}\\
\textit{Technische Universität Ilmenau} \hfill Ilmenau, Germany (Final Grade: 2.2)\\[2pt]
\textit{Master's Thesis}: ``Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks'' (Apache Flink, PyFlink)\\
\textit{Key Highlights}: Software Architectures (\textbf{1.0}), Advanced Database Systems (\textbf{2.0}), Software Safety (\textbf{2.0})
\vspace{4pt}

\textbf{B.Tech Computer Science and Engineering} \hfill \textit{08.2017 -- 06.2021}\\
\textit{Lovely Professional University} \hfill India
\vspace{5pt}

\section{Technical Skills}

\begin{itemize}
  \item \textbf{Languages}: Python, SQL, Java, C/C++, Bash, TypeScript (basic)
  \item \textbf{Data Science \& ML}: Transformers, Deep Learning Corpora, Jupyter Notebooks, Pandas, NumPy, Nextflow DSL2
  \item \textbf{Databases \& Search}: PostgreSQL, Elasticsearch, MySQL, SQLite, Relational Modeling
  \item \textbf{DevOps \& MLOps}: Docker, Kubernetes, Linux (Debian, Ubuntu), GitLab CI, Jenkins, Git, Terraform
  \item \textbf{APIs \& Web}: REST APIs, GraphQL, FastAPI, Flask, Pydantic, Microservices
  \item \textbf{Observability}: Prometheus, Grafana, ELK Stack (Kibana), Splunk
\end{itemize}
\vspace{4pt}

\section{Languages}

\textbf{English:} Fluent (C1) \quad|\quad \textbf{German:} B2 (aktiv in Entwicklung) \quad|\quad \textbf{Nepali / Hindi:} Native / Bilingual

\end{document}
"""

UNI_HAMBURG_CL = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{parskip}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}\pagestyle{empty}

\textbf{Toyanath Pandey}\\[2pt]
Kerckhoff Str. 146\\[2pt]
45144 Essen, Germany\\[2pt]
+49 159 063 77419\\[2pt]
\href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
\href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya}

\vspace{10pt}

\textbf{Universität Hamburg}\\[2pt]
Hub of Computing and Data Science (HCDS)\\[2pt]
Hamburg, Germany

\vspace{10pt}

\begin{flushright}
  Essen, 27 October 2026
\end{flushright}

\vspace{2pt}

\textbf{Application as Research Associate / Research Software Engineer (§ 28 Abs. 3 HmbHG)}

\vspace{6pt}

Dear Hiring Team of the Hub of Computing and Data Science,

I am writing to express my strong interest in the Research Software Engineer position at the Hub of Computing and Data Science (HCDS) at Universität Hamburg. The mission of HCDS to serve as the central driver of digital transformation in research—empowering scientists across all faculties through advanced data science software, data-driven systems, and multimodal transformer architectures—perfectly aligns with my academic background and engineering experience. Holding an M.Sc. in Computer \& Systems Engineering from TU Ilmenau and having worked as a Research Assistant developing scientific data and machine learning pipelines, I am eager to contribute to your interdisciplinary team.

In my recent research appointment at Hochschule Koblenz, I collaborated closely with researchers to build automated Python ETL pipelines, integrate complex REST and GraphQL APIs (Ensembl, HGNC), and construct structured FASTA/GTF training datasets for deep learning gene prediction models (Tiberius). Working in reproducible Linux environments, I containerized data science workflows using Docker and Nextflow DSL2, ensuring automated validation and continuous testing via GitLab CI. Prior to that, during my M.Sc. thesis research at TU Ilmenau, I investigated distributed stream processing mappings between PyFlink and execution frameworks, giving me a solid theoretical and practical foundation in high-performance computing and data systems.

My technical toolkit directly matches the requirements of HCDS: I have extensive hands-on experience with Python, Jupyter Notebooks, Docker, PostgreSQL, and Elasticsearch (gained through both scientific data curation and managing production ELK logging stacks at CloudSewa). I am comfortable consulting with domain experts from non-computing disciplines, translating diverse academic inquiries into scalable software architectures, and mentoring researchers in adopting modern MLOps and version-controlled development practices.

I am enthusiastic about joining the vibrant academic community of the University of Excellence Hamburg and am completely prepared to relocate to Hamburg. I look forward to discussing how my software engineering and research computing background can support HCDS in a personal interview.

\vspace{12pt}

Kind regards,\\[8pt]
\textbf{Toyanath Pandey}

\end{document}
"""

UNI_HAMBURG_META = {
    "date": TARGET_DATE,
    "company": "Universität Hamburg",
    "position": "Research Associate as Research Software Engineer",
    "location": "Hamburg",
    "apply_url": "https://www.xing.com/jobs/hamburg-research-associate-research-software-engineer-28-subsection-3-hmbhg-158813706",
    "role_type": "Research Software Engineer / Data Science",
    "language": "en",
    "status": "ready_to_compile",
    "cv_file": "universitat-hamburg_research-software-engineer_cv.tex",
    "cover_file": "universitat-hamburg_research-software-engineer_cover.tex",
    "description_file": "universitat-hamburg_research-software-engineer_description.md",
    "notes": "Handcrafted ATS package for Universität Hamburg Hub of Computing and Data Science (HCDS)."
}

# ==============================================================================
# JOB 3: KAYAK — Data Engineer (English)
# ==============================================================================

KAYAK_DESC = """Data Engineer at KAYAK (Berlin, BE, DE).
Part of Booking Holdings (NASDAQ: BKNG).
Role:
- Partner with Data Science teams to translate modeling needs into dataset requirements, collaborating with Data Engineering and Data Platform to extend foundational pipelines into ML-ready datasets.
- Design scalable and efficient dataset workflows and ensure pipeline reliability through validation, monitoring, and alerting; diagnose and resolve issues.
- Ship production-ready data solutions that enable ML applications and deliver real-world impact.
- Identify gaps and opportunities, contributing to technical decisions and roadmap priorities.
Requirements:
- Strong technical foundations in data engineering, software engineering, and systems design, backed by a track record of building and operating reliable, large-scale data pipelines.
- Hands-on experience developing production data pipelines.
- Bonus: Hands-on experience with Kafka, Flink, Iceberg, Trino, AWS, Kubernetes, Airflow, Python, SQL, and schema-based data contracts.
"""

KAYAK_CV = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=1.2cm,bottom=1.2cm,left=1.4cm,right=1.4cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\definecolor{accent}{RGB}{1,105,111}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\vspace{-4pt}\rule{\linewidth}{0.6pt}\vspace{2pt}]
\titlespacing{\section}{0pt}{5pt}{2pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.4em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt}

\begin{document}\pagestyle{empty}

\begin{center}
  {\LARGE\bfseries Toyanath Pandey}\\[3pt]
  Kerckhoff Str. 146, 45144 Essen \quad|\quad +49 159 063 77419 \quad|\quad \href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
  \href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya} \quad|\quad \href{https://github.com/Toya62}{github.com/Toya62} \quad|\quad Born 22.05.1997
\end{center}
\vspace{2pt}

\section{Professional Summary}
Data Engineer holding an M.Sc. in Computer \& Systems Engineering from TU Ilmenau with a dedicated specialization in distributed stream processing (Apache Flink, PyFlink, Apache Kafka) and large-scale data pipeline engineering. Proven experience designing automated ETL/ELT pipelines, integrating REST/GraphQL APIs, and creating production-ready ML datasets in containerized cloud and Linux environments. Committed to powering KAYAK's machine learning data foundation.

\vspace{3pt}

\section{Work Experience}

\textbf{Hochschule Koblenz} \hfill \textit{10.2025 -- 09.2026}\\
\textit{Research Assistant -- Data Pipelines \& ML Datasets} \hfill Koblenz, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Data Pipeline Engineering}: Architected robust Python ETL workflows for multi-source ingestion, validation, and schema transformation of large genomic datasets for deep learning models.
  \item \textbf{API Ingestion \& Sequence Alignment}: Built scalable clients consuming HGNC and Ensembl REST/GraphQL endpoints; orchestrated high-throughput alignment using MashMap3.
  \item \textbf{Reproducible Infrastructure}: Deployed pipeline components using Docker and Nextflow DSL2 on Linux servers, enforcing continuous data validation and test automation with GitLab CI.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{11.2023 -- 08.2024}\\
\textit{Working Student Software Development -- Assisted \& Automated Driving} \hfill Abstatt, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Data Analytics \& Tooling}: Developed automated Python log parsing and diagnostic error code (DTC) evaluation tools for electronic control units.
  \item \textbf{Monitoring \& CI/CD}: Implemented automated pipeline test workflows with Jenkins; performed log monitoring and real-time observability using Splunk.
  \item \textbf{IoT / Edge Ingestion}: Integrated REST APIs for camera test data on Raspberry Pi running Embedded Linux.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{05.2023 -- 10.2023}\\
\textit{Intern Software Development -- Assisted \& Automated Driving} \hfill Abstatt, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Automated API Ingestion}: Developed Python batch automation tools interfacing with Jira REST APIs for programmatic issue synchronization and metadata mapping.
  \item \textbf{UI Development}: Built Python user interfaces for internal diagnostic test APIs.
\end{itemize}
\vspace{4pt}

\textbf{RE DEPOSIT Solutions GmbH (REMONDIS Group)} \hfill \textit{07.2022 -- 05.2023}\\
\textit{Working Student Software Developer} \hfill Lünen / Ilmenau, Germany\\[2pt]
\begin{itemize}
  \item \textbf{Software Development}: Engineered and refactored desktop software in C++/Qt and Python on Debian/Ubuntu Linux platforms.
  \item \textbf{Data Access \& Testing}: Integrated relational databases and performed systematic unit and regression testing.
\end{itemize}
\vspace{4pt}

\textbf{CloudSewa Pvt. Ltd.} \hfill \textit{01.2021 -- 01.2022}\\
\textit{Security \& Infrastructure Analyst} \hfill Kathmandu, Nepal\\[2pt]
\begin{itemize}
  \item \textbf{Log Ingestion \& Observability}: Managed high-volume log pipelines with the ELK Stack (Elasticsearch, Logstash, Kibana) and Prometheus/Grafana.
  \item \textbf{Infrastructure Security}: Maintained network security configurations (firewalls, VPNs) and performed vulnerability assessments (OWASP).
\end{itemize}

\newpage

\section{Selected Engineering Projects}

\textbf{PyFlink Weather Stream Processing Pipeline} \hfill \href{https://github.com/Toya62/pyflink-weather-stream-pipeline}{github.com/Toya62/pyflink-weather-stream-pipeline}\\
\textit{Apache Flink, PyFlink, Apache Kafka, Python, Docker, Streaming ETL}\\[1pt]
End-to-end distributed stream processing pipeline ingesting high-velocity sensor streams via Kafka, executing stateful tumbling window aggregations, anomaly detection, and sinking to relational storage.
\vspace{4pt}

\textbf{Secure Cloud Data Orchestrator} \hfill \href{https://github.com/Toya62/secure-data-orchestrator-aws}{github.com/Toya62/secure-data-orchestrator-aws}\\
\textit{AWS (Lambda, S3, ECS Fargate), Terraform, Python, Docker, CloudWatch}\\[1pt]
Event-driven cloud data processing pipeline built with Infrastructure as Code (Terraform), orchestrating automated data ingestion into S3, least-privilege IAM security, and serverless compute processing.
\vspace{4pt}

\section{Education}

\textbf{M.Sc. Computer and Systems Engineering} \hfill \textit{10.2021 -- 02.2025}\\
\textit{Technische Universität Ilmenau} \hfill Ilmenau, Germany (Final Grade: 2.2)\\[2pt]
\textit{Master's Thesis}: ``Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks'' (\textbf{Specialized research on PyFlink, Apache Flink, and Kafka})\\
\textit{Key Coursework}: Advanced Database Systems (\textbf{2.0}), Software Architectures (\textbf{1.0}), PyFlink Stream Processing Research (\textbf{2.0}, 15 ECTS)
\vspace{4pt}

\textbf{B.Tech Computer Science and Engineering} \hfill \textit{08.2017 -- 06.2021}\\
\textit{Lovely Professional University} \hfill India
\vspace{5pt}

\section{Technical Skills}

\begin{itemize}
  \item \textbf{Streaming \& ETL}: Apache Flink, PyFlink, Apache Kafka, Stream Processing, Nextflow DSL2, Data Pipelines
  \item \textbf{Languages \& Databases}: Python, SQL, PostgreSQL, MySQL, SQLite, Java, C/C++, Bash
  \item \textbf{Cloud \& DevOps}: AWS (S3, Lambda, ECS, CloudWatch), Docker, Kubernetes, Linux (Debian, Ubuntu), GitLab CI, Jenkins, Git, Terraform
  \item \textbf{Observability \& Reliability}: Splunk, Prometheus, Grafana, ELK Stack (Elasticsearch, Kibana), Data Quality Validation
  \item \textbf{APIs \& Web}: REST APIs, GraphQL, FastAPI, Flask, Pydantic
\end{itemize}
\vspace{4pt}

\section{Languages}

\textbf{English:} Fluent (C1) \quad|\quad \textbf{German:} B2 (aktiv in Entwicklung) \quad|\quad \textbf{Nepali / Hindi:} Native / Bilingual

\end{document}
"""

KAYAK_CL = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{parskip}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}\pagestyle{empty}

\textbf{Toyanath Pandey}\\[2pt]
Kerckhoff Str. 146\\[2pt]
45144 Essen, Germany\\[2pt]
+49 159 063 77419\\[2pt]
\href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
\href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya}

\vspace{10pt}

\textbf{KAYAK}\\[2pt]
Data Engineering Recruitment Team\\[2pt]
Berlin, Germany

\vspace{10pt}

\begin{flushright}
  Essen, 27 October 2026
\end{flushright}

\vspace{2pt}

\textbf{Application for the Position of Data Engineer (ML Data Foundation)}

\vspace{6pt}

Dear KAYAK Team,

I am writing to express my strong enthusiasm for the Data Engineer position at KAYAK in Berlin. Powering the trusted data foundation behind machine learning models across billions of travel search queries at KAYAK and Booking Holdings is an inspiring challenge that directly aligns with my expertise in distributed data pipelines, stream processing, and systems design. Holding an M.Sc. in Computer \& Systems Engineering from TU Ilmenau—where my master's thesis focused explicitly on stream processing pipelines with Apache Flink, PyFlink, and Kafka—I am eager to contribute to your data engineering organization.

Throughout my academic research and engineering roles, I have specialized in building dependable, scalable data pipelines. In my master's thesis, titled \textit{``Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks''}, I analyzed stateful transformations, windowing mechanics, and fault tolerance across distributed stream frameworks. During my appointment as a Research Assistant at Hochschule Koblenz, I engineered end-to-end Python ETL pipelines transforming complex data corpora for training deep learning models, enforcing strict data validation, schema consistency, and automated CI/CD testing within Docker and GitLab CI environments.

Previously at Bosch Engineering GmbH, I developed automated Python data tools and log parsing pipelines for vehicle diagnostics, collaborating with engineering teams and maintaining continuous pipeline observability with Splunk and Jenkins. At CloudSewa, I managed large-scale log ingestion clusters using the ELK Stack and Prometheus, ensuring high data reliability, zero silent failures, and real-time anomaly alerting.

KAYAK's tech stack—centered around Kafka, Flink, AWS, Python, SQL, and robust data validation—directly reflects my technical strengths. Building on my foundational mastery in Flink and Kafka, I rapidly integrate adjacent platforms such as Iceberg, Trino, and Airflow, translating data science modeling requirements into high-throughput, ML-ready datasets with clear contracts.

I am fully prepared to work from your Friedrichshain office in Berlin 3 days per week and relocate immediately. Thank you for your consideration, and I look forward to discussing my technical background in an interview.

\vspace{12pt}

Kind regards,\\[8pt]
\textbf{Toyanath Pandey}

\end{document}
"""

KAYAK_META = {
    "date": TARGET_DATE,
    "company": "KAYAK",
    "position": "Data Engineer",
    "location": "Berlin",
    "apply_url": "https://de.indeed.com/viewjob?jk=f815d95705aa2076",
    "role_type": "Data Engineer / Stream Processing",
    "language": "en",
    "status": "ready_to_compile",
    "cv_file": "kayak_data-engineer_cv.tex",
    "cover_file": "kayak_data-engineer_cover.tex",
    "description_file": "kayak_data-engineer_description.md",
    "notes": "Handcrafted ATS package for KAYAK (Flink, Kafka, Python, SQL, ML Datasets, AWS). Direct thesis match."
}

# ==============================================================================
# JOB 4: T&S — DevOps Engineer Testing (German)
# ==============================================================================

TS_DESC = """DevOps Engineer Testing (m/w/d) bei T&S (Technology & Strategy) in Kiel.
Aufgaben:
- Mitarbeit in einem agilen Entwicklungsteam für Systemprodukte im Bereich Marinekommunikation
- Betreuung der entwicklungseigenen HIL-Testsysteme
- Aktive Unterstützung bei der Einbindung der HIL-Testsysteme in die Testautomatisierungsstrategie und Testprozesse
- Administration und Ausbau virtualisierter Testumgebungen gemäß Testsystemstrategie
- Mitwirkung bei der Automatisierung von Testsystemen und Testabläufen
- Einsatz und Weiterentwicklung von GitLab Runnern und CI/CD-Pipelines
Profil:
- Studium Informatik, Elektro-/Informationstechnik oder vergleichbar
- Erfahrung mit Linux-Betriebssystemen
- Gute Python-Kenntnisse
- Erfahrung mit Virtualisierungssoftware und CI/CD-Pipelines (GitLab Runner)
- Versionsverwaltung (GitLab/GitHub), agile Methoden (Scrum)
- Gute Deutsch- und Englischkenntnisse
- Junior bis Mid Level willkommen (50k-55k Junior, 60k-70k Mid)
"""

TS_CV = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=1.2cm,bottom=1.2cm,left=1.4cm,right=1.4cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\definecolor{accent}{RGB}{1,105,111}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\vspace{-4pt}\rule{\linewidth}{0.6pt}\vspace{2pt}]
\titlespacing{\section}{0pt}{5pt}{2pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.4em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt}

\begin{document}\pagestyle{empty}

\begin{center}
  {\LARGE\bfseries Toyanath Pandey}\\[3pt]
  Kerckhoff Str. 146, 45144 Essen \quad|\quad +49 159 063 77419 \quad|\quad \href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
  \href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya} \quad|\quad \href{https://github.com/Toya62}{github.com/Toya62} \quad|\quad Geb. 22.05.1997
\end{center}
\vspace{2pt}

\section{Profil}
DevOps- und Testautomatisierungs-Ingenieur mit M.Sc. in Computer \& Systems Engineering (TU Ilmenau) und fundierter praktischer Erfahrung in Linux-Systemadministration, automatisierter Testdurchführung (HIL/SIL), CI/CD-Pipelines (GitLab Runner, Jenkins) sowie Python-Toolentwicklung. Praktische Erfahrung mit hardwarenahen Testboxen und Steuergeräte-Diagnostik bei Bosch Engineering. Hohe Motivation zur Betreuung und Weiterentwicklung moderner Testinfrastrukturen bei T\&S in Kiel.

\vspace{3pt}

\section{Berufserfahrung}

\textbf{Hochschule Koblenz} \hfill \textit{10.2025 -- 09.2026}\\
\textit{Wissenschaftlicher Mitarbeiter (Research Assistant) -- CI/CD \& Linux-Infrastruktur} \hfill Koblenz, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{CI/CD-Automatisierung}: Aufbau und Wartung automatisierter Test- und Bereitstellungs-Pipelines mit GitLab CI/GitLab Runner unter Linux (Debian/Ubuntu).
  \item \textbf{Containerisierung \& Virtualisierung}: Bereitstellung reproduzierbarer Ausführungsumgebungen mittels Docker für automatisierte Software- und Validierungstests.
  \item \textbf{Python-Backend}: Entwicklung modularer Datenverarbeitungs- und API-Integrationsdienste mit kontinuierlicher Testabdeckung.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{11.2023 -- 08.2024}\\
\textit{Werkstudent Softwareentwicklung -- Assisted \& Automated Driving (AAD)} \hfill Abstatt, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Hardwarenahe Testsysteme}: Betreuung und REST-API-Integration der kamerabasierten Video-Testbox MPCFlix auf Raspberry Pi und Embedded Linux.
  \item \textbf{Test-Tools \& Fehleranalyse}: Entwicklung eines Python/C++ Tools zur automatisierten Interpretation von Fehlercodes (DTC) aus Steuergerätespeichern.
  \item \textbf{CI/CD \& Monitoring}: Automatisierung von Testworkflows in Jenkins CI/CD; Fehlersuche und Systemüberwachung mittels Splunk-Loganalyse.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{05.2023 -- 10.2023}\\
\textit{Praktikant Softwareentwicklung -- Assisted \& Automated Driving (AAD)} \hfill Abstatt, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Automatisierungstools}: Erstellung von Python-Automatisierungsskripten zur Jira REST-API-Anbindung für automatisierte Test- und Ticket-Workflows.
  \item \textbf{Test-UI}: Entwicklung von Python-Benutzeroberflächen für interne Test- und Diagnose-APIs.
\end{itemize}
\vspace{4pt}

\textbf{RE DEPOSIT Solutions GmbH (REMONDIS-Gruppe)} \hfill \textit{07.2022 -- 05.2023}\\
\textit{Werkstudent Softwareentwicklung} \hfill Lünen / Ilmenau, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{C++/Linux-Entwicklung}: Weiterentwicklung von Desktop-Anwendungen mit C++/Qt und Python unter Linux; Nutzung der GNU-Toolchain (gcc/g++, make, gdb).
  \item \textbf{Qualitätssicherung}: Durchführung von Modul-, Integrations- und Regressionstests im agilen Scrum-Team.
\end{itemize}
\vspace{4pt}

\textbf{CloudSewa Pvt. Ltd.} \hfill \textit{01.2021 -- 01.2022}\\
\textit{Security \& Infrastructure Analyst} \hfill Kathmandu, Nepal\\[2pt]
\begin{itemize}
  \item \textbf{Monitoring \& Logging}: Aufbau zentralisierter Monitoring- und Log-Pipelines mit Prometheus, Grafana und dem ELK-Stack (Elasticsearch, Kibana).
  \item \textbf{Netzwerk \& Sicherheit}: Konfiguration von Firewall-Regeln, VPNs und Netzwerksicherheitsrichtlinien auf gehärteten Linux-Servern.
\end{itemize}

\newpage

\section{Ausgewählte Projekte}

\textbf{Modern C++17 CAN Hardware Abstraction Layer} \hfill \href{https://github.com/Toya62/can-hardware-abstraction-layer}{github.com/Toya62/can-hardware-abstraction-layer}\\
\textit{C++17, Linux, SocketCAN, CMake, GoogleTest, GitHub Actions CI/CD}\\[1pt]
Hardware-Abstraktionsschicht für CAN-Bus-Kommunikation in automobilen Steuergeräten. Vollständig virtualisierte Testumgebung mit virtuellem CAN (vcan), Thread-sicherem Dispatching und automatisierten Unit-Tests in CI/CD.
\vspace{4pt}

\textbf{Karriere Pipeline -- Automatisierte Test- und Plattform-Infrastruktur} \hfill \href{https://github.com/Toya62/karriere-pipeline}{github.com/Toya62/karriere-pipeline}\\
\textit{Python, Pytest, Docker, Linux, CI/CD, SQLite WAL}\\[1pt]
Automatisierte Software-Plattform mit umfassender Testsuite (Unit-, Integrations- und Regressionsprüfungen), containerisiertem Betrieb und deterministischer Validierung.
\vspace{4pt}

\section{Ausbildung}

\textbf{M.Sc. Computer and Systems Engineering} \hfill \textit{10.2021 -- 02.2025}\\
\textit{Technische Universität Ilmenau} \hfill Ilmenau, Deutschland (Gesamtnote: 2,2)\\[2pt]
\textit{Masterarbeit}: „Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks“ (PyFlink, Apache Flink)\\
\textit{Schwerpunkte}: Software Safety (\textbf{2,0}), CMake Internals (\textbf{1,0}), Software Architectures (\textbf{1,0})
\vspace{4pt}

\textbf{B.Tech Computer Science and Engineering} \hfill \textit{08.2017 -- 06.2021}\\
\textit{Lovely Professional University} \hfill Indien
\vspace{5pt}

\section{Technische Kenntnisse}

\begin{itemize}
  \item \textbf{DevOps \& CI/CD}: GitLab CI, GitLab Runner, Jenkins, Docker, Linux (Debian, Ubuntu), Git, Bash, Terraform
  \item \textbf{Testsysteme \& Embedded}: HIL-Testsysteme, Testautomatisierung, Raspberry Pi, Embedded Linux, SocketCAN, GoogleTest, Pytest
  \item \textbf{Programmiersprachen}: Python, C/C++, Bash, SQL, Java
  \item \textbf{Build \& Debugging}: CMake, Make, Ninja, gcc/g++, gdb, Qt
  \item \textbf{Monitoring \& Observability}: Prometheus, Grafana, Splunk, ELK-Stack (Kibana)
  \item \textbf{Methoden}: Agile Entwicklung (Scrum), Versionsverwaltung, Ticket-Workflows
\end{itemize}
\vspace{4pt}

\section{Sprachen}

\textbf{Deutsch:} B2 (aktiv in Entwicklung) \quad|\quad \textbf{Englisch:} C1 (Fließend) \quad|\quad \textbf{Nepali / Hindi:} Muttersprache / Fließend

\end{document}
"""

TS_CL = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{parskip}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}\pagestyle{empty}

\textbf{Toyanath Pandey}\\[2pt]
Kerckhoff Str. 146\\[2pt]
45144 Essen\\[2pt]
+49 159 063 77419\\[2pt]
\href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
\href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya}

\vspace{10pt}

\textbf{T\&S (Technology \& Strategy)}\\[2pt]
Personalabteilung / Recruiting Team\\[2pt]
Kiel, Deutschland

\vspace{10pt}

\begin{flushright}
  Essen, 27. Oktober 2026
\end{flushright}

\vspace{2pt}

\textbf{Bewerbung als DevOps Engineer Testing (m/w/d) – Marinekommunikation}

\vspace{6pt}

Sehr geehrte Damen und Herren,

mit großem Interesse bewerbe ich mich auf die Position als DevOps Engineer Testing für Marinekommunikationssysteme bei T\&S am Standort Kiel. Als Ingenieur- und Beratungsdienstleister mit fundierter Expertise in Embedded Systems und Digitaler Transformation gestalten Sie die Technologien von morgen. Mit meinem Master of Science in Computer \& Systems Engineering der TU Ilmenau sowie praktischer Erfahrung in Linux-Systemen, Python-Testautomatisierung, CI/CD-Pipelines (GitLab Runner, Jenkins) und hardwarenahen Testumgebungen möchte ich Ihr agiles Team in Kiel tatkräftig verstärken.

Während meiner Tätigkeit bei der Bosch Engineering GmbH im Bereich Assisted \& Automated Driving habe ich intensiv an hardwarenahen Testsystemen gearbeitet. Ich betreute die Video-Testbox MPCFlix auf Basis von Raspberry Pi und Embedded Linux, integrierte REST-APIs zur Prüfstandssteuerung und entwickelte Python- sowie C++-Werkzeuge zur automatisierten Analyse von Fehlerspeicherlogs (DTC). Zudem band ich automatisierte Testabläufe in Jenkins CI/CD-Pipelines ein und führte Fehleranalysen mittels Splunk durch.

An der Hochschule Koblenz vertiefte ich meine DevOps-Kompetenzen im Betrieb virtualisierter Linux-Ausführungsumgebungen: Ich containerisierte Softwaresysteme mit Docker und baute automatisierte Test- und Bereitstellungspipelines mit GitLab Runner auf. Ergänzt wird mein Profil durch praktische C++/Qt-Softwaretests bei REMONDIS sowie fundierte Linux-Netzwerk- und Monitoringkenntnisse (Prometheus, Grafana, ELK) bei CloudSewa.

Die Betreuung von HIL-Testsystemen, der Ausbau virtualisierter Testumgebungen und die Weiterentwicklung von GitLab CI/CD-Pipelines für anspruchsvolle Marinekommunikationssysteme entsprechen exakt meinen fachlichen Stärken. Dank meines soliden Systemverständnisses und meiner hohen Auffassungsgabe arbeite ich mich schnell und zielgerichtet in spezifische Prüfstandskonfigurationen und maritime Teststrategien ein.

Ich bin uneingeschränkt bereit, für diese Position nach Kiel umzuziehen. Über die Gelegenheit, mich und meine Motivation in einem persönlichen Gespräch vorzustellen, freue ich mich sehr.

\vspace{12pt}

Mit freundlichen Grüßen,\\[8pt]
\textbf{Toyanath Pandey}

\end{document}
"""

TS_META = {
    "date": TARGET_DATE,
    "company": "T&S (Technology & Strategy)",
    "position": "DevOps Engineer Testing (m/w/d)",
    "location": "Kiel",
    "apply_url": "https://www.linkedin.com/jobs/view/4483583531",
    "role_type": "DevOps & Test Systems Engineer",
    "language": "de",
    "status": "ready_to_compile",
    "cv_file": "t-s-technology-strategy_devops-engineer-testing_cv.tex",
    "cover_file": "t-s-technology-strategy_devops-engineer-testing_cover.tex",
    "description_file": "t-s-technology-strategy_devops-engineer-testing_description.md",
    "notes": "Handcrafted ATS package for T&S Technology & Strategy (HIL Testing, Linux, Python, GitLab Runner, Marinekommunikation)."
}

# ==============================================================================
# JOB 5: MK Versuchsanlagen — Embedded Software Entwickler (German)
# ==============================================================================

MK_DESC = """Embedded Software Entwickler:in (m/w/d) bei MK Versuchsanlagen GmbH & Co. KG in Mücke (35325).
Familiengeführtes High-Tech-Unternehmen (230 Mitarbeitende), Reinraumsysteme sowie Mess- und Prüfgeräte für Industrie und Forschung.
Aufgaben:
- Firmware-Entwicklung, Entwicklung von Embedded Software
- Implementierung von Treibern für Sensoren, Aktoren und Peripherie
- Entwicklung von Kommunikationsprotokollen
- Mitarbeit bei Cybersecurity Risikoanalysen und grundlegenden Sicherheitsbewertungen
- Entwicklung automatisierter Testverfahren
- Fehleranalyse und Root-Cause-Analysen auf System- und Komponentenebene
- Erstellung technischer Dokumentationen
- Mitarbeit bei der Auswahl und Evaluierung von Mikrocontrollern und Embedded-Plattformen
Profil:
- Fachinformatiker, Techniker oder Studium im Bereich Embedded Systems oder vergleichbar
- Kenntnisse in Softwareentwicklung, idealerweise im Bereich Embedded Systems
- Kenntnisse in Konfigurationsmanagementwerkzeugen
- Teamfähigkeit und Zuverlässigkeit
"""

MK_CV = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=1.2cm,bottom=1.2cm,left=1.4cm,right=1.4cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\definecolor{accent}{RGB}{1,105,111}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\vspace{-4pt}\rule{\linewidth}{0.6pt}\vspace{2pt}]
\titlespacing{\section}{0pt}{5pt}{2pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.4em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt}

\begin{document}\pagestyle{empty}

\begin{center}
  {\LARGE\bfseries Toyanath Pandey}\\[3pt]
  Kerckhoff Str. 146, 45144 Essen \quad|\quad +49 159 063 77419 \quad|\quad \href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
  \href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya} \quad|\quad \href{https://github.com/Toya62}{github.com/Toya62} \quad|\quad Geb. 22.05.1997
\end{center}
\vspace{2pt}

\section{Profil}
Embedded Software- und Systems-Engineer mit M.Sc. in Computer \& Systems Engineering (TU Ilmenau) und fundierter praktischer Erfahrung in hardwarenaher Softwareentwicklung (C/C++, Python), Treiberimplementierung, Kommunikationsprotokollen (CAN, UART, SocketCAN) sowie Linux-Systemen (Embedded Linux, Raspberry Pi). Fundierte Kenntnisse in Cybersecurity-Risikoanalysen (CEH – Certified Ethical Hacker, abgelaufen 2023) und automatisierten Testverfahren für Mess-, Prüf- und Reinraumsysteme.

\vspace{3pt}

\section{Berufserfahrung}

\textbf{Hochschule Koblenz} \hfill \textit{10.2025 -- 09.2026}\\
\textit{Wissenschaftlicher Mitarbeiter (Research Assistant) -- Softwareentwicklung} \hfill Koblenz, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Backend-Systeme \& Validierung}: Entwicklung modularer Datenverarbeitungswerkzeuge in Python unter Linux; automatisierte Datenvalidierung und Schnittstellenanbindung.
  \item \textbf{Container \& CI/CD}: Aufbau containerisierter Ausführungsumgebungen (Docker) und Integration automatisierter Tests in GitLab CI.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{11.2023 -- 08.2024}\\
\textit{Werkstudent Softwareentwicklung -- Assisted \& Automated Driving (AAD)} \hfill Abstatt, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Embedded Linux \& Sensorik}: Mitwirkung an der MPCFlix-Videoerfassungsbox auf Raspberry Pi und Embedded Linux; REST-API-Anbindung und Peripherie-Kommunikation.
  \item \textbf{C++ Steuergeräte-Diagnose}: Entwicklung und Optimierung von Diagnosetools (DTC-Interpreter) zur automatisierten Auswertung und Fehleranalyse von Steuergerätespeichern.
  \item \textbf{Automatisierte Tests}: Integration automatisierter Testläufe in Jenkins CI/CD; systematische Fehleranalyse mit Splunk.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{05.2023 -- 10.2023}\\
\textit{Praktikant Softwareentwicklung -- Assisted \& Automated Driving (AAD)} \hfill Abstatt, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Schnittstellen \& Tools}: Entwicklung von Python-Automatisierungstools zur Jira REST API-Anbindung für Batch-Ticketverarbeitung.
  \item \textbf{Fehleranalyse}: Hardwarenahe Fehleranalyse an Videotestboxen für Frontkamera-Steuergeräte.
\end{itemize}
\vspace{4pt}

\textbf{RE DEPOSIT Solutions GmbH (REMONDIS-Gruppe)} \hfill \textit{07.2022 -- 05.2023}\\
\textit{Werkstudent Softwareentwicklung} \hfill Lünen / Ilmenau, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{C++/Qt-Entwicklung}: Programmierung hardwarenaher und grafischer Anwendungen in C++/Qt unter Linux (Debian/Ubuntu); Nutzung von gcc/g++, make und gdb.
  \item \textbf{Debugging \& Tests}: Statische Codeanalysen, Speicherleckprüfung und Durchführung von Modultests im agilen Scrum-Team.
\end{itemize}
\vspace{4pt}

\textbf{CloudSewa Pvt. Ltd.} \hfill \textit{01.2021 -- 01.2022}\\
\textit{Security \& Infrastructure Analyst} \hfill Kathmandu, Nepal\\[2pt]
\begin{itemize}
  \item \textbf{Cybersecurity \& Risikoanalysen}: Durchführung von Schwachstellenbewertungen (OWASP); Konfiguration gehärteter Linux-Netzwerke, Firewalls und VPNs.
  \item \textbf{Monitoring \& Logging}: Überwachung verteilter Systeme mittels Prometheus/Grafana und ELK-Stack.
\end{itemize}

\newpage

\section{Ausgewählte Projekte}

\textbf{Modern C++17 CAN Hardware Abstraction Layer} \hfill \href{https://github.com/Toya62/can-hardware-abstraction-layer}{github.com/Toya62/can-hardware-abstraction-layer}\\
\textit{C++17, Linux, SocketCAN, Modern CMake, GoogleTest, Thread-Safety}\\[1pt]
Polymorphe Hardware-Abstraktionsschicht für CAN-Bus-Kommunikation in automobilen Steuergeräten. Unterstützt Frame-Filterung, virtuelle CAN-Simulation (vcan), Thread-sicheres Dispatching und automatisierte Unit-Tests.
\vspace{4pt}

\textbf{PyFlink Stream Processing Engine} \hfill \href{https://github.com/Toya62/pyflink-weather-stream-pipeline}{github.com/Toya62/pyflink-weather-stream-pipeline}\\
\textit{Apache Flink, PyFlink, Kafka, Python, Docker}\\[1pt]
Verteilte Streaming-Pipeline zur Erfassung und Auswertung hochfrequenter Sensorsignale mit automatisierter Anomalieerkennung und kontinuierlicher Datenfilterung.
\vspace{4pt}

\section{Ausbildung}

\textbf{M.Sc. Computer and Systems Engineering} \hfill \textit{10.2021 -- 02.2025}\\
\textit{Technische Universität Ilmenau} \hfill Ilmenau, Deutschland (Gesamtnote: 2,2)\\[2pt]
\textit{Masterarbeit}: „Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks“\\
\textit{Schwerpunktnoten}: Software Safety (\textbf{2,0}), CMake Internals (\textbf{1,0}), Software Architectures (\textbf{1,0})
\vspace{4pt}

\textbf{B.Tech Computer Science and Engineering} \hfill \textit{08.2017 -- 06.2021}\\
\textit{Lovely Professional University} \hfill Indien
\vspace{5pt}

\section{Zertifizierungen}

\textbf{Cybersecurity}: CEH -- Certified Ethical Hacker (abgelaufen 2023)
\vspace{4pt}

\section{Technische Kenntnisse}

\begin{itemize}
  \item \textbf{Embedded \& Hardwarenah}: C/C++, Embedded Linux, Raspberry Pi, CAN-Bus, SocketCAN, DTC-Diagnosetools, Treiberentwicklung, Sensoren/Aktoren
  \item \textbf{Entwicklungswerkzeuge}: CMake, Make, Ninja, gcc/g++, gdb, Qt, Git, GitLab CI, Jenkins
  \item \textbf{Sicherheit \& Protokolle}: Cybersecurity-Risikoanalysen, OWASP, TCP/IP, Kommunikationsprotokolle, Firewall/VPN
  \item \textbf{Programmiersprachen}: C, C++, Python, Bash, SQL, Java
  \item \textbf{Testing \& Qualität}: Automatisierte Testverfahren, GoogleTest, Pytest, Root-Cause-Fehleranalyse
\end{itemize}
\vspace{4pt}

\section{Sprachen}

\textbf{Deutsch:} B2 (aktiv in Entwicklung) \quad|\quad \textbf{Englisch:} C1 (Fließend) \quad|\quad \textbf{Nepali / Hindi:} Muttersprache / Fließend

\end{document}
"""

MK_CL = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{parskip}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}\pagestyle{empty}

\textbf{Toyanath Pandey}\\[2pt]
Kerckhoff Str. 146\\[2pt]
45144 Essen\\[2pt]
+49 159 063 77419\\[2pt]
\href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
\href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya}

\vspace{10pt}

\textbf{MK Versuchsanlagen GmbH \& Co. KG}\\[2pt]
Personalabteilung\\[2pt]
35325 Mücke, Deutschland

\vspace{10pt}

\begin{flushright}
  Essen, 27. Oktober 2026
\end{flushright}

\vspace{2pt}

\textbf{Bewerbung als Embedded Software Entwickler:in (m/w/d)}

\vspace{6pt}

Sehr geehrte Damen und Herren,

mit großem Interesse bewerbe ich mich auf die Position als Embedded Software Entwickler:in bei MK Versuchsanlagen. Als renommiertes, technologiegetriebenes Familienunternehmen setzen Sie mit Ihren innovativen Reinraumsystemen sowie Mess- und Prüfgeräten weltweite Qualitätsmaßstäbe. Mit meinem Master of Science in Computer \& Systems Engineering der TU Ilmenau, praktischer Erfahrung in hardwarenaher C/C++- und Python-Entwicklung unter Linux sowie fundierten Kenntnissen in Kommunikationsprotokollen und Cybersecurity möchte ich Ihr Entwicklungsteam in Mücke verstärken.

Während meiner Tätigkeit bei der Bosch Engineering GmbH im Bereich Assisted \& Automated Driving habe ich intensiv an eingebetteten Systemen gearbeitet: Ich wirkte an der kamerabasierten Videoerfassungsbox MPCFlix auf Raspberry Pi und Embedded Linux mit, band Sensor- und Steuerungsschnittstellen über REST-APIs an und entwickelte C++-Werkzeuge (DTC-Interpreter) zur automatisierten Interpretation von Fehlercodes auf Steuergeräteebene. Ergänzend programmierte ich bei REMONDIS hardwarenahe Desktop- und Steuerungsanwendungen in C++/Qt unter Linux unter Einsatz moderner GNU-Toolchains (gcc/g++, make, gdb).

Darüber hinaus verfüge ich über fundierte Erfahrung in Cybersecurity-Risikoanalysen und Sicherheitsbewertungen (CEH – Certified Ethical Hacker, abgelaufen 2023) aus meiner Zeit als Security Analyst bei CloudSewa. Diese Kombination aus hardwarenaher Programmierung, fundiertem Protokollverständnis (z.\,B. CAN-Bus/SocketCAN) und Sicherheitsbewusstsein ermöglicht es mir, robuste Treiber für Sensoren und Aktoren zu implementieren und verlässliche automatisierte Testverfahren für Ihre Mess- und Prüfsysteme aufzusetzen.

Ich zeichne mich durch eine eigenverantwortliche, strukturierte Arbeitsweise und ausgeprägtes Qualitätsbewusstsein aus. Gerne bringe ich meine Fähigkeiten in Ihre flachen Unternehmensstrukturen ein und bin für diese Position uneingeschränkt bereit, nach Mücke bzw. in die Region Mittelhessen umzuziehen.

Ich freue mich über die Gelegenheit, mich in einem persönlichen Gespräch vorzustellen.

\vspace{12pt}

Mit freundlichen Grüßen,\\[8pt]
\textbf{Toyanath Pandey}

\end{document}
"""

MK_META = {
    "date": TARGET_DATE,
    "company": "MK Versuchsanlagen GmbH & Co. KG",
    "position": "Embedded Software Entwickler:in (m/w/d)",
    "location": "Mücke",
    "apply_url": "https://www.arbeitsagentur.de/jobsuche/jobdetail/13651-JOB-868158-S",
    "role_type": "Embedded Systems / C++ Integration",
    "language": "de",
    "status": "ready_to_compile",
    "cv_file": "mk-versuchsanlagen_embedded-software-entwickler_cv.tex",
    "cover_file": "mk-versuchsanlagen_embedded-software-entwickler_cover.tex",
    "description_file": "mk-versuchsanlagen_embedded-software-entwickler_description.md",
    "notes": "Handcrafted ATS package for MK Versuchsanlagen (Firmware, Embedded Linux, Sensor/Aktor-Treiber, C/C++, Cybersecurity)."
}

# ==============================================================================
# JOB 6: Debeka — Backend-Developer (German)
# ==============================================================================

DEBEKA_DESC = """Backend-Developer (w/m/d) bei Debeka in Koblenz (RP, DE).
Aufgaben:
- Entwicklung von Backend-Services für Kundenanwendungen (Online Services, Debeka.de, Kundenportal) auf Basis gängiger und moderner Technologien (REST, Quarkus, Container, Kafka, Camunda, API Management/Gateway)
- Stetige Weiterentwicklung der bestehenden Backend-Architektur und Infrastruktur
- Mitarbeit bei Konzeption und Spezifikation von APIs (OpenAPI)
- Verwendung und Ausbau des CI/CD-Software-Entwicklungsprozesses (gitops-like) inkl. Code-Reviews, Security-Tests, automatisierten Tests
- Entwicklung von Anwendungen mit hohen Anforderungen bzgl. IT-Security und Test-Automatisierung
Profil:
- Programmiererfahrung in Java oder vergleichbaren Programmiersprachen
- Erfahrung in Basis-Technologien und Konzepten der Web-Entwicklung (HTTP, REST, SQL, OAuth)
- Kenntnisse von zeitgemäßen CI/CD-Prozessen und Versionsverwaltung (git)
- Interesse und Lernbereitschaft für neue Technologien
- Idealerweise Kenntnisse in Container-Umgebungen (OpenShift, Docker)
- Kenntnisse und Methoden aus IT-Security sowie Testing (Unit-Tests, Last-Tests, BDD)
"""

DEBEKA_CV = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=1.2cm,bottom=1.2cm,left=1.4cm,right=1.4cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\definecolor{accent}{RGB}{1,105,111}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\vspace{-4pt}\rule{\linewidth}{0.6pt}\vspace{2pt}]
\titlespacing{\section}{0pt}{5pt}{2pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.4em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt}

\begin{document}\pagestyle{empty}

\begin{center}
  {\LARGE\bfseries Toyanath Pandey}\\[3pt]
  Kerckhoff Str. 146, 45144 Essen \quad|\quad +49 159 063 77419 \quad|\quad \href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
  \href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya} \quad|\quad \href{https://github.com/Toya62}{github.com/Toya62} \quad|\quad Geb. 22.05.1997
\end{center}
\vspace{2pt}

\section{Profil}
Backend- und Software-Engineer mit M.Sc. in Computer \& Systems Engineering (TU Ilmenau) und fundierter praktischer Erfahrung in der Entwicklung robuster Backend-Services (Java, Python), REST/GraphQL-APIs, ereignisgesteuerter Architekturen (Apache Kafka) sowie relationaler Datenbanksysteme (SQL, PostgreSQL). Fundierte Expertise in Anwendungs- und Netzwerksicherheit (OWASP) sowie containerisierten CI/CD-Pipelines (Docker, GitLab CI). Vertraut mit dem Standort Koblenz durch Forschungstätigkeit.

\vspace{3pt}

\section{Berufserfahrung}

\textbf{Hochschule Koblenz} \hfill \textit{10.2025 -- 09.2026}\\
\textit{Wissenschaftlicher Mitarbeiter (Research Assistant) -- Backend \& Dateninfrastruktur} \hfill Koblenz, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Backend-Services \& API-Integration}: Konzeption und Implementierung modularer Python-Backend-Dienste zur Abfrage und Verarbeitung heterogener REST- und GraphQL-APIs.
  \item \textbf{Containerisierung \& CI/CD}: Aufbau und Betrieb reproduzierbarer Docker-Containerumgebungen auf Linux-Servern; Einbindung automatisierter Test- und Validierungsworkflows in GitLab CI.
  \item \textbf{Datenqualität}: Implementierung robuster Schemavalidierungen zur Absicherung der Datenkonsistenz über den gesamten Datenfluss.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{11.2023 -- 08.2024}\\
\textit{Werkstudent Softwareentwicklung -- Assisted \& Automated Driving (AAD)} \hfill Abstatt, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Schnittstellen- \& Tool-Entwicklung}: Weiterentwicklung interner Diagnosetools (DTC-Interpreter in C++ und Python) zur Analyse komplexer Steuergeräteprotokolle.
  \item \textbf{REST-API \& Linux-Integration}: Anbindung von REST-Schnittstellen für das Kamerasystem MPCFlix auf Raspberry Pi unter Embedded Linux.
  \item \textbf{CI/CD \& Log-Analyse}: Integration automatisierter Testläufe in Jenkins CI/CD; Fehlersuche und Monitoring mittels Splunk.
\end{itemize}
\vspace{4pt}

\textbf{Bosch Engineering GmbH} \hfill \textit{05.2023 -- 10.2023}\\
\textit{Praktikant Softwareentwicklung -- Assisted \& Automated Driving (AAD)} \hfill Abstatt, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{API-Automatisierung}: Entwicklung von Python-Tools zur automatisierten Anbindung an die Jira REST API für Batch-Ticketverarbeitung und Synchronisation.
  \item \textbf{UI-Entwicklung}: Implementierung von Python-Oberflächen für interne Test- und Diagnose-APIs.
\end{itemize}
\vspace{4pt}

\textbf{RE DEPOSIT Solutions GmbH (REMONDIS-Gruppe)} \hfill \textit{07.2022 -- 05.2023}\\
\textit{Werkstudent Softwareentwicklung} \hfill Lünen / Ilmenau, Deutschland\\[2pt]
\begin{itemize}
  \item \textbf{Softwareentwicklung}: Entwicklung und Refactoring von Desktop-Anwendungen mit C++/Qt und Python unter Linux; relationale Datenbankanbindung.
  \item \textbf{Qualitätssicherung}: Durchführung von Modul- und Regressionstests im agilen Scrum-Team.
\end{itemize}
\vspace{4pt}

\textbf{CloudSewa Pvt. Ltd.} \hfill \textit{01.2021 -- 01.2022}\\
\textit{Security \& Infrastructure Analyst} \hfill Kathmandu, Nepal\\[2pt]
\begin{itemize}
  \item \textbf{IT-Security \& OWASP}: Durchführung von Sicherheitsbewertungen und Penetrationstests für Web- und Mobilanwendungen nach OWASP Top 10.
  \item \textbf{Monitoring \& SIEM}: Zentralisierte Log-Auswertung mittels ELK-Stack (Elasticsearch, Logstash, Kibana) sowie Prometheus und Grafana.
  \item \textbf{Netzwerk-Härtung}: Konfiguration von Firewall-Regelwerken, VPN-Tunneln und sicheren Zugriffskontrollen.
\end{itemize}

\newpage

\section{Ausgewählte Projekte}

\textbf{Karriere Pipeline -- Autonome Backend-Plattform \& API-Engine} \hfill \href{https://github.com/Toya62/karriere-pipeline}{github.com/Toya62/karriere-pipeline}\\
\textit{Python, REST APIs, SQLite (WAL), Pydantic, Docker, CI/CD}\\[1pt]
Modulare Backend-Architektur mit asynchroner Datenextraktion, REST-API-Anbindung, SQLite-Deduplikation, deterministischer Schemavalidierung und automatisierter Berichtsgenerierung.
\vspace{4pt}

\textbf{PyFlink \& Kafka Weather Stream Processing} \hfill \href{https://github.com/Toya62/pyflink-weather-stream-pipeline}{github.com/Toya62/pyflink-weather-stream-pipeline}\\
\textit{Apache Kafka, Apache Flink, PyFlink, Python, Docker, Streaming ETL}\\[1pt]
Ereignisgesteuerte Streaming-Architektur mit Apache Kafka zur Erfassung kontinuierlicher Datenströme, zustandsbehafteten Transformationen und zuverlässiger Speicherung in relationalen Datenbanken.
\vspace{4pt}

\section{Ausbildung}

\textbf{M.Sc. Computer and Systems Engineering} \hfill \textit{10.2021 -- 02.2025}\\
\textit{Technische Universität Ilmenau} \hfill Ilmenau, Deutschland (Gesamtnote: 2,2)\\[2pt]
\textit{Masterarbeit}: „Metamorphosis -- A seamless mapping of stream processing pipelines between development and execution frameworks“ (Fokus auf Apache Flink, PyFlink und Kafka)\\
\textit{Schwerpunkte}: Software Architectures (\textbf{1,0}), Advanced Database Systems (\textbf{2,0}), Software Safety (\textbf{2,0})
\vspace{4pt}

\textbf{B.Tech Computer Science and Engineering} \hfill \textit{08.2017 -- 06.2021}\\
\textit{Lovely Professional University} \hfill Indien
\vspace{5pt}

\section{Technische Kenntnisse}

\begin{itemize}
  \item \textbf{Programmiersprachen}: Java, Python, SQL, C/C++, Bash, TypeScript (Grundlagen)
  \item \textbf{Backend \& APIs}: REST APIs, GraphQL, OpenAPI/Swagger, FastAPI, Flask, Quarkus (hohe Lernbereitschaft), HTTP, OAuth
  \item \textbf{Messaging \& Streaming}: Apache Kafka, Stream Processing, Apache Flink, PyFlink
  \item \textbf{Datenbanken}: PostgreSQL, MySQL, SQLite, Relationale Datenmodellierung, SQL-Optimierung
  \item \textbf{Container \& CI/CD}: Docker, OpenShift-Grundlagen, GitLab CI, Jenkins, Git, Linux (Debian, Ubuntu)
  \item \textbf{IT-Security \& Testing}: OWASP Top 10, Sicherheitsprüfungen, Modultests, Pytest, Lasttests, Logging (ELK, Splunk)
\end{itemize}
\vspace{4pt}

\section{Sprachen}

\textbf{Deutsch:} B2 (aktiv in Entwicklung) \quad|\quad \textbf{Englisch:} C1 (Fließend) \quad|\quad \textbf{Nepali / Hindi:} Muttersprache / Fließend

\end{document}
"""

DEBEKA_CL = r"""\documentclass[a4paper,10pt]{article}
\usepackage[a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{parskip}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}\pagestyle{empty}

\textbf{Toyanath Pandey}\\[2pt]
Kerckhoff Str. 146\\[2pt]
45144 Essen\\[2pt]
+49 159 063 77419\\[2pt]
\href{mailto:pandeytoya22@gmail.com}{pandeytoya22@gmail.com}\\[2pt]
\href{https://linkedin.com/in/pandeytoya}{linkedin.com/in/pandeytoya}

\vspace{10pt}

\textbf{Debeka}\\[2pt]
Abteilung Customer Services / Recruiting\\[2pt]
Koblenz, Deutschland

\vspace{10pt}

\begin{flushright}
  Essen, 27. Oktober 2026
\end{flushright}

\vspace{2pt}

\textbf{Bewerbung als Backend-Developer (w/m/d) – Customer Services}

\vspace{6pt}

Sehr geehrte Damen und Herren,

mit großem Interesse bewerbe ich mich auf die Position als Backend-Developer in der Abteilung Customer Services bei der Debeka in Koblenz. Als eine der führenden Versicherungs- und Bauspargruppen sichern Sie die Zukunft von über 7,5 Millionen Mitgliedern. Die Weiterentwicklung Ihrer digitalen Plattformen—insbesondere des Mitgliederportals und der Online-Services—auf Basis moderner Technologien wie REST, Kafka und Container-Architekturen spricht mich fachlich wie persönlich sehr an.

Durch meine Tätigkeit als wissenschaftlicher Mitarbeiter an der Hochschule Koblenz bin ich mit dem Standort Koblenz bestens vertraut. An der Hochschule konzipierte und betrieb ich modulare Backend-Services in Python, integrierte REST- und GraphQL-Schnittstellen und stellte reproduzierbare Ausführungsumgebungen mittels Docker auf Linux-Servern bereit. Durch automatisierte Test- und Validierungspipelines in GitLab CI stellte ich höchste Softwarezuverlässigkeit sicher. Während meines Masterstudiums an der TU Ilmenau (Masterarbeit über verteilte Stream-Verarbeitung mit Apache Flink und Kafka) vertiefte ich fundierte Kenntnisse in objektorientiertem Softwaredesign in Java und nachrichtenbasierten Architekturen.

Zusätzlich bringe ich wertvolle Praxiserfahrung im Bereich IT-Sicherheit aus meiner Zeit als Security Analyst bei CloudSewa mit: Die Absicherung von Webanwendungen nach OWASP-Standards, sichere Authentifizierungsverfahren (OAuth/HTTP) und die Log-Analyse mit SIEM- und Monitoring-Systemen (ELK, Splunk) sind mir bestens vertraut. Bei Bosch Engineering entwickelte ich REST-Schnittstellen und automatisierte Jenkins-CI/CD-Workflows für interne Diagnosesysteme.

Dank meines fundierten Hintergrunds in Java, REST-APIs, relationalen Datenbanken und Kafka übertrage ich bewährte Architekturmuster schnell und zielgerichtet auf Ihr Framework Quarkus und GitOps-gestützte OpenShift-Umgebungen. Ich schätze das kollegiale Miteinander im agilen Team und freue mich darauf, zur digitalen Zukunft der Debeka beizutragen.

Ein Umzug nach Koblenz bzw. Arbeiten vor Ort ist für mich problemlos und kurzfristig realisierbar. Über die Gelegenheit, mich Ihnen in einem persönlichen Gespräch vorzustellen, freue ich mich sehr.

\vspace{12pt}

Mit freundlichen Grüßen,\\[8pt]
\textbf{Toyanath Pandey}

\end{document}
"""

DEBEKA_META = {
    "date": TARGET_DATE,
    "company": "Debeka",
    "position": "Backend-Developer (w/m/d)",
    "location": "Koblenz",
    "apply_url": "https://de.indeed.com/viewjob?jk=0b7026fe5cd9dfe9",
    "role_type": "Backend Platform Engineer / Java",
    "language": "de",
    "status": "ready_to_compile",
    "cv_file": "debeka_backend-developer_cv.tex",
    "cover_file": "debeka_backend-developer_cover.tex",
    "description_file": "debeka_backend-developer_description.md",
    "notes": "Handcrafted ATS package for Debeka (REST, Java/Quarkus, Kafka, Docker, IT Security, Testing, Koblenz)."
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    jobs = [
        ("stargazr_software-engineer", STARGAZR_CV, STARGAZR_CL, STARGAZR_META, STARGAZR_DESC),
        ("universitat-hamburg_research-software-engineer", UNI_HAMBURG_CV, UNI_HAMBURG_CL, UNI_HAMBURG_META, UNI_HAMBURG_DESC),
        ("kayak_data-engineer", KAYAK_CV, KAYAK_CL, KAYAK_META, KAYAK_DESC),
        ("t-s-technology-strategy_devops-engineer-testing", TS_CV, TS_CL, TS_META, TS_DESC),
        ("mk-versuchsanlagen_embedded-software-entwickler", MK_CV, MK_CL, MK_META, MK_DESC),
        ("debeka_backend-developer", DEBEKA_CV, DEBEKA_CL, DEBEKA_META, DEBEKA_DESC),
    ]

    for slug, cv_tex, cl_tex, meta, desc in jobs:
        print(f"\n--- Processing {slug} ---")
        write_file(f"{slug}_cv.tex", cv_tex)
        write_file(f"{slug}_cover.tex", cl_tex)
        write_file(f"{slug}.meta.json", json.dumps(meta, indent=2))
        write_file(f"{slug}_description.md", desc)

    print("\nAll 6 application packages generated in applications/2026-10-27/!")

if __name__ == "__main__":
    main()
