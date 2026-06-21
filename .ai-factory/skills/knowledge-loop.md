# Skill — Knowledge Loop

Run this skill when: review **FAIL**, recurring bug, AC/architecture deviation, user requests to remember.

## Lesson writing checklist

1. [ ] Open `.ai-factory/knowledge/INDEX.md` — get next ID (`KL-G-NNN` or `KL-P-NNN`)
2. [ ] Copy `.ai-factory/templates/lesson-template.md`
3. [ ] Save to `global/lessons/` (all projects) or `project/lessons/` (domain-specific)
4. [ ] Fill in **Rules** as an actionable checklist
5. [ ] Add a row to INDEX
6. [ ] In `reviews/*.md` or task: write `Lesson: KL-…`

## Choosing a tier

| Global | Project |
|--------|---------|
| Stack, testing, security patterns | Project-specific entities/domains |
| Agent process errors | Domain-specific business rules |

## Promote

When a project lesson no longer depends on a domain → move to `global/`, update INDEX.

Full workflow: [knowledge-loop.md](../workflows/knowledge-loop.md).
