# Agent Bootstrap (all platforms)

**Mandatory entry point** for all agents: Cursor, Claude Code, Ollama, custom API, etc.

Memory = **files in the repo**, not chat. Agents **must not skip** the steps below.

---

## 0. Each session / each new task

1. Read `AGENTS.md` (hard rules).
2. Read `.ai-factory/knowledge/INDEX.md` — apply relevant lessons.
3. Read session skill: [.ai-factory/skills/session-protocol.md](.ai-factory/skills/session-protocol.md).
4. Read **one** agent file matching the current role (`.ai-factory/agents/*.md`).

## 1. Before implement / review / plan

- Scan INDEX: open lessons with tags matching stack or task.
- Do not code/review without reading potentially relevant lessons.

## 2. After an issue (FAIL review, recurring bug, user says "remember")

**In the same session**, before ending:

1. Run skill [.ai-factory/skills/knowledge-loop.md](.ai-factory/skills/knowledge-loop.md).
2. Create lesson + update `INDEX.md`.
3. Write in review/task: `Lesson: KL-G-NNN` or `KL-P-NNN`.

Detailed workflow: [.ai-factory/workflows/knowledge-loop.md](.ai-factory/workflows/knowledge-loop.md).

## 3. End of project (operator)

Run sync script (no AI dependency):

```powershell
.\scripts\sync-knowledge-to-master.ps1 -MasterPath "D:\path\to\AgentV1"
```

---

## One-line prompt (paste into any agent)

```
Follow AGENT-BOOTSTRAP.md: read AGENTS.md + knowledge/INDEX.md before starting; after FAIL/issue write lesson per knowledge-loop; do not end session when missing a lesson for a recurring issue.
```

## Context gathering script (CLI / Ollama / API)

```powershell
.\scripts\bootstrap-context.ps1
```

Prints a text block — paste as system prompt or first message.
