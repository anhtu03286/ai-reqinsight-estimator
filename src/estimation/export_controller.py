import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.config import get_settings
from src.auth.rbac import require_permission, CurrentUser, Permission
from src.estimation.excel_export import export_quotation

router = APIRouter(prefix="/projects", tags=["export"])
settings = get_settings()


@router.get("/{project_id}/export/quotation")
async def export_excel(
    project_id: uuid.UUID,
    user: CurrentUser = Depends(require_permission(Permission.export_quotation)),
):
    engine = create_engine(settings.database_sync_url)
    with Session(engine) as db:
        excel_bytes = export_quotation(
            project_id=project_id,
            organization_id=uuid.UUID(user.organization_id),
            db=db,
        )
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=quotation-{project_id}.xlsx"},
    )
