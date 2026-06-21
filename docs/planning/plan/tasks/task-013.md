# Task 013 — WBS Generation & Rate Card

## Metadata
- **Epic:** EPIC-04 Estimation
- **Story:** S-17, S-18
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement Rate Card CRUD and WBS generation from Approved AnalysisResults — produces an Epic→Story→Task hierarchy with effort estimates and risk buffers.

## Files

- `src/estimation/wbs_service.py`
- `src/estimation/rate_card_service.py`
- `src/estimation/router.py`
- `src/estimation/jobs/wbs_job.py`

## Dependencies

- Task 010 (AI Abstraction Layer — WBS generation uses LLM)
- Task 012 (Approved items must exist)

## Acceptance Criteria

- [x] Rate Card CRUD: Create, Read, Update per API design
- [x] Rate Card includes at least these roles: dev, qa, ba, pm; seniority levels: junior, mid, senior
- [x] `POST /projects/:id/wbs/generate` only processes items with `status = 'approved'` (BR-20)
- [x] WBS generator calls LLM to decompose Approved items → Epic→Story→Task
- [x] Each WBS item has: `effort_dev_md`, `effort_qa_md`, `effort_ba_md`, `effort_pm_md`
- [x] Risk buffer % is derived from Gap/Risk severity level (BR-17): High → 30%, Medium → 15%, Low → 5%
- [x] WBS items saved to DB with correct parent_id hierarchy
- [x] `GET /projects/:id/wbs` returns tree structure

## Tests Required

- Unit: risk buffer calculation by severity
- Unit: WBS generator with mock LLM response → correct hierarchy
- Integration: generate from 5 Approved items → WBS items in DB
- Integration: Rate Card CRUD end-to-end

## Notes

- Effort is in Man-days (not hours)
- Task 001 decision: if `historical_ref` is available → record it in the WBS item (FR-12)
