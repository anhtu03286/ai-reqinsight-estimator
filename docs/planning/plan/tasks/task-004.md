# Task 004 — Tenant Context Middleware

## Metadata
- **Epic:** EPIC-00 Foundation
- **Story:** S-00d
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement middleware that injects `organization_id` into every request and DB session, ensuring RLS operates automatically — no request can access cross-tenant data.

## Files

- `src/middleware/tenant.py`
- `tests/test_tenant_isolation.py`

## Dependencies

- Task 002 (RLS policies must exist)
- Task 003 (JWT must include `organization_id` in payload)

## Acceptance Criteria

- [x] Middleware runs after JWT auth, before the request reaches the service
- [x] Middleware reads `organization_id` from JWT payload
- [x] Every DB connection is set with `SET LOCAL app.current_org_id = '<org_id>'` before executing a query
- [x] Requests without JWT (public endpoints) do not trigger the middleware
- [x] Test: user from org-A cannot read data belonging to org-B even when knowing the UUID
- [x] Test: query without org context set → RLS blocks → 403 or empty result

## Tests Required

- Unit: middleware correctly extracts org_id from JWT
- Unit: DB helper correctly sets the session variable
- Integration: user from org-A attempts to access a project belonging to org-B → 404 (existence not revealed)
- Integration: cross-org document access → blocked

## Notes

- Return 404 instead of 403 for cross-tenant access to avoid revealing resource existence (security best practice)
- This is hard rule #9 in AGENTS.md — no exceptions
