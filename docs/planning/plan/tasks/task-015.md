# Task 015 — PM Tools Sync (Jira / Linear / ClickUp)

## Metadata
- **Epic:** EPIC-04 Estimation
- **Story:** S-20
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement one-click WBS sync to Jira, Linear, and ClickUp — idempotent, syncs only Approved items (BR-25, BR-26).

## Files

- `src/integration/router.py`
- `src/integration/sync_service.py`
- `src/integration/pm_adapter.py`
- `src/integration/jira_adapter.py`
- `src/integration/linear_adapter.py`
- `src/integration/clickup_adapter.py`
- `src/integration/jobs/sync_job.py`

## Dependencies

- Task 013 (WBS must exist)

## Acceptance Criteria

- [x] `POST /projects/:id/sync/pm` — accepts `tool` (jira/linear/clickup) + `project_key`
- [x] Jira adapter: creates issues via REST API v3
- [x] Linear adapter: creates issues via GraphQL API
- [x] ClickUp adapter: creates tasks via REST API v2
- [x] Syncs only WBS items (BR-25)
- [x] Idempotent: checks whether item already exists before creating (BR-26)
- [x] Response: `{synced: n, updated: n, errors: [...]}`
- [x] Adapter pattern: `PMToolAdapter` interface with `push_tasks()`
- [x] OAuth credentials stored per-organization, not shared across orgs

## Tests Required

- Unit: sync with mock adapter — verify only WBS items are sent
- Unit: idempotent — call sync twice → create only happens on the first call
- Integration (mock API): Jira adapter creates an issue with the correct fields
- Unit: OAuth token does not leak to another org

## Notes

- Jira, Linear, and ClickUp all provide sandbox/test environments for testing
- OAuth refresh token is automatically refreshed when expired
- If external API rate-limits → retry with backoff, do not fail the entire sync
