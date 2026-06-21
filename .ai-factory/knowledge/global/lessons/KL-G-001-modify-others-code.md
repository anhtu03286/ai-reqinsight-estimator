# [KL-G-001] — Modifying code outside task scope / code just pulled

> **Tier:** global  
> **Date:** 2026-06-18  
> **Source:** missing guardrail — agent modified others' code after `git pull`  
> **Tags:** `agent-behavior`, `git`, `scope`, `risk`

## Problem

After `pull` / rebase / merge, the agent sees new code from teammates and makes unsolicited edits (formatting, refactoring, minor fixes) even though they are not part of the current task — causing noisy diffs, PR conflicts, and regressions that are hard to trace.

## Root cause

- The old rule only said "do not modify unrelated files" but did not require a documented **reason**, **impact scope measurement**, or **risk assessment**
- The agent did not distinguish between "newly pulled" code and "code belonging to the current task"
- Missing checklist before touching any file outside **Files** in the task

## Rules (must apply going forward)

- [ ] Only modify files listed in the **Files** section of `docs/planning/plan/tasks/task-XXX.md`
- [ ] Newly pulled code: **read to integrate**, do not casually refactor / reformat
- [ ] Any modification outside **Files** is mandatory → document **Reason** (1–3 sentences, specific)
- [ ] Before modifying: identify **impact scope** — list files, symbols, number of call sites / usages
- [ ] Document **risk assessment** Low / Medium / High + consequences + mitigation
- [ ] Risk **High** → stop, notify user / create a separate task; do not commit in the current PR
- [ ] PR must have an **Out-of-scope changes** section when there are changes outside **Files**
- [ ] Reviewer FAIL if the 3 items above are missing or the modification was unnecessary

## Anti-pattern → Correct pattern

| Avoid | Do instead |
|-------|-----------|
| After pull, see messy code → fix it immediately | Only modify the parts required by the task; other issues → separate task/PR |
| Fix a shared helper "just to be safe" | Count call sites; document risk; test the affected area |
| No explanation in PR | Out-of-scope section: Reason + Scope + Risk |
| Guess the impact | `grep` / impact tool / test before committing |

## Checks before merge / task close

- [ ] Diff only touches **Files** of the task, or has a complete Out-of-scope changes section
- [ ] Tests have been run for the affected area (if out-of-scope)
- [ ] Reviewer has confirmed the risk is acceptable

## Links

- Hard rule: `AGENTS.md` section 8
- Protocol: `.ai-factory/agents/implement-agent.md` — Out-of-scope change protocol
- Session: `.ai-factory/skills/session-protocol.md`
