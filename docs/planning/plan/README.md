# Plan

Directory containing **Planner Agent output** (Agent 03).

| Directory | Contents |
|-----------|----------|
| `epics/` | Epics per milestone / deliverable value (e.g. `epics/EPIC-01-spa-booking.md`) |
| `stories/` | User stories linked to epics |
| `tasks/` | Small tasks for the Implement Agent (e.g. `tasks/task-001.md`) |

## Task Conventions

- Each task <= ~4 hours, single responsibility, independently testable
- Required format: Goal, Files, Dependencies, Acceptance Criteria, Tests Required — see [planner-agent.md](../.ai-factory/agents/planner-agent.md)
- Templates: [task-template.md](../.ai-factory/templates/task-template.md), [epic-template.md](../.ai-factory/templates/epic-template.md), [story-template.md](../.ai-factory/templates/story-template.md)

## Input

- `docs/planning/architecture/architecture.md` (+ files in `docs/planning/architecture/` and `docs/planning/product/prd.md` when needed)

Subdirectories are generated when the Planner Agent runs — the original template leaves them empty (README only).
