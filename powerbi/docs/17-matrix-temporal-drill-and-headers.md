# Matrix temporal drill and header styling

This revision keeps the validated report measures intact and isolates temporal drill behavior inside the comparison Matrix.

## Rows

`Carrera -> Sede -> Modalidad -> Mes -> Día`

## Columns

- 2025: TOTAL, YTD, REAL, Δ%
- 2026: BUDGET, YTD, REAL, REAL %, Δ BUDGET, COMPLETION, REAL VS LY, VARIANZA

## Temporal behavior

- At Carrera/Sede/Modalidad level, the existing period-level logic is preserved.
- At Mes level, B25 TOTAL and B26 REAL return the value for the selected month.
- At Día level, B25 TOTAL and B26 REAL return the value for the selected calendar-equivalent day.
- YTD measures accumulate through the selected month/day, with the current B26 data cut used for the open month.
- BUDGET remains the contextual career/site/modality target because no official daily target exists.
- Dependent percentages, gap, completion, year-over-year and variance are recalculated at the active temporal grain.

## Empty rows

The Matrix value measure returns BLANK for every metric when neither B25 nor B26 has observations in the current row context. This suppresses empty branches from Carrera through Día.

## Header styling

Column headers are centered, use dark blue `#17365D`, and white text.
