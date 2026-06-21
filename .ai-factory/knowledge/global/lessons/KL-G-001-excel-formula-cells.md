---
name: KL-G-001-excel-formula-cells
description: In Excel exports, cost/computed cells must use openpyxl formula strings (starting with "="), never pre-computed Python values. This is the global generalization of KL-P-002.
metadata:
  type: project
---

When generating Excel files with `openpyxl`, always write formula strings (e.g. `ws.cell(r, c, "=A2*B2")`) for any derived value. Never write a computed float directly.

**Why:** Formulas allow end-users to change input cells (rates, effort) and have downstream cells update automatically. Hardcoded values silently break this expectation and are a common source of presales errors.

**How to apply:** Identify all "derived" cells (totals, costs, subtotals, percentages). Trace back to their source cells and write the formula. Run the test `test_summary_sheet_uses_formulas_not_hardcoded` to verify.

Related: [[KL-P-002-excel-dynamic-formula]]
