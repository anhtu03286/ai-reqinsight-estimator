# [KL-P-001] — Tenant isolation must return 404 not 403

> **Tier:** project
> **Date:** 2026-06-21
> **Source:** Architect phase — security design decision
> **Tags:** `security`, `multi-tenant`, `api`

## Problem

When a user attempts to access a resource belonging to another organization (cross-tenant), returning 403 FORBIDDEN inadvertently confirms that the resource exists — an attacker can enumerate UUIDs.

## Root cause

403 carries the semantics "you know it exists but do not have permission." 404 carries the semantics "does not exist (for you)" — no information is leaked.

## Rules (must apply going forward)

- [ ] Cross-tenant access → always return 404, never 403
- [ ] Tenant middleware checks `organization_id` before querying the DB
- [ ] RLS policy at the DB layer is the last line of defense — do not rely solely on application code

## Anti-pattern → Correct pattern

| Avoid | Do instead |
|-------|-----------|
| `if (resource.org_id != user.org_id) return 403` | Query DB with `WHERE org_id = $user_org_id` → if not found → natural 404 |
| Check permissions after fetching a cross-tenant resource | RLS filter at the DB — resources from another org are never fetched |

## Checks before merge / task close

- [ ] Test: user from org-A sends UUID belonging to org-B → receives 404
- [ ] Test: RLS policy active — query without org context → empty result

## Links

- Task: `docs/planning/plan/tasks/task-004.md`
- Business rules: BR-21, BR-24
