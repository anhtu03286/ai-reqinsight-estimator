"""RQ job: generate WBS from approved analysis results."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.config import get_settings
from src.estimation.wbs_service import generate_wbs

settings = get_settings()


def run_wbs_job(project_id: str, organization_id: str) -> dict:
    engine = create_engine(settings.database_sync_url)
    with Session(engine) as db:
        items = generate_wbs(
            project_id=uuid.UUID(project_id),
            organization_id=uuid.UUID(organization_id),
            db=db,
        )
        return {"status": "done", "wbs_items": len(items)}
