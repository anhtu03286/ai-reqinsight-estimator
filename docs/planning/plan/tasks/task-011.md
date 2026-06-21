# Task 011 — AI Analysis Pipeline (Core)

## Metadata
- **Epic:** EPIC-02 AI Core
- **Story:** S-06
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement the document analysis pipeline — receives chunks, calls the LLM, and produces 5 types of AnalysisResult (clarification, risk, gap, suggestion, test_case) with deep-link citations.

## Files

- `src/ai_core/analysis_service.py`
- `src/ai_core/prompts/analysis_prompt.py`
- `src/ai_core/jobs/analysis_job.py`
- `src/ai_core/router.py`

## Dependencies

- Task 009 (chunks + embeddings must exist)
- Task 010 (AI Abstraction Layer)

## Acceptance Criteria

- [x] Job consumer receives the "document.chunked" event
- [x] Pipeline loads chunks from DB, batches them, and sends to LLM
- [x] LLM response is parsed into `AnalysisResult[]` with the correct types
- [x] Each result has a `chunk_id` (deep-link citation — BR-10)
- [x] Risk/Gap items have a `severity` (high/medium/low — BR-06)
- [x] All results saved with `status = 'pending'`
- [x] Results stored in DB with `organization_id`, `project_id`
- [x] Job emits "analysis.completed" event after finishing
- [x] Analysis of < 50 pages completes in ≤ 2 minutes (NFR-01) — benchmark required
- [x] Do not log prompt/response content (log metadata only)

## Tests Required

- Unit: result-parser with mock LLM response → correct count and types
- Unit: severity mapping from LLM output → enum
- Unit: missing chunk_id → result-parser throws error
- Integration: end-to-end with mock LLM → AnalysisResults in DB
- Performance: 50-page document (fixture) → ≤ 120s

## Notes

- Prompt template must instruct the LLM to return structured JSON for the result-parser to work reliably
- Batch chunks within the LLM's context window (do not exceed context limit)
