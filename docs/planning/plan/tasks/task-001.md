# Task 001 — Decide Tech Stack & Project Structure

## Metadata
- **Epic:** EPIC-00 Foundation
- **Story:** S-00a
- **Owner:** Tech Lead
- **Status:** Done ✓

## Goal

Decide and document the tech stack for the entire project, and create the basic project structure.

## Files

- `AGENTS.md` — update section 3. Tech Stack
- `docs/planning/architecture/architecture.md` — update Tech Stack section
- `src/` or `apps/` — create skeleton structure

## Dependencies

None — first task

## Acceptance Criteria

- [x] Tech stack decided and written into `AGENTS.md` section 3 (Runtime, Framework, DB, Queue, Storage, CI)
- [x] ADR written into `AGENTS.md` section 10 Decision Log with rationale
- [x] Project structure created with directories: `src/` (or `apps/`), `tests/`, `scripts/`, `infra/`
- [x] `README.md` at root includes dev environment setup instructions
- [x] `.gitignore` covers the correct files per stack
- [x] Monorepo vs multi-repo decision clearly documented

## Tests Required

- Manual: verify project can be cloned and a `hello world` endpoint runs successfully

## Notes

Suggested tech stack based on NFRs:
- Backend: Python (FastAPI) or Node.js (NestJS) — both have good ecosystems for LLM + async
- DB: PostgreSQL + pgvector
- Queue: Redis Streams or BullMQ
- Storage: MinIO (local) / S3 (prod)
- Frontend: React + TypeScript
Final decision belongs to the Tech Lead.
