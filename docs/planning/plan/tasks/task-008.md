# Task 008 — Document Parser (Excel, CSV) & OCR Engine

## Metadata
- **Epic:** EPIC-01 Ingestion & Parsing
- **Story:** S-02
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement parsers for structured files (XLSX, CSV) and an OCR pipeline for scanned PDFs that have no text layer.

## Files

- `src/ingestion/parsers/excel_parser.py`
- `src/ingestion/parsers/csv_parser.py`
- `src/ingestion/ocr/ocr_adapter.py`
- `src/ingestion/ocr/tesseract_ocr.py`

## Dependencies

- Task 007 (parser factory + standardized output format)

## Acceptance Criteria

- [x] Excel parser: reads each sheet, converts tables to structured text (headers + rows)
- [x] Excel parser: preserves sheet names as section headers
- [x] CSV parser: auto-detects delimiter (comma, semicolon, tab)
- [x] OCR service: receives PDFs flagged `needs_ocr: true` from task-007
- [x] OCR service: extracts text and returns the same output format as pdf_parser
- [x] OCR service uses adapter pattern — easy to swap provider (Tesseract / AWS Textract / Azure DI)
- [x] Updates `Document.ocr_applied = true` after OCR completes

## Tests Required

- Unit: Excel parser with a multi-sheet .xlsx fixture
- Unit: CSV parser with comma and semicolon delimiters
- Unit: OCR adapter mock — verify interface is correct
- Integration: scanned PDF → OCR → text output is not empty

## Notes

- Initial OCR provider: Tesseract (free, local) — sufficient for MVP
- Upgrade to AWS Textract if accuracy falls short after UAT
- Excel with formulas: read values only, do not evaluate formulas
