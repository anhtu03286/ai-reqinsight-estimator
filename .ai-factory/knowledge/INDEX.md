# Knowledge Index

Agent **must read this file** before implementing, reviewing, or planning a new task.

## Global lessons (all projects)

| ID | Title | Tags | One-line summary |
|----|-------|------|-----------------|
| KL-G-001 | Modifying code outside scope / after pull | `agent-behavior`, `git`, `scope`, `risk` | Must document Reason + Impact Scope + Risk before modifying code not belonging to the current task |
| KL-G-001b | Excel export must use all dynamic formulas | `estimation`, `integration` | Do not hardcode numbers into Excel cells — always use reference formulas (global generalization of KL-P-002) |
| KL-G-002 | Update task file after implementation is complete | `agent-behavior`, `scope`, `review` | Implement Agent must change Status → Done ✓ and tick `- [x]` immediately after completing a task |

## Project lessons (this project)

| ID | Title | Tags | One-line summary |
|----|-------|------|-----------------|
| KL-P-001 | Tenant isolation must return 404 not 403 | `security`, `multi-tenant`, `api` | Cross-tenant requests return 404 to avoid revealing resource existence — 403 confirms the resource exists |
| KL-P-002 | Excel export must use all dynamic formulas | `estimation`, `integration` | Do not hardcode numbers into Excel cells — always use reference formulas so that totals update automatically when the Rate Card changes |
| KL-P-003 | RQ worker must use sync SQLAlchemy Session | `database`, `architecture`, `error-handling` | RQ jobs run in a separate process with no event loop — use `Session(create_engine(...))` sync, do not use `AsyncSession` |

## How to add

1. Create a file from [lesson-template.md](../templates/lesson-template.md)
2. Place it in `global/lessons/` or `project/lessons/`
3. Add one row to the table above
4. Only use tags from the **Tag Taxonomy** list below

## Promote project → global

When a lesson **does not depend on the project domain** → move it to `global/lessons/`, update INDEX, delete or add a redirect note in the project version.

---

## Tag Taxonomy

Only use tags from this list. Need a new tag → add it here first with a reason.

### Process & Agent behavior

| Tag | Use when |
|-----|----------|
| `agent-behavior` | How an agent should / should not behave |
| `scope` | Task scope management, out-of-scope changes |
| `review` | Review process, reviewer checklist |
| `planning` | Task breakdown, estimation, planner anti-patterns |
| `knowledge` | Lesson writing / reading process |

### Engineering

| Tag | Use when |
|-----|----------|
| `git` | Git workflow, branch, commit, rebase, pull |
| `testing` | Writing tests, coverage, test strategy |
| `security` | AuthN/AuthZ, secrets, injection, safe logging |
| `performance` | Hot path, N+1, caching, payload |
| `database` | Schema, migration, index, query |
| `api` | API contract, versioning, error response |
| `architecture` | Architecture decisions, coupling, bounded context |
| `error-handling` | Error handling, retry, fallback |
| `logging` | Observability, tracing, log format |

### Risk & Change management

| Tag | Use when |
|-----|----------|
| `risk` | Risk assessment, potential consequences |
| `breaking-change` | Changes that break existing contract / API / schema |
| `migration` | Data migration, code migration, backward compatibility |

### Domain (AI ReqInsight & Estimator)

| Tag | Use when |
|-----|----------|
| `document-processing` | OCR, parsing, chunking, file ingestion pipeline |
| `ai-analysis` | LLM prompting, analysis pipeline, delta analysis, semantic matching |
| `estimation` | WBS, effort, rate card, quotation, risk buffer calculation |
| `collaboration` | Approval workflow, multi-role review, RBAC, interactive editing |
| `integration` | PM tools (Jira/Linear/ClickUp), Excel export, API sync |
| `multi-tenant` | Data isolation, per-org scoping, tenant context |
