# Task 009 — Semantic Chunking & Embedding

## Metadata
- **Epic:** EPIC-01 Ingestion & Parsing
- **Story:** S-03
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Split parsed text into context-aware chunks (preserving meaning), generate an embedding vector for each chunk, and store them in the DB — ready for AI analysis and semantic search.

## Files

- `src/ingestion/chunking/semantic_chunker.py`
- `src/ingestion/jobs/parse_job.py`
- `tests/test_chunker.py`

## Dependencies

- Task 005 (queue consumer)
- Task 007, Task 008 (parsed text output)

## Acceptance Criteria

- [x] Chunker receives parsed text and splits first by heading boundaries
- [x] Maximum chunk size ~500 tokens; sentences are never cut mid-way
- [x] Overlap between chunks: ~50 tokens to preserve context
- [x] Each chunk stores: `chunk_index`, `content`, `page_number`, `section_header`
- [x] Embedding service calls the AI Abstraction Layer to generate an embedding vector (1536 dim)
- [x] Embedding stored in `document_chunks.embedding` (pgvector)
- [x] Job consumer subscribes to the "document.parsed" event from the queue
- [x] Job emits "document.chunked" event after completion
- [x] `Document.parse_status = 'done'` after chunks + embeddings are complete

## Tests Required

- Unit: chunker does not produce empty chunks
- Unit: chunker does not cut a sentence mid-way
- Unit: overlap is the correct number of tokens
- Integration: end-to-end parse job → chunks in DB → embedding is not null

## Notes

- Embedding model: must match the model used for semantic matching in FR-12
- Use tiktoken for accurate token counting
