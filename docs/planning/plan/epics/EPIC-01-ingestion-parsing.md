# Epic 01 — Ingestion & Parsing

> Planner Agent output — `.ai-factory/agents/planner-agent.md`

## Objective

Users can upload a multi-format document set, the system processes it asynchronously and returns normalized content ready for AI analysis.

## Links

- PRD: Module Ingestion & Parsing (FR-01, FR-02, FR-03)
- Architecture: `ingestion-service`
- DB: `documents`, `document_chunks`

## Epic scope

Upload file → validate → OCR (if needed) → parse → semantic chunk → store encrypted → emit event

## User stories

| ID | Description | Priority |
|----|-------------|----------|
| S-01 | As a BA, I want to upload multiple files at once via drag-drop to submit a project document set | P0 |
| S-02 | As a system, I want automatic OCR of scanned PDFs to extract text for AI | P0 |
| S-03 | As a system, I want to chunk text by context to preserve semantic integrity | P0 |
| S-04 | As a BA, I want to see the processing status of each file to know when results are available | P1 |

## Epic completion criteria

- [ ] Multi-file upload working (PDF, DOCX, MD, TXT, XLSX, CSV ≤ 50MB)
- [ ] OCR processes scanned PDFs
- [ ] Chunks have sufficient metadata for deep-link citation
- [ ] Files encrypted with AES-256 at rest
- [ ] Event "document.parsed" emitted for AI Core to consume

## Dependencies & risks

- Dependency: Infra (Object Storage, Message Queue) must exist first
- Risk: OCR accuracy low for poor-quality scanned documents

## Milestone

Sprint 1-2
