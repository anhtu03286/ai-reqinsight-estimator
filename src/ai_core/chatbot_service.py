import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.chunk import DocumentChunk
from src.ai.ai_factory import get_llm_provider


def chat_with_document(
    project_id: uuid.UUID,
    organization_id: uuid.UUID,
    db: Session,
    question: str,
    history: list[dict],
) -> str:
    provider = get_llm_provider()
    embedding = provider.embed(question)

    # Semantic search: cosine similarity via pgvector
    chunks = db.execute(
        select(DocumentChunk).where(
            DocumentChunk.organization_id == organization_id,
        ).order_by(
            # pgvector cosine distance operator
            DocumentChunk.embedding.cosine_distance(embedding)
        ).limit(10)
    ).scalars().all()

    context = "\n\n---\n\n".join(c.content for c in chunks)

    messages = list(history)
    messages.append({
        "role": "user",
        "content": f"Context from requirements document:\n{context}\n\nQuestion: {question}",
    })

    response = provider.chat(messages)

    # Append citation references
    refs = []
    for c in chunks[:3]:
        if c.section_header:
            refs.append(f"[{c.section_header}, p.{c.page_number}]")
    if refs:
        response += "\n\n_Sources: " + ", ".join(refs) + "_"

    return response
