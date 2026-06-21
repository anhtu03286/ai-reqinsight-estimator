import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.auth.rbac import require_permission, CurrentUser, Permission
from src.config import get_settings
from src.queue.queue_service import enqueue_job

router = APIRouter(prefix="/projects", tags=["integration"])
settings = get_settings()


class SyncRequest(BaseModel):
    tool: str  # jira | linear | clickup
    project_key: str


@router.post("/{project_id}/sync/pm")
async def sync_pm(
    project_id: uuid.UUID,
    body: SyncRequest,
    user: CurrentUser = Depends(require_permission(Permission.sync_pm_tools)),
):
    from src.integration.jobs.sync_job import run_sync_job
    job_id = enqueue_job(run_sync_job, str(project_id), user.organization_id, body.tool, body.project_key)
    return {"job_id": job_id}
