# AI ReqInsight & Estimator

AI-powered platform for analyzing software requirement documents and automating project quotations.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| Docker & Docker Compose | Latest |
| Tesseract OCR | 5.x (optional, for scanned PDFs) |

---

## Quick Start

### 1. Clone & create environment file

```bash
cp .env.example .env
```

Edit `.env` and fill in required values — at minimum:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/reqinsight
DATABASE_SYNC_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/reqinsight
ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Start infrastructure services

```bash
docker compose -f docker-compose.dev.yml up -d
```

This starts:
- PostgreSQL 15 with pgvector at `localhost:5432`
- Redis 7 at `localhost:6379`
- MinIO at `localhost:9000` (console: `localhost:9001`)

### 3. Install Python dependencies

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the API server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: `http://localhost:8000/docs`

### 6. Start the RQ worker (in a separate terminal)

```bash
rq worker default --url $REDIS_URL
```

---

## Project Structure

```
src/
├── main.py                  # FastAPI app entry point
├── config.py                # Settings (pydantic-settings)
├── models/                  # SQLAlchemy ORM models
├── db/                      # Async session factory
├── auth/                    # JWT + RBAC
├── middleware/              # Tenant isolation middleware
├── ingestion/               # File upload, parsers, OCR, chunking
├── ai/                      # LLM provider interface + Claude implementation
├── ai_core/                 # Analysis pipeline, chatbot, prompts
├── collaboration/           # Approval workflow
├── estimation/              # WBS generation, rate card, Excel export
├── integration/             # Jira / Linear / ClickUp sync
├── storage/                 # MinIO/S3 storage service
└── queue/                   # RQ job queue

tests/                       # pytest test suite
docs/planning/               # Product, architecture, plan artefacts
.ai-factory/                 # AI Factory framework (agents, knowledge, templates)
alembic/                     # Database migrations
```

---

## Generating a Quotation Report

There are two ways to produce the Excel quotation file depending on whether you have infrastructure set up.

---

### Way 1 — Standalone Script (no API key, no Docker)

Best for: quick demo, offline use, or when you want to run an analysis that has already been pre-processed by Claude.

**Requirements:** Python 3.11+ and `openpyxl` only.

```bash
# Install the single dependency
pip install openpyxl

# Run the script
python scripts/generate_report.py
```

Output is written to:

```
reports/ReqInsight_Quotation_Report.xlsx
```

The script contains Claude's analysis of `docs/specs/requirement.md` already embedded — no API call is made at runtime. The Excel file has 6 tabs:

| Tab | Content |
|-----|---------|
| Cover & Summary | Project overview, cost breakdown per Epic |
| Analysis Results | 21 findings: Clarification / Risk / Gap / Suggestion |
| Test Cases | 12 test scenarios with priority and acceptance criteria |
| WBS & Effort | 35 WBS items (Epic / Story / Task) with man-day estimates |
| Rate Card & Cost | Configurable daily rates; all cost cells use Excel formulas |
| Assumptions & Exclusions | 8 assumptions + 9 out-of-scope items |

To recalculate costs, open the file and change the **Daily Rate** values in the Rate Card tab — all totals update automatically.

---

### Way 2 — Full Platform via REST API (requires API key + Docker)

Best for: production use, processing custom documents, multi-tenant environments.

**Requirements:** Docker, Anthropic API key (Enterprise tier recommended — see NFR-04).

**Step 1 — Start infrastructure**

```bash
cp .env.example .env
# Fill in ANTHROPIC_API_KEY, SECRET_KEY, JWT_SECRET in .env

docker compose -f docker-compose.dev.yml up -d
```

**Step 2 — Start the application**

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload --port 8000
# In a second terminal:
rq worker default --url redis://localhost:6379
```

**Step 3 — Authenticate**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "changeme"}'
# → {"access_token": "eyJ...", "refresh_token": "..."}
```

**Step 4 — Upload a requirement document**

```bash
curl -X POST http://localhost:8000/projects/{project_id}/documents \
  -H "Authorization: Bearer {access_token}" \
  -F "file=@docs/specs/requirement.md"
# → {"job_id": "...", "status": "queued"}
```

**Step 5 — Poll until analysis is complete**

```bash
curl http://localhost:8000/documents/{document_id}/status \
  -H "Authorization: Bearer {access_token}"
# → {"status": "done"}
```

**Step 6 — Download the Excel quotation**

```bash
curl -OJ http://localhost:8000/projects/{project_id}/export/quotation \
  -H "Authorization: Bearer {access_token}"
# Saves: quotation_{project_id}.xlsx
```

Interactive API docs (Swagger UI): `http://localhost:8000/docs`

---

## Core Workflow

```
Upload document → Parse & OCR → Chunk & Embed
    → AI Analysis → Review & Approve
    → Generate WBS → Compute Cost
    → Export Excel Quotation → Sync to PM Tool
```

---

## Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Get access + refresh tokens |
| POST | `/projects/{id}/documents` | Upload requirement documents |
| GET | `/projects/{id}/analysis` | Get AI analysis results |
| POST | `/analysis/{id}/approve` | Approve / reject a result |
| POST | `/projects/{id}/wbs/generate` | Generate WBS from approved results |
| GET | `/projects/{id}/estimation/cost` | Compute total cost |
| GET | `/projects/{id}/export/quotation` | Download Excel quotation |
| POST | `/projects/{id}/sync/pm` | Sync WBS to Jira / Linear / ClickUp |

---

## Running Tests

```bash
pytest
```

---

## LLM Provider

Default provider is **Claude** (`LLM_PROVIDER=claude`). Set `ANTHROPIC_API_KEY` in `.env`.

To switch providers, set `LLM_PROVIDER=azure_openai` and fill in `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT`.

---

## Continuing Development

This project follows the **AI Factory** framework. Before starting a new session:

1. Read `CLAUDE.md` — bootstrap checklist
2. Read `.ai-factory/knowledge/INDEX.md` — apply relevant lessons
3. Read the relevant agent file in `.ai-factory/agents/`

Specification: `docs/specs/requirement.md`
