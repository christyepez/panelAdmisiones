# Matrix YTD / filter audit — v1.29

## Matrix row context
Carrera -> Sede -> Modalidad -> Mes -> Dia.

## Active dimension propagation
The semantic model has active relationships from DimCarreraAdm, DimSedeAdm and DimModalidadAdm to:
- FactAdmision615 (B26)
- FactMatriculaHistorica (B25)
- FactMetaAdmision (B26 targets)

Matrix YTD measures only clear DimFecha / DimMesPeriodo / DimPeriodo when rebuilding the cumulative date range. They do not clear Carrera, Sede, Modalidad or TipoCarrera, therefore those filters remain in force.

## Equivalent-cut logic
- B26 cutoff: current matrix Month/Day, capped at the maximum loaded B26 date.
- B25 cutoff: same elapsed-day offset from the B25 period start.
- 2025 TOTAL: final B25 total for the current Carrera/Sede/Modalidad context.
- 2025 YTD: B25 cumulative through the equivalent cutoff.
- 2025 REAL: B25 YTD / B25 TOTAL.
- 2025 Delta %: B26 Budget / B25 TOTAL - 1.
- 2026 BUDGET: target for current Carrera/Sede/Modalidad context; it is intentionally not split by date.
- 2026 YTD: Budget * (B25 YTD / B25 TOTAL).
- 2026 REAL: B26 cumulative through the current cutoff.
- 2026 REAL %: B26 cumulative / B26 Real objective.
- Delta Budget: B26 cumulative - B26 Real objective.
- Completion: B26 cumulative / Budget.
- Real vs LY: B26 cumulative / B25 cumulative equivalent.
- Variance: B26 cumulative - B25 cumulative equivalent.

## Empty-row behavior
At Month/Day levels, row visibility is based on actual records in that exact interval in either B25 or B26; cumulative values alone do not force empty dates to display.
