# Panel Admisiones — Universidad Indoamérica

Power BI project for admissions trend, progress, targets and projection analysis.

## Current implementation gates

1. Data quality and reconciliation before visual development.
2. Semantic model and business rules.
3. YTD B25 vs B26 using the same elapsed day inside each admissions period.
4. B26 projection based on elapsed days and observed run rate.
5. B26 institutional target: 2,400 admissions, allocated proportionally by career.
6. Missing campus target values remain 0, preserving the source Excel rule.
7. Visual layer and storytelling only after quality gates pass.

## Repository structure

- `docs/` — scope, business rules, data dictionary and validation criteria.
- `data-quality/` — reconciliation and quality rules.
- `dax/` — documented measure specifications.
- `PanelAdmisiones.Report/` — Power BI report project artifacts.
- `PanelAdmisiones.SemanticModel/` — semantic model artifacts.

> Source data must be validated before measures and visuals are considered final.
