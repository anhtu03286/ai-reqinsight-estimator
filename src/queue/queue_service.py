import json
from redis import Redis
from rq import Queue
from src.config import get_settings

settings = get_settings()

_redis_conn: Redis | None = None
_queues: dict[str, Queue] = {}


def get_redis() -> Redis:
    global _redis_conn
    if _redis_conn is None:
        _redis_conn = Redis.from_url(settings.redis_url)
    return _redis_conn


def get_queue(name: str = "default") -> Queue:
    if name not in _queues:
        _queues[name] = Queue(name, connection=get_redis(), default_timeout=600)
    return _queues[name]


def enqueue_job(func, *args, queue_name: str = "default", job_timeout: int = 600, **kwargs) -> str:
    queue = get_queue(queue_name)
    job = queue.enqueue(func, *args, job_timeout=job_timeout, **kwargs)
    return job.id


def get_job_status(job_id: str) -> dict:
    from rq.job import Job
    try:
        job = Job.fetch(job_id, connection=get_redis())
        return {
            "job_id": job_id,
            "status": job.get_status().value,
            "progress_pct": job.meta.get("progress_pct", 0),
            "result": job.result if job.is_finished else None,
            "error": str(job.exc_info) if job.is_failed else None,
        }
    except Exception:
        return {"job_id": job_id, "status": "not_found"}
