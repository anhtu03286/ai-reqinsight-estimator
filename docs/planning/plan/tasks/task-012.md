# Task 012 — Approval Workflow API

## Metadata
- **Epic:** EPIC-03 Collaboration
- **Story:** S-12
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement the Approval/Rejection API for AnalysisResults — enforcing role-based permissions (BR-12) and storing an audit history.

## Files

- `src/collaboration/router.py`
- `src/collaboration/approval_service.py`

## Dependencies

- Task 003 (RBAC middleware)
- Task 011 (AnalysisResults must exist)

## Acceptance Criteria

- [x] `POST /analysis/:id/approve` — only roles with permission per BR-12 may approve
- [x] `POST /analysis/:id/reject` — a `comment` is required
- [x] Approving an already Approved/Rejected item → 409 `ALREADY_APPROVED` (BR-11 — not reversible)
- [x] Each action creates an `ApprovalRecord` with `user_id`, `action`, `comment`, `timestamp`
- [x] `GET /analysis/:id/history` returns the full ApprovalRecord list
- [x] `POST /projects/:id/bulk-approve` approves multiple items at once — skips already Approved/Rejected items, returns `{approved: n, failed: n}`
- [x] AnalysisResult `status` is updated correctly after each action

## Tests Required

- Unit: BA approves a technical Risk → 403 (BR-12)
- Unit: PM approves a Clarification → 200
- Unit: approve an already Approved item → 409
- Integration: approve → status in DB = 'approved'
- Integration: reject without a comment → 400

## Notes

- Per BR-11: only Admin can override Approved/Rejected if necessary (must be explicitly recorded in the audit log)
