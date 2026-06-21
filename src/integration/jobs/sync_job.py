"""RQ job: sync WBS items to external PM tool."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.config import get_settings
from src.integration.sync_service import sync_to_pm

settings = get_settings()


def run_sync_job(project_id: str, organization_id: str, tool: str, project_key: str) -> dict:
    engine = create_engine(settings.database_sync_url)
    with Session(engine) as db:
        return sync_to_pm(
            project_id=uuid.UUID(project_id),
            organization_id=uuid.UUID(organization_id),
            tool=tool,
            project_key=project_key,
            db=db,
        )
