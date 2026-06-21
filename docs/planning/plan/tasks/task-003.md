# Task 003 — JWT Auth & RBAC Middleware

## Metadata
- **Epic:** EPIC-00 Foundation
- **Story:** S-00c
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement JWT authentication and RBAC middleware at the API Gateway layer — every protected endpoint is automatically secured.

## Files

- `src/auth/jwt.py`
- `src/auth/rbac.py`
- `src/auth/router.py`
- `tests/test_jwt.py`
- `tests/test_rbac.py`

## Dependencies

- Task 001 (tech stack)
- Task 002 (users table must exist)

## Acceptance Criteria

- [x] `POST /auth/login` returns `access_token` (15 minutes) + `refresh_token` (7 days)
- [x] `POST /auth/refresh` issues a new `access_token` from a valid refresh token
- [x] Request missing token → 401 UNAUTHORIZED
- [x] Request with expired token → 401 UNAUTHORIZED
- [x] Request with valid token but wrong role → 403 FORBIDDEN
- [x] JWT payload contains: `user_id`, `organization_id`, `role`
- [x] RBAC middleware reads `role` from JWT, compares against permission map, blocks if insufficient permissions
- [x] Permission map accurately reflects the permission table in `business-rules.md` section 4

## Tests Required

- Unit: JWT sign and verify (valid, expired, tampered)
- Unit: RBAC permission matrix — each role vs each action
- Integration: login → use token → access protected endpoint
- Integration: expired token → refresh → access again

## Notes

- Do not store JWT secret in code — use env var `JWT_SECRET`
- Refresh token stored in DB (table or Redis) to allow revocation
