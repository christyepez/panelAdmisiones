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
- Current configured period is May 1 through September 30 for B25 and B26.
- Out-of-period rows remain auditable and are excluded from period KPIs.

## Gate 4 — Targets
- B26 institutional career targets reconcile to 2,400 after proportional allocation.
- Campus targets reconcile to source Excel values.
- Missing campus target = 0.

## Gate 5 — Reconciliation
- Source row count is documented.
- Valid admissions total is documented.
- Totals by period, campus and career reconcile with source controls.
- Exceptions are listed before the semantic model is approved.

## Gate 6 — Comparable universe
- Career target coverage is explicit.
- Institutional attainment excludes programs without a B26 career target.
- Mixed graduate/postgraduate totals never use the institutional target denominator.

## Validated snapshot — 2026-09-15
- Candidate B26 rows before date window: 1,351.
- B26 rows mapped to the 35 target careers: 1,304; programs without target: 47.
- Historical B25 rows before date window: 1,879.
- B25 rows mapped to target careers: 1,589; programs without target: 290.
- Within May 1–September 15, comparable B26 YTD is 1,293 and B25 same-day YTD is 1,069.
- Within May 1–September 30, comparable B25 final is 1,355.
- Career targets reconcile from 2,500 source units to exactly 2,400 adjusted units.
- 25 identifiers repeat in the complete B26 source; rows remain preserved pending a business rule.
- 74 of 79 detail target rows have no identifiable campus and are not distributed by assumption.

## Exit criterion
The navigable panel passes schema, target reconciliation, date-window and comparable-universe controls. Duplicate treatment and campus target allocation remain open business exceptions for Power BI finalization.
