# Initial DAX Measure Catalog

Measures are specifications until the validated table and column names are confirmed.

## Base
- `Admisiones` — valid admissions at the agreed business grain.
- `Meta` — target in current filter context.
- `% Cumplimiento` — Admisiones / Meta.
- `Gap Meta` — Meta - Admisiones.

## Period progress
- `Dia Transcurrido Periodo` — ordinal elapsed day in selected admissions period.
- `Dias Periodo` — total valid days in period.
- `Dias Restantes` — Dias Periodo - Dia Transcurrido Periodo.
- `% Tiempo Transcurrido` — Dia Transcurrido Periodo / Dias Periodo.

## YTD comparable
- `Admisiones YTD` — admissions through current elapsed period day.
- `Admisiones YTD Periodo Anterior` — prior comparison period through the same elapsed day.
- `Variacion YTD` — current YTD - comparable prior YTD.
- `% Variacion YTD` — Variacion YTD / comparable prior YTD.

## Projection
- `Ritmo Diario Actual` — current admissions YTD / elapsed days.
- `Ritmo Diario Requerido` — remaining target / remaining days.
- `Proyeccion Cierre` — projection using elapsed-day run rate.
- `Gap Proyectado` — Meta - Proyeccion Cierre.
- `% Proyeccion Meta` — Proyeccion Cierre / Meta.

## Status
- `Estado Proyeccion` — target reached / on track / at risk according to agreed thresholds.

Exact DAX is implemented after the data-quality gate confirms source schema, grain, period boundaries and target tables.