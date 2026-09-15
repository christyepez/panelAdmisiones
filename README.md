# Panel Admisiones — Universidad Indoamérica

Panel navegable y proyecto Power BI para analizar tendencias, avance, metas y proyección de admisiones B25/B26.

## Panel navegable

La implementación funcional está en `dist/` y se abre con cualquier servidor HTTP estático. Incluye:

- resumen ejecutivo;
- comparación B25/B26 al mismo día transcurrido del período;
- cuadro por carrera, sede y modalidad;
- proyección lineal de cierre;
- filtro de formalización;
- separación entre carreras cubiertas por la meta B26 y programas sin meta; y
- controles de calidad y exportación CSV.

El panel usa solamente datos agregados. No almacena identificaciones, nombres, correos ni teléfonos.

Para actualizar `dist/data.json` desde los Excel:

```powershell
python scripts/extract_admissions.py --source-dir "RUTA_A_LA_CARPETA_DE_EXCEL"
node scripts/validate-dashboard.cjs
```

## Current implementation gates

1. Data quality and reconciliation before visual development.
2. Semantic model and business rules.
3. YTD B25 vs B26 using the same elapsed day inside each admissions period.
4. B26 projection based on elapsed days and observed run rate.
5. B26 institutional target: 2,400 admissions, allocated proportionally by career.
6. Missing campus target values remain 0, preserving the source Excel rule.
7. El avance institucional usa únicamente carreras cubiertas por `Metas.xlsx`; los programas sin meta se analizan aparte.

## Repository structure

- `docs/` — scope, business rules, data dictionary and validation criteria.
- `data-quality/` — reconciliation and quality rules.
- `dax/` — documented measure specifications.
- `dist/` — panel web navegable y datos agregados.
- `scripts/` — extracción reproducible y controles automáticos.
- `powerbi/` — proyecto PBIP, informe de cuatro páginas y modelo semántico TMDL.

## Power BI

Abra `powerbi/panelAdmisiones.pbip` en Power BI Desktop y pulse **Actualizar**. El parámetro `SourceFolder` apunta a la carpeta de los tres Excel y puede cambiarse desde **Transformar datos > Administrar parámetros**.

El proyecto incluye las páginas **Resumen ejecutivo**, **Matriz comparativa 2025–2026**, **Proyección** y **Calidad y trazabilidad**. Para regenerar y validar sus archivos:

```powershell
python scripts/build_powerbi_project.py
python scripts/validate_powerbi_project.py
```
