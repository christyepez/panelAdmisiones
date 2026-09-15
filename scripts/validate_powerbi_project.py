from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
PBI = ROOT / "powerbi"
SOURCE = Path(r"C:\Users\ChristianYepez\Universidad Tecnologica Indoamerica\Andres Leonardo Alvear Cosios - Analisis comercial  leads")


def norm(value: object) -> str:
    text = str(value or "").strip().upper()
    return re.sub(r"\s+", " ", "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)))


def career(value: object) -> str:
    text = re.sub(r"^INGENIERIA (EN |DE )?", "", norm(value))
    return {
        "PSICOLOGIA": "PSICOLOGIA GENERAL",
        "ELECTRICIDAD": "ELECTRICA",
        "PEDAGOGIA DE LA ACTIVIDAD FISICA Y DEPORTE": "PEDAGOGIA DE LA ACTIVIDAD FISICA Y DEL DEPORTE",
        "COMUNICACION, PERIODISMO Y PRODUCCION AUDIVISUAL": "COMUNICACION, PERIODISMO Y PRODUCCION AUDIOVISUAL",
    }.get(text, text)


def as_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).strip()).date()
    except ValueError:
        return None


def sheet(file_name: str, sheet_name: str) -> list[tuple]:
    wb = openpyxl.load_workbook(SOURCE / file_name, read_only=True, data_only=True)
    rows = list(wb[sheet_name].values)
    wb.close()
    return rows


def source_controls() -> dict[str, int | float]:
    metas = sheet("Metas.xlsx", "Hoja1")
    target_rows = []
    detail_rows = []
    for row in metas[2:]:
        if not row[1] or not isinstance(row[3], (int, float)):
            continue
        key, modality, value = career(row[1]), norm(row[2]), int(row[3])
        if key == "GENERAL":
            continue
        if modality == "GENERAL":
            target_rows.append((key, value))
        else:
            detail_rows.append((key, modality, value))
    target_keys = {key for key, _ in target_rows}
    original_target = sum(value for _, value in target_rows)

    source26 = sheet("615.xlsx", "reporte")
    headers26 = [norm(x) for x in source26[0]]
    rows26 = []
    ids = Counter()
    for values in source26[1:]:
        row = dict(zip(headers26, values))
        ids[str(row.get("IDENTIFICACION"))] += 1
        if norm(row.get("PERIODO")) != "B26" or norm(row.get("HOMOLOGA")) != "NO" or norm(row.get("MATRICULA EN PRIMERO")) != "SI":
            continue
        rows26.append((career(row.get("CARRERA")), as_date(row.get("FECHA MATRICULA"))))

    source25 = sheet("Datoshistoricob25.xlsx", "Hoja2")
    headers25 = [norm(x) for x in source25[0]]
    rows25 = []
    for values in source25[1:]:
        row = dict(zip(headers25, values))
        if norm(row.get("PERIODO")) == "B25":
            rows25.append((career(row.get("CARRERA")), as_date(row.get("FECHA DE MATRICULA"))))

    start26, end26 = date(2026, 5, 1), date(2026, 9, 30)
    valid_dates = [d for key, d in rows26 if key in target_keys and d and start26 <= d <= end26]
    cutoff = max(valid_dates)
    elapsed = (cutoff - start26).days + 1
    cutoff25 = date(2025, 5, 1).fromordinal(date(2025, 5, 1).toordinal() + elapsed - 1)
    b26_real = sum(key in target_keys and d is not None and start26 <= d <= cutoff for key, d in rows26)
    b25_total = sum(key in target_keys for key, _ in rows25)
    b25_ytd = sum(key in target_keys and d is not None and date(2025, 5, 1) <= d <= cutoff25 for key, d in rows25)
    budget_ytd = round(2400 * b25_ytd / b25_total)
    return {
        "raw_615": len(source26) - 1,
        "candidate_b26": len(rows26),
        "b25_total": b25_total,
        "b25_ytd": b25_ytd,
        "b26_real": b26_real,
        "day_cutoff": elapsed,
        "budget_original": original_target,
        "budget_adjusted": 2400,
        "budget_ytd": budget_ytd,
        "duplicate_identifiers": sum(v > 1 for v in ids.values()),
        "unassigned_target_rows": sum(not re.search(r"\b(AMB|UIO|LTG)\b", modality) for _, modality, _ in detail_rows),
    }


def validate_project() -> None:
    required = [
        PBI / "panelAdmisiones.pbip",
        PBI / "panelAdmisiones.Report" / "definition.pbir",
        PBI / "panelAdmisiones.SemanticModel" / "definition.pbism",
        PBI / "panelAdmisiones.SemanticModel" / "definition" / "model.tmdl",
    ]
    assert all(path.exists() for path in required), "Faltan archivos PBIP"
    for path in PBI.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))

    table_dir = PBI / "panelAdmisiones.SemanticModel" / "definition" / "tables"
    fields: dict[str, set[str]] = {}
    for path in table_dir.glob("*.tmdl"):
        text = path.read_text(encoding="utf-8")
        table_match = re.search(r"^table (.+)$", text, re.M)
        assert table_match, f"Tabla sin declaración: {path}"
        table = table_match.group(1).strip("'")
        fields[table] = set(re.findall(r"^\t(?:column|measure) '?([^'\n]+)'? =?|^\tcolumn ([^\n]+)$", text, re.M))
        normalized = set()
        for item in fields[table]:
            normalized.add(next(x for x in item if x).strip().rstrip(" ="))
        fields[table] = normalized

    for path in (PBI / "panelAdmisiones.Report" / "definition" / "pages").rglob("visual.json"):
        value = json.loads(path.read_text(encoding="utf-8"))
        for node in re.findall(r'"Entity":\s*"([^"]+)"[\s\S]{0,180}?"Property":\s*"([^"]+)"', json.dumps(value)):
            entity, prop = node
            assert entity in fields, f"Entidad inexistente {entity} en {path}"
            assert prop in fields[entity], f"Campo inexistente {entity}.{prop} en {path}"


def validate_reference_math() -> None:
    # Valores visibles en la imagen de referencia. Verifica la semántica de las
    # columnas, aunque el Excel actual tenga un corte posterior.
    total25, ytd25, budget26, real26 = 1589, 906, 2400, 1117
    assert round(ytd25 / total25 * 100) == 57
    assert round(budget26 * ytd25 / total25) == 1368
    assert round(real26 / 1368 * 100) == 82
    assert real26 - 1368 == -251
    assert round(real26 / budget26 * 100) == 47
    assert round(real26 / ytd25 * 100) == 123
    assert real26 - ytd25 == 211


if __name__ == "__main__":
    validate_project()
    validate_reference_math()
    controls = source_controls()
    expected = {"raw_615":1942,"candidate_b26":1351,"b25_total":1589,"budget_original":2500,"budget_adjusted":2400,"duplicate_identifiers":25,"unassigned_target_rows":74}
    for key, value in expected.items():
        assert controls[key] == value, f"{key}: esperado {value}, obtenido {controls[key]}"
    print(json.dumps(controls, ensure_ascii=False, indent=2))
    print("PBIP, referencias visuales y controles de fuente: OK")
