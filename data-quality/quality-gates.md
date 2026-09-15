# Data Quality Gates

## Gate 1 — Schema
- Required admissions date exists and is parseable.
- Period is populated and normalized.
- Campus and career dimensions are populated or explicitly classified.
- Admission identifier is suitable for the agreed counting grain.

## Gate 2 — Duplicates
- Detect duplicate admission identifiers.
- Quantify duplicate rows before applying any removal rule.
- Never silently deduplicate source data.

## Gate 3 — Dates and periods
- Every admission date maps to exactly one admissions period.
- B25 and B26 have explicit start/end dates.
- Elapsed-day comparison never exceeds the valid duration of either period.

## Gate 4 — Targets
- B26 institutional career targets reconcile to 2,400 after proportional allocation.
- Campus targets reconcile to source Excel values.
- Missing campus target = 0.

## Gate 5 — Reconciliation
- Source row count is documented.
- Valid admissions total is documented.
- Totals by period, campus and career reconcile with source controls.
- Exceptions are listed before the semantic model is approved.

## Exit criterion
All critical gates must pass before final DAX and visual development.