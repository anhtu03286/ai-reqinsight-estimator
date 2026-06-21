"""RQ job: trigger AI analysis after document parsing is complete."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from src.config import get_settings
from src.models.document import Document
from src.models.project import Project
from src.ai_core.analysis_service import run_analysis

settings = get_settings()


def run_analysis_job(document_id: str, organization_id: str) -> dict:
    engine = create_engine(settings.database_sync_url)
    with Session(engine) as db:
        doc = db.execute(
            select(Document).where(Document.id == uuid.UUID(document_id))
        ).scalar_one_or_none()

        if not doc:
            return {"error": "document not found"}

        results = run_analysis(
            document_id=doc.id,
            project_id=doc.project_id,
            organization_id=uuid.UUID(organization_id),
            db=db,
        )
        return {"status": "done", "result_count": len(results)}
