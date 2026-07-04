<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenAI%20GPT-412991?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/Tkinter-GUI-FF6B35?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Status-Complete-2ea44f?style=for-the-badge"/>

# Smart Email Classifier & Summarizer System

**An AI-powered desktop application that automatically classifies emails into categories and generates concise summaries — built with SQL Server, Python, OpenAI GPT, and Tkinter.**

[Features](#-features) · [Architecture](#-architecture) · [Database Design](#-database-design) · [Setup](#-setup) · [Usage](#-usage) · [Project Structure](#-project-structure)

---

</div>

## Overview

Managing large volumes of emails is a growing challenge in modern digital communication. This project solves that problem by building a full-stack desktop application that:

- **Stores** emails and users in a normalized SQL Server relational database
- **Classifies** each email into one of five categories using OpenAI's GPT API
- **Summarizes** email content into 2–3 concise lines using NLP
- **Displays** everything through an interactive desktop GUI — no command-line input required

Built as a 4th Semester DBMS Lab project at university, this system demonstrates end-to-end integration of database management, backend engineering, AI/NLP APIs, and GUI development.

---

## Features

- **AI Classification** — Automatically assigns one of five categories: `Work` · `Personal` · `Spam` · `Important` · `Promotions`
- **AI Summarization** — Generates a 2–3 sentence summary for every email
- **Two-Panel GUI** — Email list on the left, full detail view (body + category + summary) on the right
- **Category Filter Bar** — One-click filtering by category
- **Idempotent Pipeline** — Re-running the backend never duplicates or overwrites existing results
- **Live Data** — GUI always reads directly from the database; no hardcoded or cached content
- **Refresh Button** — Reload emails without restarting the app
- **Colour-Coded Categories** — Instant visual distinction between email types
- **Modular Backend** — 6 single-responsibility Python modules for clean separation of concerns
- **Secure by Design** — API key isolated in config, parameterised SQL queries throughout

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GUI Layer                            │
│              Tkinter — Two-panel desktop interface          │
│         Left: Email list    Right: Detail + AI output       │
└────────────────────────┬────────────────────────────────────┘
                         │ live SQL queries
┌────────────────────────▼────────────────────────────────────┐
│                    Python Backend                           │
│  db_connect → fetch_emails → prompt_builder                 │
│            → ai_processor → save_results                    │
└──────────┬──────────────────────────────┬───────────────────┘
           │ pyodbc                       │ OpenAI SDK
┌──────────▼──────────┐       ┌───────────▼───────────────────┐
│   SQL Server DB     │       │       OpenAI GPT API           │
│                     │       │                                │
│  Users              │       │  Classification + Summary      │
│  Emails             │       │  returned as structured JSON   │
│  Categories         │       └───────────────────────────────┘
│  AI_Output          │
└─────────────────────┘
```

---

## Database Design

### Schema (3rd Normal Form)

The database is fully normalized to 3NF — eliminating redundancy, preventing update anomalies, and ensuring referential integrity.

```sql
Users         (user_id PK, name, email UNIQUE, created_at)
      │ 1:M
Emails        (email_id PK, user_id FK, subject, body, sender, received_at)
      │ 1:1
AI_Output     (output_id PK, email_id FK, category_id FK, summary)
      │ M:1
Categories    (category_id PK, category_name UNIQUE)
```

### Relationships

| Relationship | Type | Description |
|---|---|---|
| Users → Emails | 1 : Many | One user owns many emails |
| Emails → AI_Output | 1 : 1 | Each email has one AI result |
| Categories → AI_Output | 1 : Many | One category assigned to many outputs |

### Why 3NF matters here
Storing `category_name` directly in `AI_Output` would create a transitive dependency:
`output_id → category_id → category_name`. By keeping it in a dedicated `Categories` table, renaming a category requires changing one row — not every row in `AI_Output`.

---

## Project Structure

```
smart-email-classifier/
│
├── backend/
│   ├── config_template.py   # Copy to config.py and fill in credentials
│   ├── db_connect.py        # pyodbc connection setup
│   ├── fetch_emails.py      # SQL queries — unprocessed emails & category map
│   ├── prompt_builder.py    # Constructs the GPT prompt per email
│   ├── ai_processor.py      # Calls OpenAI API, parses JSON response
│   ├── save_results.py      # INSERTs AI results into AI_Output table
│   └── main.py              # Pipeline orchestrator — runs all modules in order
│
├── gui.py                   # Tkinter two-panel GUI (entry point)
├── schema.sql               # Full DDL + sample data
├── relational_schema.html   # Interactive schema diagram (open in browser)
└── README.md
```

---

## Setup

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | [python.org](https://python.org) |
| SQL Server | 2019+ | Express edition is free |
| SSMS | 18+ | For running the SQL script |
| ODBC Driver 17 | Latest | [Download from Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) |
| OpenAI API Key | Active | [platform.openai.com](https://platform.openai.com) |

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/smart-email-classifier.git
cd smart-email-classifier
```

**2. Install Python dependencies**
```bash
pip install pyodbc openai
```

**3. Set up the database**

Open SSMS, connect to your SQL Server instance, open a New Query window, and run the full `schema.sql` file. This creates the database, all four tables, and loads 12 sample emails.

**4. Configure credentials**
```bash
cp backend/config_template.py backend/config.py
```

Then open `backend/config.py` and update:

```python
DB_CONFIG = {
    "server":   "YOUR_SERVER_NAME",   # from SSMS Object Explorer
    "database": "Smart_Email_Clssifier_and_Summarizer_System",
    "trusted":  True,                  # Windows Auth — no password needed
}

OPENAI_API_KEY = "sk-..."             # your OpenAI key
```

> **Finding your server name:** In SSMS, right-click the server in Object Explorer → Properties. Common formats: `DESKTOP-ABC\SQLEXPRESS` or `localhost`.

---

## Usage

### Step 1 — Run the AI pipeline

```bash
cd backend
python main.py
```

Expected output:
```
=======================================================
  Smart Email Classifier — Backend Pipeline Starting
=======================================================
[db_connect]   Connected to SQL Server successfully.
[fetch_emails] Found 12 unprocessed email(s).

[main] (1/12) email_id=1 — 'Project Meeting'
[ai_processor] email_id 1 → category='Work'
[save_results] Saved  email_id=1  category='Work'  (id=1)
...
=======================================================
  Pipeline complete.
  Emails processed : 12
  AI results saved : 12
  Failures         : 0
=======================================================
```

### Step 2 — Launch the GUI

```bash
cd ..
python gui.py
```

The window opens, loads all emails from the database, and the app is fully interactive.

> **Note:** If you re-run `main.py`, it automatically skips already-processed emails. To reprocess everything, run `DELETE FROM AI_Output` in SSMS first.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Database | Microsoft SQL Server | Relational data storage — 3NF normalized schema |
| Connectivity | pyodbc | Python-to-SQL Server bridge via ODBC |
| AI / NLP | OpenAI GPT API | Email classification and summarization |
| Backend | Python 3.10+ | Pipeline orchestration, prompt engineering, JSON parsing |
| GUI | Tkinter | Cross-platform desktop interface (stdlib — no extra install) |
| Version Control | Git + GitHub | Source control and portfolio hosting |

---

## Key Implementation Details

### Idempotent Processing Pipeline
The backend uses a `LEFT JOIN ... WHERE IS NULL` pattern to detect unprocessed emails:
```sql
SELECT E.email_id, E.subject, E.body, E.sender
FROM   Emails AS E
LEFT JOIN AI_Output AS A ON E.email_id = A.email_id
WHERE  A.output_id IS NULL
ORDER BY E.received_at ASC;
```
Running the pipeline multiple times is always safe — existing results are never touched.

### Structured AI Prompting
Each email is sent with an explicit JSON contract:
```
Return ONLY a valid JSON object with exactly two keys:
  "category" : one of [Work, Personal, Spam, Important, Promotions]
  "summary"  : a concise 2-3 sentence summary
```
The response is validated against the allowed category list, with a fallback to `Important` for unexpected values.

### Cascade Delete Integrity
```sql
FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
FOREIGN KEY (email_id) REFERENCES Emails(email_id) ON DELETE CASCADE
```
Deleting a user automatically removes all their emails and AI outputs — no orphan records.

---

## Challenges & Resolutions

| Challenge | Root Cause | Resolution |
|---|---|---|
| `APIRemovedInV1` error | openai >= 1.0.0 removed `ChatCompletion.create()` | Migrated to new client-based SDK: `client.chat.completions.create()` |
| `ModuleNotFoundError` on Windows | Relative `sys.path` failed under Git Bash | Replaced with `os.path.abspath()` for reliable absolute path resolution |
| `TclError: unknown option -lettersp` | `lettersp` is not a valid Tkinter Label parameter | Removed the invalid option |
| Inconsistent AI category output | Model occasionally returned wrong casing | Added validation with allowlist check and safe fallback default |

---

## Normalization Summary

| Table | 1NF | 2NF | 3NF | Key Justification |
|---|---|---|---|---|
| Users | ✅ | ✅ | ✅ | All attributes depend directly on `user_id` |
| Categories | ✅ | ✅ | ✅ | `category_name` depends only on `category_id` |
| Emails | ✅ | ✅ | ✅ | All attributes depend directly on `email_id` |
| AI_Output | ✅ | ✅ | ✅ | `category_id` FK eliminates transitive dependency on `category_name` |

---

## Author

**Muhammad Ahmad**
BSCS 4-A · 4th Semester
DBMS Lab Project · Submitted to Miss Nadia Shakir

---

<div align="center">

*Built with Python · SQL Server · OpenAI · Tkinter*

</div>
