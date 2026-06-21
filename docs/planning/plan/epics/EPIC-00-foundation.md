# Epic 00 — Foundation & Infrastructure

> Planner Agent output — `.ai-factory/agents/planner-agent.md`

## Objective

Establish the technical foundation (project structure, DB, auth, infra) before business epics begin.

## Links

- Architecture: `api-gateway`, `shared`, database design
- DB: migrations baseline
- Security: JWT, RBAC, encryption setup

## Epic scope

Project setup → DB migrations → Auth (JWT + RBAC) → Multi-tenant middleware → Object Storage + Message Queue setup → CI baseline

## User stories

| ID | Description | Priority |
|----|-------------|----------|
| S-00a | As a team, we want a standard project structure to start development | P0 |
| S-00b | As a system, I want a DB migrations baseline so that all entities exist | P0 |
| S-00c | As a system, I want JWT auth + RBAC to protect every endpoint | P0 |
| S-00d | As a system, I want tenant context middleware to ensure data isolation | P0 |

## Epic completion criteria

- [ ] Monorepo or multi-repo structure decided and set up
- [ ] DB migrations runnable (all tables from database-design.md)
- [ ] API Gateway with JWT auth + RBAC working
- [ ] Tenant middleware injects `organization_id` into every request
- [ ] Object Storage config (local dev + prod)
- [ ] Message Queue config (local dev + prod)
- [ ] Basic CI pipeline (lint + test + build)

## Dependencies & risks

- Dependency: Tech stack decision (TBD — must be decided before sprint 1)
- Risk: Unselected tech stack may block the entire epic

## Milestone

Sprint 1 (must complete before all other epics)
