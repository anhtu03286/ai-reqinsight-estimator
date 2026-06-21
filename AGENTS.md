# AGENTS.md

Reference document for humans and agents (AI) working in this repo. **Update when the project changes**.

---

## 1. Project Context

| Item | Content |
|------|---------|
| **Name / purpose** | **AI ReqInsight & Estimator** — AI platform for analyzing software requirements documents and automating project estimation |
| **Primary users** | BA, PM, Presales, Tech Lead, QA/QC within software companies |
| **MVP scope** | 4 modules: Ingestion & Parsing · AI Core & Delta Analysis · Collaboration & Review · Estimation & Integration |
| **Product documents** | PRD and artefacts in `docs/planning/product/`: see `.ai-factory/agents/product-agent.md` (output: `docs/planning/product/prd.md`, `docs/planning/product/business-rules.md`, `docs/planning/product/success-metrics.md`) |

**Constraints / assumptions:**
- LLM must be Private or Enterprise API — do not use customer data as training data (NFR-04)
- Each organization is an independent tenant; absolute data isolation
- Input files max 50MB/file; asynchronous processing (async)
- Original specification: `docs/specs/requirement.md` (SRS v1.1.0)

---

## 2. Architecture

| Item | Content |
|------|---------|
| **System type** | Microservices with AI abstraction layer — LLM pluggable (Claude / GPT / Gemini) per NFR-06 |
| **Main boundaries** | 4 bounded contexts: `ingestion` · `ai-core` · `collaboration` · `estimation` |
| **Data flow** | Upload (async) → Parse → AI Analyze → Review/Approve → Export (Excel / PM Tools) |
| **Architecture documents** | `docs/planning/architecture/` — `architecture.md`, `module-map.md`, `database-design.md`, `api-design.md` (per `.ai-factory/agents/architect-agent.md`) |

**Diagrams / links:** TBD (after Architect Agent)

---

## 3. Tech Stack

| Layer | Technology |
|-------|-----------|
| **Runtime / language** | Python 3.11+ |
| **Framework** | FastAPI (async) + SQLAlchemy 2.0 async |
| **Database** | PostgreSQL 15 + pgvector (vector search) |
| **Migration** | Alembic |
| **AI / LLM** | Pluggable via abstraction layer — Claude Enterprise (default), Azure OpenAI (stub) |
| **OCR** | pytesseract (MVP) — swappable via adapter |
| **Cache / queue** | Redis + rq (job queue) |
| **Storage** | MinIO (dev) / AWS S3 (prod) via boto3 |
| **Document parsing** | pdfplumber, python-docx, openpyxl, pandas |
| **Excel export** | openpyxl (dynamic formulas) |
| **Testing** | pytest + pytest-asyncio + httpx |
| **Deployment** | Docker Compose (dev); container-based (prod TBD) |
| **CI** | GitHub Actions (TBD) |

Pinned versions: `requirements.txt` at root

---

## 4. Coding Standards

- **Formatting & lint:** TBD — Architect decides per stack
- **Naming:** TBD — convention for files, variables, API endpoints
- **Directory structure:** see section **7. Folder Conventions**
- **Error handling:** TBD — when to throw, when to return Result, logging
- **Comments:** Only explain non-obvious logic; avoid comments that repeat the code
- **i18n:** System handles language automatically, prioritizing English and Vietnamese

---

## 5. Hard Rules

**Mandatory** rules — agents must not violate unless the maintainer explicitly agrees.

1. **Do not commit secrets** — do not include `.env`, API keys, tokens in git; use secret manager / local environment variables.
2. **Do not modify outside task scope** — Implement Agent: only files related to task / AC (per `.ai-factory/agents/implement-agent.md`).
3. **Do not change architecture / PRD in code** — if deviation detected → write issue / PR comment, no silent large refactors.
4. **Do not disable hooks / skip tests** to merge — unless repo rules allow a different process.
5. **Backward compatibility:** TBD — mandatory migration or breaking OK with version bump.
6. **Bootstrap each session** — Read `AGENT-BOOTSTRAP.md` + `.ai-factory/knowledge/INDEX.md` (or run `scripts/bootstrap-context.ps1` / `.sh`) before starting.
7. **Write lesson after issue** — Review FAIL / recurring bug: skill `.ai-factory/skills/knowledge-loop.md`; write `Lesson: KL-…` in review; do not end session when a recurring issue lacks a lesson.
8. **Modifying code outside the task** (including code just pulled / rebased / merged from others) — Implement Agent **only** modifies files listed under **Files** in the task. If **absolutely required** to modify outside that list, must write in PR / task before committing:
   - **Reason** — why the task cannot be completed without touching that code
   - **Scope of Impact** — number of files / symbols / call sites affected
   - **Risk Assessment** — level Low / Medium / High + potential consequences and mitigation
   - Do not refactor, format, or "clean up" other people's code outside the task scope. Details: lesson `KL-G-001`, [implement-agent.md](.ai-factory/agents/implement-agent.md).
9. **Data isolation** — Documents and estimation data for each organization must be absolutely isolated. No cross-tenant queries; do not use customer data as input training for public LLMs (NFR-04).
10. **Mandatory encryption** — All stored documents must be encrypted with AES-256; transmission must use TLS 1.3. Do not store plain-text documents in DB or object store (NFR-03).
11. **LLM vendor contract** — Before integrating any LLM provider, confirm the contract has a clause "do not store prompts / do not use data for training". Clearly record the confirmed provider in the Decision Log.

---

## 6. Workflow

| Step | Role | Artefact / action |
|------|------|-------------------|
| 1 | Product | `docs/planning/product/prd.md`, `docs/planning/product/business-rules.md`, `docs/planning/product/success-metrics.md` |
| 2 | Architect | `docs/planning/architecture/architecture.md`, `docs/planning/architecture/module-map.md`, `docs/planning/architecture/database-design.md`, `docs/planning/architecture/api-design.md` |
| 3 | Planner | `docs/planning/plan/epics/`, `docs/planning/plan/stories/`, `docs/planning/plan/tasks/` — task ≤ ~4h, single responsibility |
| 4 | Implement | One `docs/planning/plan/tasks/task-XXX.md` → code + tests + minimal docs |
| 5 | Reviewer | PR → `docs/planning/reviews/review.md` — **PASS** or **FAIL** with reasons |
| — | Knowledge loop | Issue → `.ai-factory/knowledge/` — see `knowledge-loop.md` |

**Git / PR:** TBD — branch, squash, minimum number of reviewers

**Agent details:** `.ai-factory/agents/*.md`

---

## 7. Folder Conventions

| Path | Purpose |
|------|---------|
| `.ai-factory/` | Agent definitions, templates, skills, knowledge, workflows (meta) |
| `docs/specs/` | Original specification documents (SRS, stakeholder input) — **do not modify after baseline** |
| `docs/planning/` | AI Factory pipeline output (product, architecture, plan, reviews) |
| `docs/planning/product/` | Product Agent output: PRD, business rules, success metrics |
| `docs/planning/architecture/` | Architect Agent output: architecture, module map, DB, API |
| `docs/planning/plan/` | Planner Agent output: `epics/`, `stories/`, `tasks/` |
| `docs/planning/reviews/` | Reviewer Agent output: PR review results |
| `.ai-factory/knowledge/` | Lesson memory: `global/` (all projects), `project/` (project-specific), `INDEX.md` |
| `src/` | TBD — runtime code (Architect decides structure) |
| `tests/` | TBD — unified convention after stack selection |

Task file naming convention: `docs/planning/plan/tasks/task-001.md`, …

---

## 8. Testing Rules

- **Mandatory:** Every behavioral change with AC must have a corresponding test or a documented reason for refusing to test (written in PR).
- **Test types:** TBD — unit / integration / e2e; tools per stack
- **Run before PR:** TBD — full command
- **Coverage:** TBD — threshold or "do not decrease coverage on touched modules"
- **Test data:** fixture / factory — do not use real customer documents

---

## 9. Security Rules

- **AuthN / AuthZ:** RBAC — user bound to organization; can only view assigned projects (NFR-05). Check permissions at API layer.
- **Input validation:** Validate at API boundary; parameterized queries — no raw string SQL concatenation.
- **Encryption:** AES-256 at-rest for documents and estimates; TLS 1.3 in-transit (NFR-03).
- **Data isolation:** Per-organization — no cross-tenant query; do not use customer data as training data (NFR-04).
- **Secrets:** Only through environment variables / vault; rotate when exposed.
- **Dependencies:** TBD — audit schedule and CVE review.
- **LLM:** Mandatory Private LLM or Enterprise API with commitment to not store prompts (NFR-04).
- **Logging:** Do not log customer document content, PII, tokens, full sensitive payloads.

---

## 10. Decision Log

| Date | Decision | Context | Consequence |
|------|----------|---------|-------------|
| 2026-06-21 | Microservices + AI abstraction layer | NFR-06 requires LLM pluggable between Claude/GPT/Gemini | Need abstraction API layer between business logic and LLM; each module deploys independently |
| 2026-06-21 | Private LLM / Enterprise API only | NFR-04 prohibits using customer data as training data | Must choose provider with data privacy commitment; confirm contract before integrating |
| 2026-06-21 | Python + FastAPI as backend | Best AI/ML ecosystem; async native; rich document processing libraries | SQLAlchemy 2.0 async + asyncpg for PostgreSQL; rq + Redis for job queue |
| 2026-06-21 | Alembic for DB migration | Good integration with SQLAlchemy; supports Python and SQL migration | Convention: `VYYY_MM_DD_HHMMSS_description.py` |

---

## Appendix: Quick Links

- Original specification: `docs/specs/requirement.md`
- Bootstrap (all agents): `AGENT-BOOTSTRAP.md`
- Scripts: `scripts/bootstrap-context.ps1`, `scripts/verify-knowledge-loop.ps1`
- Agents: `.ai-factory/agents/`
- Templates: `.ai-factory/templates/`
- Product artefacts: `docs/planning/product/`
- Architecture artefacts: `docs/planning/architecture/`
- Plan (epic / story / task): `docs/planning/plan/`
- Reviews: `docs/planning/reviews/`
- Knowledge (read before working): `.ai-factory/knowledge/INDEX.md`
- Knowledge loop: `.ai-factory/workflows/knowledge-loop.md`
