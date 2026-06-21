# [KL-P-002] — Excel export must use all dynamic formulas

> **Tier:** project
> **Date:** 2026-06-21
> **Source:** BR-15 design decision — estimation module
> **Tags:** `estimation`, `integration`

## Problem

If numbers are hardcoded into Excel cells on export, when the user changes the Rate Card the total cost does not update automatically — the file must be exported again. This breaks the value of the "dynamic quotation" feature.

## Root cause

The code generator fills cells with pre-computed values instead of Excel formulas — easier to implement but incorrect from a business standpoint.

## Rules (must apply going forward)

- [ ] All computed cells in Excel must be formulas (`=`, `SUM`, `PRODUCT`…)
- [ ] Tab 3 (Rate Card) contains the base values; Tab 2 references Tab 3
- [ ] Tab 1 (Dashboard) references totals from Tab 2 and Tab 3
- [ ] Do not use `cell.value = computed_number` — use `cell.value = "=Tab2!C2*Tab3!D5"`
- [ ] Manual QA: change the daily rate in Tab 3 → verify Tab 1 total updates

## Anti-pattern → Correct pattern

| Avoid | Do instead |
|-------|-----------|
| `cell.value = effort * daily_rate` | `cell.value = f"=B{row}*RateCard!C{rate_row}"` |
| Compute totals in Python and write to cell | `cell.value = f"=SUM(E2:E{last_row})"` |

## Checks before merge / task close

- [ ] Open the Excel file in real Excel/LibreOffice
- [ ] Change one daily rate → total cost updates automatically
- [ ] No cell has a static value in a computed position

## Links

- Task: `docs/planning/plan/tasks/task-014.md`
- Business rules: BR-15, BR-16
