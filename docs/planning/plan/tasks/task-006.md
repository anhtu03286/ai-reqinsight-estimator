# Task 006 — File Upload API & Validation

## Metadata
- **Epic:** EPIC-01 Ingestion & Parsing
- **Story:** S-01
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement `POST /projects/:id/documents` — accepts multi-file uploads, validates format/size, stores encrypted files in Object Storage, and creates Document records.

## Files

- `src/ingestion/upload_controller.py`
- `src/ingestion/upload_service.py`
- `src/ingestion/validators/file_validator.py`
- `tests/test_file_validator.py`

## Dependencies

- Task 003 (auth middleware)
- Task 004 (tenant middleware)
- Task 005 (Object Storage service)

## Acceptance Criteria

- [x] Accepts `multipart/form-data` with multiple files at once
- [x] Rejects files > 50MB → 400 `DOCUMENT_TOO_LARGE` (BR-01)
- [x] Rejects unsupported formats → 400 `UNSUPPORTED_FORMAT` (BR-02)
- [x] Accepted formats: PDF, DOCX, DOC, MD, TXT, XLSX, XLS, CSV (BR-02)
- [x] Saves file to Object Storage with AES-256 SSE
- [x] Creates a `Document` record in DB with `parse_status = 'pending'`
- [x] Returns 202 Accepted + `{documents: [...], job_ids: [...]}`
- [x] `GET /documents/:id/status` returns `{status, progress_pct}`

## Tests Required

- Unit: validator rejects file > 50MB
- Unit: validator rejects .exe, .zip
- Integration: upload a valid PDF → Document record created in DB → storage key exists
- Integration: upload 3 files simultaneously → 3 Document records created

## Notes

- Do not read file content in the controller — stream directly to storage
- job_id allows the client to poll parse status (next step in task-007)
