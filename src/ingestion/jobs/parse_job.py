"""RQ job: parse document, chunk, embed, emit event."""
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from src.config import get_settings
from src.models.document import Document, ParseStatus, DocumentFormat
from src.models.chunk import DocumentChunk
from src.storage.storage_service import download_file
from src.ingestion.parsers.parser_factory import get_parser
from src.ingestion.ocr.tesseract_ocr import ocr_pdf
from src.ingestion.chunking.semantic_chunker import chunk_document
from src.ai.ai_factory import get_llm_provider
import uuid

settings = get_settings()


def run_parse_job(document_id: str, organization_id: str) -> dict:
    """Synchronous entry point for RQ worker."""
    engine = create_engine(settings.database_sync_url)

    with Session(engine) as db:
        doc = db.execute(
            select(Document).where(Document.id == uuid.UUID(document_id))
        ).scalar_one_or_none()

        if not doc:
            return {"error": "document not found"}

        doc.parse_status = ParseStatus.processing
        db.commit()

        try:
            content = download_file(doc.storage_key)
            parser = get_parser(doc.format.value)
            result = parser.parse(content)

            if result.needs_ocr and doc.format == DocumentFormat.pdf:
                ocr_text = ocr_pdf(content)
                from src.ingestion.parsers.base import ParsedPage
                result.pages = [ParsedPage(page=1, text=ocr_text, headings=[])]
                doc.ocr_applied = True

            pages_data = [{"page": p.page, "text": p.text, "headings": p.headings} for p in result.pages]
            raw_chunks = chunk_document(pages_data)

            provider = get_llm_provider()
            db_chunks = []
            for ch in raw_chunks:
                embedding = provider.embed(ch.content)
                db_chunk = DocumentChunk(
                    document_id=doc.id,
                    organization_id=uuid.UUID(organization_id),
                    chunk_index=ch.chunk_index,
                    content=ch.content,
                    page_number=ch.page_number,
                    section_header=ch.section_header,
                    embedding=embedding,
                )
                db_chunks.append(db_chunk)

            db.add_all(db_chunks)
            doc.parse_status = ParseStatus.done
            doc.language = result.detected_language
            db.commit()

            # Trigger AI analysis
            from src.ai_core.jobs.analysis_job import run_analysis_job
            from src.queue.queue_service import enqueue_job
            enqueue_job(run_analysis_job, document_id, organization_id)

            return {"status": "done", "chunks": len(db_chunks)}

        except Exception as e:
            doc.parse_status = ParseStatus.failed
            db.commit()
            raise
