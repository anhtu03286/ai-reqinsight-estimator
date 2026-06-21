---
name: KL-G-002-update-task-status-after-implement
description: Implement Agent must update the task file (Status + checkboxes) immediately after completion — do not leave the file in Todo state when the code is already done.
metadata:
  type: feedback
---

After implementing a task, the Implement Agent **must** update the file `docs/planning/plan/tasks/task-XXX.md`:

1. `**Status:** Todo` → `**Status:** Done ✓`
2. All `- [ ]` in Acceptance Criteria → `- [x]`

**Why:** Task files are the sole tracking artifact for the pipeline. If not updated, readers cannot distinguish completed tasks from pending ones — the entire value of the framework is lost.

**How to apply:** After each task is complete (code written, tests passing), update the corresponding task file IMMEDIATELY before moving on to the next task. This is the mandatory final step of every task, not optional.

Related: [[session-protocol]], [[implement-agent]]
