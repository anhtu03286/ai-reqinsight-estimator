import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.analysis_result import AnalysisResult, ResultType, Severity, ApprovalStatus
from src.models.chunk import DocumentChunk
from src.ai.ai_factory import get_llm_provider
from src.ai_core.prompts.analysis_prompt import build_analysis_prompt


def _severity(raw: str) -> Severity:
    try:
        return Severity(raw.lower())
    except ValueError:
        return Severity.medium


def _result_type(raw: str) -> ResultType:
    try:
        return ResultType(raw.lower())
    except ValueError:
        return ResultType.clarification


def run_analysis(
    document_id: uuid.UUID,
    project_id: uuid.UUID,
    organization_id: uuid.UUID,
    db: Session,
    persona: str | None = None,
) -> list[AnalysisResult]:
    chunks = db.execute(
        select(DocumentChunk).where(
            DocumentChunk.document_id == document_id,
            DocumentChunk.organization_id == organization_id,
        ).order_by(DocumentChunk.chunk_index)
    ).scalars().all()

    if not chunks:
        return []

    provider = get_llm_provider()
    prompt = build_analysis_prompt(persona)
    context_texts = [c.content for c in chunks]
    response = provider.analyze(prompt, context_texts)

    results = []
    for item in response.results:
        ar = AnalysisResult(
            organization_id=organization_id,
            project_id=project_id,
            document_id=document_id,
            result_type=_result_type(item.get("type", "clarification")),
            severity=_severity(item.get("severity", "medium")),
            title=item.get("title", "Untitled")[:500],
            content=item.get("content", ""),
            ai_version=response.model_version,
            status=ApprovalStatus.pending,
            persona=persona,
        )
        db.add(ar)
        results.append(ar)

    db.commit()
    return results
