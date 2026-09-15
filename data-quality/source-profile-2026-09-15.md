# Source Profile — 2026-09-15

## 615.xlsx
- Sheet `reporte`: 1,942 data rows, 30 columns.
- Periods: B26 1,929; A26 11; B25 2.
- Campuses: MATRIZ 1,466; QUITO 410; LATACUNGA 66.
- `HOMOLOGA`: NO 1,703; SI 239.
- `MATRICULA EN PRIMERO`: SI 1,366; NO 576.
- `FORMALIZADO`: SI 1,248; NO 694.
- Identification is populated in all rows; 25 identifiers are duplicated once.
- Registration dates range 2023-12-01 to 2026-09-15.
- Matriculation dates exist for 1,366 rows and range 2026-04-02 to 2026-09-15.

### Candidate B26 admissions grain
Using `PERIODO=B26`, `HOMOLOGA=NO`, and `MATRICULA EN PRIMERO=SI` produces 1,351 rows: MATRIZ 1,013; QUITO 286; LATACUNGA 52. Of these, 1,240 are `FORMALIZADO=SI` and 111 are `FORMALIZADO=NO`. This is a candidate rule only until business reconciliation confirms whether formalization is required.

## Datoshistoricob25.xlsx
- `Hoja2`: 1,879 rows, all B25 and all `1RO NIVEL`.
- Campuses: MATRIZ 1,352; QUITO 434; LATACUNGA 93.
- `FORMALIZADA`: SI 1,859; NO 20.
- `RET.CARRERA`: NO for all 1,879 rows.
- No blank or duplicate primary identifiers detected in Hoja2.
- Matriculation dates range 2025-06-23 to 2025-12-02.

## Metas.xlsx
- 115 populated target records after the header.
- Institutional `GENERAL` target is 2,400.
- Career-level rows with `MODALIDAD=GENERAL` currently sum to 2,500 across 35 careers.
- Therefore career targets require proportional reconciliation to the official 2,400 target before use in the semantic model.

## Quality findings requiring model treatment
1. `615.xlsx` contains periods other than B26 and must be filtered deliberately.
2. `615.xlsx` has 25 duplicate identification keys; no silent deduplication is allowed.
3. Historical B25 is clean at identifier grain in `Hoja2`.
4. Current and historical career names are not fully canonicalized (for example accents and engineering naming variants); a career mapping dimension is required.
5. Current source includes postgraduate career names while the target workbook is primarily career-target structured; target coverage must be classified explicitly.
6. Career GENERAL targets sum to 2,500, while the approved institutional B26 target is 2,400; proportional factor = 0.96 before rounding/remainder allocation.
7. Same-day B25/B26 comparison must use an elapsed-period-day key rather than calendar date.

## Gate status
Data-quality gate is **IN PROGRESS**. Schema profiling passed. Target reconciliation and canonical dimension mapping remain before final DAX/visual acceptance.