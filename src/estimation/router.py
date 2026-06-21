import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.db.session import get_db
from src.auth.rbac import get_current_user, CurrentUser, require_permission, Permission
from src.estimation.rate_card_service import compute_cost

router = APIRouter(prefix="/projects", tags=["estimation"])


class CostResponse(BaseModel):
    currency: str
    total: float
    breakdown: list[dict]


@router.get("/{project_id}/estimation/cost", response_model=CostResponse)
async def get_cost_estimate(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(require_permission(Permission.export_quotation)),
):
    return await compute_cost(project_id, uuid.UUID(user.organization_id), db)


@router.post("/{project_id}/wbs/generate", status_code=202)
async def trigger_wbs_generation(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(require_permission(Permission.export_quotation)),
):
    from src.queue.queue_service import enqueue_job
    from src.estimation.jobs.wbs_job import run_wbs_job
    job_id = enqueue_job(run_wbs_job, str(project_id), user.organization_id)
    return {"job_id": job_id}
