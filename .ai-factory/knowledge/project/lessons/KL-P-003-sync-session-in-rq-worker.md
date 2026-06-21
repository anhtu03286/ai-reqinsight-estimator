---
name: KL-P-003-sync-session-in-rq-worker
description: RQ workers must use synchronous SQLAlchemy sessions (not async), because RQ runs in a separate forked process without an async event loop.
metadata:
  type: project
---

RQ workers (`run_in_background=True` via `enqueue_job`) are executed in a plain synchronous Python process. Using `AsyncSession` / `await db.execute(...)` inside an RQ job raises `RuntimeError: no running event loop`.

**Pattern**: always create a fresh sync `Session` via `create_engine(settings.database_sync_url)` at the start of each job. Never import the FastAPI async session or use `asyncio.run()` inside an RQ job.

**Why:** RQ forks a worker process per job. There is no asyncio event loop in that context.

**How to apply:** Any function decorated or called via `enqueue_job()` must be fully synchronous. If you need async logic, run it with `asyncio.run()` wrapped in a try/except, or restructure to sync.

See: `src/ingestion/jobs/parse_job.py`, `src/estimation/jobs/wbs_job.py`
