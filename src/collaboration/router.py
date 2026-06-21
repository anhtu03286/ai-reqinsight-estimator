import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.auth.rbac import get_current_user, CurrentUser
from src.models.approval_record import ApprovalAction
from src.collaboration.approval_service import approve_result, edit_result

router = APIRouter(prefix="/analysis", tags=["collaboration"])


class ApproveRequest(BaseModel):
    action: ApprovalAction
    comment: str | None = None


class EditRequest(BaseModel):
    content: str


class AnalysisResultOut(BaseModel):
    id: str
    result_type: str
    severity: str | None
    title: str
    content: str
    status: str
    edited_by: str | None

    class Config:
        from_attributes = True


@router.post("/{result_id}/approve", response_model=AnalysisResultOut)
async def approve(
    result_id: uuid.UUID,
    body: ApproveRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    ar = await approve_result(result_id, body.action, body.comment, user, db)
    return AnalysisResultOut(
        id=str(ar.id),
        result_type=ar.result_type.value,
        severity=ar.severity.value if ar.severity else None,
        title=ar.title,
        content=ar.content,
        status=ar.status.value,
        edited_by=str(ar.edited_by) if ar.edited_by else None,
    )


@router.patch("/{result_id}", response_model=AnalysisResultOut)
async def edit(
    result_id: uuid.UUID,
    body: EditRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    ar = await edit_result(result_id, body.content, user, db)
    return AnalysisResultOut(
        id=str(ar.id),
        result_type=ar.result_type.value,
        severity=ar.severity.value if ar.severity else None,
        title=ar.title,
        content=ar.content,
        status=ar.status.value,
        edited_by=str(ar.edited_by) if ar.edited_by else None,
    )
