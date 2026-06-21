import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.db.session import get_db
from src.auth.rbac import get_current_user, CurrentUser, require_permission, Permission
from src.ingestion.upload_service import handle_upload
from src.queue.queue_service import get_job_status

router = APIRouter(prefix="/projects", tags=["ingestion"])


class UploadResponse(BaseModel):
    document_ids: list[str]
    job_ids: list[str]


@router.post("/{project_id}/documents", response_model=UploadResponse, status_code=202)
async def upload_documents(
    project_id: uuid.UUID,
    files: list[UploadFile] = File(...),
    version_label: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(require_permission(Permission.upload_document)),
):
    docs, job_ids = await handle_upload(
        project_id=project_id,
        organization_id=uuid.UUID(user.organization_id),
        user_id=uuid.UUID(user.user_id),
        files=files,
        version_label=version_label,
        db=db,
    )
    return UploadResponse(document_ids=[str(d.id) for d in docs], job_ids=job_ids)


@router.get("/documents/{document_id}/status")
async def get_document_status(document_id: str, job_id: str):
    return get_job_status(job_id)
