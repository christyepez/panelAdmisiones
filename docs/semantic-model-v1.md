# Semantic Model V1

## Facts
### FactAdmisionesB26
Source: `615.xlsx/reporte`.
Candidate business filter: B26 + HOMOLOGA=NO + MATRICULA EN PRIMERO=SI. Formalization remains an explicit attribute until reconciliation decides whether it belongs in the admission rule.

### FactAdmisionesB25
Source: `Datoshistoricob25.xlsx/Hoja2`.
Grain: one first-level B25 student per identifier; 1,879 unique identifiers in the supplied sheet.

### FactMetas
Source: `Metas.xlsx/Hoja1`.
Store original source target and adjusted B26 target separately. Do not overwrite the source value.

## Dimensions
- DimFecha
- DimPeriodo with PeriodStart, PeriodEnd and DayInPeriod
- DimCarrera with canonical career key and source aliases
- DimSede: MATRIZ, QUITO, LATACUNGA
- DimModalidad with normalized modality values
- DimFuente where available

## Target reconciliation
Career GENERAL source targets total 2,500. Approved B26 target is 2,400. Base proportional factor is `2400 / 2500 = 0.96`. Final integer allocation must preserve exactly 2,400 after rounding by assigning remainder deterministically.

Campus target rows retain source Excel values. Missing campus target combinations evaluate to 0.

## Period alignment
The comparison axis is `DayInPeriod`. B25 and B26 cumulative admissions are compared at equal elapsed-day positions, never by equal calendar date.

## Relationships
Use single-direction 1:* dimension-to-fact relationships. Avoid bidirectional and many-to-many relationships unless a documented bridge is required after canonical mapping.