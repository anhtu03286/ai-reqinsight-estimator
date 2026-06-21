# Task 002 — Database Migrations Baseline

## Metadata
- **Epic:** EPIC-00 Foundation
- **Story:** S-00b
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Create all database migrations for every table defined in database-design.md, including RLS policies and indexes.

## Files

- `alembic/versions/V001_baseline.py` — single migration covering all tables

## Dependencies

- Task 001 (tech stack must be decided)

## Acceptance Criteria

- [x] All 10 tables created successfully from the migration
- [x] pgvector extension enabled (`CREATE EXTENSION IF NOT EXISTS vector`)
- [x] VECTOR(1536) column on `document_chunks.embedding`
- [x] All indexes defined in database-design.md are created
- [x] RLS enabled on `projects`, `documents`, `analysis_results`, `wbs_items`
- [x] RLS policy uses `current_setting('app.current_org_id')` for tenant isolation
- [x] Migration rollback (down script) exists for each file
- [x] Running `migrate up` from an empty DB succeeds without errors

## Tests Required

- Integration test: run migration against an empty PostgreSQL instance, verify schema via `information_schema`
- Integration test: RLS policy blocks queries without `app.current_org_id`
- Integration test: RLS policy allows queries when `app.current_org_id` is set correctly

## Notes

- Use Alembic (Python) per the tech stack decision in task-001
