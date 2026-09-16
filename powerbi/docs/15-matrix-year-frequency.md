# Matrix year grouping and temporal frequency

Base: v1.20.

Matrix:
- Rows: Carrera > Sede > Modalidad > FrecuenciaTiempo field parameter.
- Columns: Ano > Metrica.
- 2025: TOTAL, YTD, REAL, Delta %.
- 2026: BUDGET, YTD, REAL, REAL %, Delta BUDGET, COMPLETION, REAL VS LY, VARIANZA.

Frequency slicer options:
- Mes
- Quincena
- Semana
- Dia

The frequency selector is implemented as a native Power BI field parameter so the same Matrix switches the temporal row grouping without duplicating visuals.
