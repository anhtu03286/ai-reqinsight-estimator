import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.session import get_db
from src.auth.rbac import get_current_user, CurrentUser, require_permission, Permission
from src.models.analysis_result import AnalysisResult, ApprovalStatus

router = APIRouter(prefix="/projects", tags=["analysis"])


class AnalysisResultOut(BaseModel):
    id: str
    result_type: str
    severity: str | None
    title: str
    content: str
    status: str
    persona: str | None

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str
    history: list[dict] = []


@router.get("/{project_id}/analysis", response_model=list[AnalysisResultOut])
async def get_analysis_results(
    project_id: uuid.UUID,
    result_type: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(require_permission(Permission.view_analysis)),
):
    query = select(AnalysisResult).where(
        AnalysisResult.project_id == project_id,
        AnalysisResult.organization_id == uuid.UUID(user.organization_id),
    )
    if result_type:
        query = query.where(AnalysisResult.result_type == result_type)
    if status:
        query = query.where(AnalysisResult.status == status)

    results = await db.execute(query)
    return results.scalars().all()


@router.post("/{project_id}/chat")
async def chat(
    project_id: uuid.UUID,
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(require_permission(Permission.view_analysis)),
):
    # Sync wrapper for chatbot (RQ worker approach for heavy ops)
    from src.ai_core.chatbot_service import chat_with_document
    # Note: chatbot_service uses sync Session; wrap with run_in_executor in production
    raise HTTPException(status_code=501, detail="Use async chat endpoint via websocket")
