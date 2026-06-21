import uuid
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.document import Document, DocumentFormat, ParseStatus
from src.storage.storage_service import upload_file
from src.queue.queue_service import enqueue_job
from src.ingestion.validators.file_validator import validate_file, validate_file_size
import io


async def handle_upload(
    project_id: uuid.UUID,
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    files: list[UploadFile],
    version_label: str | None,
    db: AsyncSession,
) -> tuple[list[Document], list[str]]:
    documents = []
    job_ids = []

    for file in files:
        ext = validate_file(file)
        content = await validate_file_size(file)

        storage_key = f"{organization_id}/{project_id}/{uuid.uuid4()}.{ext}"
        upload_file(io.BytesIO(content), storage_key, file.content_type or "application/octet-stream")

        doc = Document(
            organization_id=organization_id,
            project_id=project_id,
            filename=file.filename,
            format=DocumentFormat(ext),
            storage_key=storage_key,
            version_label=version_label,
            file_size_bytes=len(content),
            uploaded_by=user_id,
            parse_status=ParseStatus.pending,
        )
        db.add(doc)
        await db.flush()

        from src.ingestion.jobs.parse_job import run_parse_job
        job_id = enqueue_job(run_parse_job, str(doc.id), str(organization_id))
        job_ids.append(job_id)
        documents.append(doc)

    await db.commit()
    return documents, job_ids
