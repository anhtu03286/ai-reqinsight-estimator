# Task 014 — Excel Export (4-Tab Quotation)

## Metadata
- **Epic:** EPIC-04 Estimation
- **Story:** S-19
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement Excel export that produces a professional 4-tab quotation file with fully dynamic formulas — no hardcoded values (BR-15, BR-16).

## Files

- `src/estimation/excel_export.py`
- `src/estimation/export_controller.py`
- `tests/test_excel_export.py`

## Dependencies

- Task 013 (WBS + Rate Card must exist)

## Acceptance Criteria

- [x] `POST /projects/:id/export/excel` returns an Excel file download
- [x] Excel file has exactly 4 tabs: Rate Card, WBS, Summary, Test Cases (BR-16)
- [x] **Tab Rate Card:** role, seniority, daily rate
- [x] **Tab WBS:** complete with columns Code, Module, Feature, Complexity, Effort (Dev/QA/BA/PM), Risk Buffer
- [x] **Tab Summary:** cost formula `=WBS.Effort * RateCard.DailyRate` — not hardcoded
- [x] **Tab Test Cases:** test cases from AnalysisResults where type=test_case
- [x] All calculated cells use formulas, not static values (BR-15, KL-P-002)
- [x] File contains no macros (`.xlsx`, not `.xlsm`)

## Tests Required

- Unit: verify Summary cost formula references the correct WBS + Rate Card cells
- Unit: Grand total uses `=SUM(...)` formula
- Integration: generate with 3 WBS items → verify formulas exist
- Manual QA: open the real Excel file, change a daily rate → total cost updates automatically

## Notes

- Library: openpyxl (Python)
- KL-P-002: every derived-value cell MUST be a formula, not a static number
