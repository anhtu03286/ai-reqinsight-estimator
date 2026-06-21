# Knowledge

**File-based memory** for agents — independent of chat sessions. Agents **read before working**, **write after learning**.

## Two tiers

| Tier | Path | Scope | Portable to other projects |
|------|------|-------|---------------------------|
| **Global** | `global/lessons/` | Lessons applicable to all projects (stack, process, common agent mistakes) | Yes — lives in template, synced to **AgentV1 master** |
| **Project** | `project/lessons/` | Domain / stack specific to this project | Only when copied from an old repo or promoted to global |

**Index:** read [INDEX.md](INDEX.md) before every implement / review / plan session.

## Structure

```
knowledge/
├── INDEX.md                 # Lookup table — update whenever a lesson is added
├── global/
│   └── lessons/             # KL-G-001-*.md
└── project/
    └── lessons/             # KL-P-001-*.md
```

## Process

See [knowledge-loop.md](../workflows/knowledge-loop.md).

## Other content (project-specific)

- `project/glossary.md` — domain terminology
- `project/adr/` — ADRs for this project only
- Short decisions: section **10. Decision Log** in `AGENTS.md`
