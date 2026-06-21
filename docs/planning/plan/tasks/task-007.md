# Task 007 — Document Parser (PDF, DOCX, MD, TXT)

## Metadata
- **Epic:** EPIC-01 Ingestion & Parsing
- **Story:** S-02
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement a parser pipeline that processes text-based files (PDF with text layer, DOCX, MD, TXT) — extracts plain text with structural metadata (heading, page number).

## Files

- `src/ingestion/parsers/pdf_parser.py`
- `src/ingestion/parsers/docx_parser.py`
- `src/ingestion/parsers/markdown_parser.py`
- `src/ingestion/parsers/text_parser.py`
- `src/ingestion/parsers/parser_factory.py`
- `tests/test_parsers.py`

## Dependencies

- Task 005 (download file from storage)
- Task 006 (Document record must exist)

## Acceptance Criteria

- [x] `ParserFactory.getParser(format)` returns the correct parser
- [x] PDF parser: extracts text + page numbers, detects if no text layer is present (→ flag as needing OCR)
- [x] DOCX parser: extracts text while preserving heading structure (H1, H2, H3)
- [x] MD parser: extracts text while preserving heading structure
- [x] TXT parser: extracts text line by line
- [x] Standardized output: `{pages: [{page: number, text: string, headings: string[]}]}`
- [x] Updates `Document.parse_status = 'processing'` on start, `'done'` on success, `'failed'` on error

## Tests Required

- Unit: each parser with a fixture file (sample PDF, DOCX, MD, TXT)
- Unit: PDF with no text layer → `needs_ocr: true`
- Unit: DOCX with heading structure → headings are preserved
- Integration: download from storage → parse → verify text output is not empty

## Notes

- Libraries used: pdfplumber (Python), python-docx (DOCX)
- Excel/CSV parsing is not in this task — see task-008
