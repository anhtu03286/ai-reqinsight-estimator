import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from src.models.analysis_result import AnalysisResult, ApprovalStatus, ResultType
from src.models.approval_record import ApprovalRecord, ApprovalAction
from src.models.user import UserRole
from src.auth.rbac import CurrentUser, Permission, ROLE_PERMISSIONS

# Which roles can approve which result types
APPROVAL_AUTHORITY: dict[ResultType, set[UserRole]] = {
    ResultType.clarification: {UserRole.ba, UserRole.pm, UserRole.admin},
    ResultType.risk: {UserRole.pm, UserRole.tech_lead, UserRole.admin},
    ResultType.gap: {UserRole.ba, UserRole.pm, UserRole.admin},
    ResultType.suggestion: {UserRole.pm, UserRole.ba, UserRole.tech_lead, UserRole.admin},
    ResultType.test_case: {UserRole.qa, UserRole.ba, UserRole.admin},
}


async def approve_result(
    result_id: uuid.UUID,
    action: ApprovalAction,
    comment: str | None,
    user: CurrentUser,
    db: AsyncSession,
) -> AnalysisResult:
    result = await db.execute(
        select(AnalysisResult).where(
            AnalysisResult.id == result_id,
            AnalysisResult.organization_id == uuid.UUID(user.organization_id),
        )
    )
    ar = result.scalar_one_or_none()
    if not ar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")

    if ar.status != ApprovalStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Result is already {ar.status.value}",
        )

    allowed_roles = APPROVAL_AUTHORITY.get(ar.result_type, set())
    if UserRole(user.role) not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")

    record = ApprovalRecord(
        analysis_result_id=ar.id,
        user_id=uuid.UUID(user.user_id),
        organization_id=uuid.UUID(user.organization_id),
        action=action,
        comment=comment,
    )
    db.add(record)

    ar.status = ApprovalStatus.approved if action == ApprovalAction.approved else ApprovalStatus.rejected
    await db.commit()
    await db.refresh(ar)
    return ar


async def edit_result(
    result_id: uuid.UUID,
    new_content: str,
    user: CurrentUser,
    db: AsyncSession,
) -> AnalysisResult:
    result = await db.execute(
        select(AnalysisResult).where(
            AnalysisResult.id == result_id,
            AnalysisResult.organization_id == uuid.UUID(user.organization_id),
        )
    )
    ar = result.scalar_one_or_none()
    if not ar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")

    if not ROLE_PERMISSIONS.get(UserRole(user.role), set()).intersection(
        {Permission.edit_analysis}
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")

    ar.original_content = ar.original_content or ar.content  # preserve first original
    ar.content = new_content
    ar.edited_by = uuid.UUID(user.user_id)
    ar.edited_at = datetime.now(timezone.utc)
    ar.status = ApprovalStatus.pending  # reset to pending after edit

    await db.commit()
    await db.refresh(ar)
    return ar
