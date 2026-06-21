# CLAUDE.md — AI ReqInsight & Estimator

> AI platform for analyzing software requirements documents and automating project estimation.
> Original specification: `docs/specs/requirement.md` (SRS v1.1.0)

## Mandatory Bootstrap (each session)

Before doing anything, perform in order:

1. Read `AGENTS.md` — hard rules, project conventions
2. Read `.ai-factory/knowledge/INDEX.md` — apply lessons with relevant tags
3. Read `.ai-factory/skills/session-protocol.md` — session checklist
4. Identify the agent role for the current task, read the corresponding agent file in `.ai-factory/agents/`

Details: `AGENT-BOOTSTRAP.md`

---

## Agent Roles

| Role | Definition File | When |
|------|-----------------|------|
| Product | `.ai-factory/agents/product-agent.md` | Creating PRD / business documents |
| Architect | `.ai-factory/agents/architect-agent.md` | Designing architecture from PRD |
| Planner | `.ai-factory/agents/planner-agent.md` | Breaking epic → story → task |
| Implement | `.ai-factory/agents/implement-agent.md` | Coding exactly one task |
| Reviewer | `.ai-factory/agents/reviewer-agent.md` | Reviewing PR → PASS / FAIL |

---

## Artefact Flow

```
docs/planning/product/   ← Product Agent output
docs/planning/architecture/  ← Architect Agent output
docs/planning/plan/      ← Planner Agent output (epics/, stories/, tasks/)
docs/planning/reviews/   ← Reviewer Agent output
.ai-factory/knowledge/   ← Knowledge base (read before, write after issue)
```

---

## Hard Rules Summary

- **Do not commit secrets** (.env, API key, token)
- **Implement Agent**: only modify files listed under **Files** in the task — violations must document Reason + Scope of Impact + Risk (see KL-G-001)
- **After review FAIL / recurring bug**: run skill `.ai-factory/skills/knowledge-loop.md`, create lesson, update INDEX
- **Do not end the session** when there is a recurring issue without a lesson

Full rules: `AGENTS.md` section 5.

---

## Knowledge Loop

When encountering an issue (review FAIL, recurring bug, user requests to remember):

1. Open `.ai-factory/knowledge/INDEX.md` → get the next ID
2. Copy `.ai-factory/templates/lesson-template.md` → `global/` or `project/lessons/`
3. Fill in Problem, Root Cause, Checklist Rules
4. Add a row to INDEX
5. Write `Lesson: KL-…` in the review or task

Details: `.ai-factory/workflows/knowledge-loop.md`

---

## Templates

All skeleton templates are located at `.ai-factory/templates/`:

| Template | Used for |
|----------|----------|
| `prd-template.md` | PRD |
| `business-rules-template.md` | Business rules |
| `success-metrics-template.md` | Success metrics |
| `architecture-template.md` | Overall architecture |
| `module-map-template.md` | Module map |
| `database-design-template.md` | Database design |
| `api-design-template.md` | API design |
| `epic-template.md` | Epic |
| `story-template.md` | User story |
| `task-template.md` | Task (Planner → Implement) |
| `review-template.md` | Review (Reviewer Agent) |
| `lesson-template.md` | Knowledge lesson |
