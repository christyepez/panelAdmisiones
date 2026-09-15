from __future__ import annotations

import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POWERBI = ROOT / "powerbi"
MODEL = POWERBI / "panelAdmisiones.SemanticModel"
REPORT = POWERBI / "panelAdmisiones.Report"
SOURCE_FOLDER = Path(
    r"C:\Users\ChristianYepez\Universidad Tecnologica Indoamerica\Andres Leonardo Alvear Cosios - Analisis comercial  leads"
)


def uid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"panelAdmisiones:{name}"))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def field(entity: str, prop: str, kind: str = "Measure", alias: str | None = None) -> dict:
    result = {
        "field": {
            kind: {
                "Expression": {"SourceRef": {"Entity": entity}},
                "Property": prop,
            }
        },
        "queryRef": f"{entity}.{prop}",
    }
    if alias:
        result["nativeQueryRef"] = alias
    return result


def literal(value: str) -> dict:
    return {"expr": {"Literal": {"Value": value}}}


def container(title: str) -> dict:
    return {
        "background": [{"properties": {"show": literal("true"), "color": {"solid": {"color": literal("'#FFFFFF'")}}, "transparency": literal("0D")}}],
        "border": [{"properties": {"show": literal("true"), "color": {"solid": {"color": literal("'#DED8E4'")}}, "radius": literal("8D")}}],
        "title": [{"properties": {"show": literal("true"), "text": literal(f"'{title}'"), "fontColor": {"solid": {"color": literal("'#2E1748'")}}, "bold": literal("true")}}],
    }


def card(name: str, measure: str, title: str, x: int, y: int, w: int = 250, h: int = 105) -> dict:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": 10, "height": h, "width": w, "tabOrder": 10},
        "visual": {
            "visualType": "card",
            "query": {"queryState": {"Values": {"projections": [field("Medidas", measure, alias=title)]}}},
            "objects": {"categoryLabels": [{"properties": {"show": literal("false")}}], "labels": [{"properties": {"fontSize": literal("24D"), "labelDisplayUnits": literal("1D")}}]},
            "visualContainerObjects": container(title),
        },
    }


def slicer(name: str, entity: str, prop: str, title: str, x: int, y: int, w: int = 220) -> dict:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": 10, "height": 70, "width": w, "tabOrder": 10},
        "visual": {
            "visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [dict(field(entity, prop, "Column"), active=True)]}}},
            "objects": {"header": [{"properties": {"show": literal("false")}}], "selection": [{"properties": {"singleSelect": literal("false"), "selectAllCheckboxEnabled": literal("true")}}], "data": [{"properties": {"mode": literal("'Dropdown'")}}]},
            "visualContainerObjects": container(title),
        },
    }


def line_chart(name: str, title: str, measures: list[tuple[str, str]], x: int, y: int, w: int, h: int) -> dict:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": 8, "height": h, "width": w, "tabOrder": 8},
        "visual": {
            "visualType": "lineChart",
            "query": {"queryState": {"Category": {"projections": [dict(field("DimDiaPeriodo", "DiaPeriodo", "Column"), active=True)]}, "Y": {"projections": [field("Medidas", m, alias=a) for m, a in measures]}}, "sortDefinition": {"sort": [{"field": field("DimDiaPeriodo", "DiaPeriodo", "Column")["field"], "direction": "Ascending"}], "isDefaultSort": True}},
            "objects": {"labels": [{"properties": {"show": literal("false")}}], "lineStyles": [{"properties": {"strokeWidth": literal("3D"), "showMarker": literal("false")}}]},
            "visualContainerObjects": container(title),
        },
    }


def bar_chart(name: str, title: str, measure: str, x: int, y: int, w: int, h: int) -> dict:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": 9, "height": h, "width": w, "tabOrder": 9},
        "visual": {
            "visualType": "clusteredBarChart",
            "query": {"queryState": {"Category": {"projections": [dict(field("DimCarrera", "Carrera", "Column"), active=True)]}, "Y": {"projections": [field("Medidas", measure, alias="Real 2026")]}}, "sortDefinition": {"sort": [{"field": field("Medidas", measure)["field"], "direction": "Descending"}], "isDefaultSort": True}},
            "objects": {"dataPoint": [{"properties": {"fill": {"solid": {"color": literal("'#5B2C83'")}}}}], "labels": [{"properties": {"show": literal("true"), "labelDisplayUnits": literal("1D")}}]},
            "visualContainerObjects": container(title),
        },
    }


def table_visual(name: str, title: str, projections: list[dict], x: int, y: int, w: int, h: int) -> dict:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": 7, "height": h, "width": w, "tabOrder": 7},
        "visual": {"visualType": "tableEx", "query": {"queryState": {"Values": {"projections": projections}}}, "visualContainerObjects": container(title)},
    }


EXPRESSIONS = f'''expression SourceFolder = "{SOURCE_FOLDER}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]

expression FxCleanText =
\t\t(v as any) as nullable text =>
\t\tlet
\t\t    T = if v = null then null else Text.Trim(Text.From(v))
\t\tin
\t\t    if T = null or T = "" or Text.Lower(T) = "null" then null else T

expression FxNormalize =
\t\t(v as any) as text =>
\t\tlet
\t\t    S0 = Text.Upper(Text.Trim(if v = null then "" else Text.From(v))),
\t\t    S1 = Text.Replace(Text.Replace(Text.Replace(Text.Replace(Text.Replace(Text.Replace(S0,"Á","A"),"É","E"),"Í","I"),"Ó","O"),"Ú","U"),"Ü","U"),
\t\t    S2 = Text.Replace(S1,"Ñ","N"),
\t\t    S3 = Text.Combine(List.Select(Text.SplitAny(S2," "), each _ <> ""), " ")
\t\tin
\t\t    S3

expression FxCareerKey =
\t\t(v as any) as text =>
\t\tlet
\t\t    N0 = FxNormalize(v),
\t\t    N1 = if Text.StartsWith(N0,"INGENIERIA EN ") then Text.Range(N0,14) else if Text.StartsWith(N0,"INGENIERIA DE ") then Text.Range(N0,14) else if Text.StartsWith(N0,"INGENIERIA ") then Text.Range(N0,11) else N0,
\t\t    N2 = if N1 = "PSICOLOGIA" then "PSICOLOGIA GENERAL" else if N1 = "ELECTRICIDAD" then "ELECTRICA" else if N1 = "PEDAGOGIA DE LA ACTIVIDAD FISICA Y DEPORTE" then "PEDAGOGIA DE LA ACTIVIDAD FISICA Y DEL DEPORTE" else if N1 = "COMUNICACION, PERIODISMO Y PRODUCCION AUDIVISUAL" then "COMUNICACION, PERIODISMO Y PRODUCCION AUDIOVISUAL" else N1
\t\tin
\t\t    N2

expression FxTipoPrograma =
\t\t(v as any) as text =>
\t\tlet N = FxNormalize(v)
\t\tin if Text.Contains(N,"MAESTRIA") or Text.Contains(N,"ESPECIALIZACION") or Text.Contains(N,"DOCTORADO") or Text.Contains(N,"POSGRADO") or Text.Contains(N,"MASTER") or Text.Contains(N,"PHD") then "POSGRADO" else "GRADO"
'''


FACT_METAS_CARRERA_M = '''let
    Wb = Excel.Workbook(File.Contents(SourceFolder & "\\Metas.xlsx"), null, true),
    Raw = Wb{[Item="Hoja1",Kind="Sheet"]}[Data],
    Rows = Table.Skip(Raw,2),
    Selected = Table.SelectColumns(Rows,{"Column1","Column2","Column3"}),
    Renamed = Table.RenameColumns(Selected,{{"Column1","Carrera"},{"Column2","Modalidad"},{"Column3","MetaOriginal"}}),
    Clean = Table.TransformColumns(Renamed,{{"Carrera",FxCleanText,type text},{"Modalidad",FxNormalize,type text},{"MetaOriginal",each try Number.From(_) otherwise null,type number}}),
    AddKey = Table.AddColumn(Clean,"CarreraKey",each FxCareerKey([Carrera]),type text),
    Filtered = Table.SelectRows(AddKey, each [CarreraKey] <> "" and [CarreraKey] <> "GENERAL" and [Modalidad] = "GENERAL" and [MetaOriginal] <> null),
    TotalOriginal = List.Sum(Filtered[MetaOriginal]),
    AddExact = Table.AddColumn(Filtered,"MetaExacta",each [MetaOriginal] * 2400 / TotalOriginal,type number),
    AddBase = Table.AddColumn(AddExact,"MetaBase",each Number.RoundDown([MetaExacta]),Int64.Type),
    AddRemainder = Table.AddColumn(AddBase,"Resto",each [MetaExacta]-[MetaBase],type number),
    Missing = 2400 - List.Sum(AddRemainder[MetaBase]),
    Sorted = Table.Sort(AddRemainder,{{"Resto",Order.Descending},{"CarreraKey",Order.Ascending}}),
    Indexed = Table.AddIndexColumn(Sorted,"OrdenResto",1,1,Int64.Type),
    AddTarget = Table.AddColumn(Indexed,"MetaAjustada",each [MetaBase] + (if [OrdenResto] <= Missing then 1 else 0),Int64.Type),
    Result = Table.SelectColumns(AddTarget,{"CarreraKey","Carrera","MetaOriginal","MetaAjustada"})
in
    Result'''


FACT_B26_M = '''let
    Wb = Excel.Workbook(File.Contents(SourceFolder & "\\615.xlsx"), null, true),
    Raw = Wb{[Item="reporte",Kind="Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(Raw,[PromoteAllScalars=true]),
    Selected = Table.SelectColumns(Promoted,{"Periodo","Sede","CARRERA","MODALIDAD","IDENTIFICACION","FECHA MATRICULA","FORMALIZADO","HOMOLOGA","MATRICULA EN PRIMERO"},MissingField.UseNull),
    Renamed = Table.RenameColumns(Selected,{{"CARRERA","Carrera"},{"MODALIDAD","Modalidad"},{"IDENTIFICACION","Identificacion"},{"FECHA MATRICULA","FechaMatricula"},{"FORMALIZADO","Formalizado"},{"HOMOLOGA","Homologa"},{"MATRICULA EN PRIMERO","MatriculaPrimero"}}),
    Clean = Table.TransformColumns(Renamed,{{"Periodo",FxNormalize,type text},{"Sede",FxNormalize,type text},{"Carrera",FxCleanText,type text},{"Modalidad",FxNormalize,type text},{"Identificacion",FxCleanText,type text},{"Formalizado",FxNormalize,type text},{"Homologa",FxNormalize,type text},{"MatriculaPrimero",FxNormalize,type text},{"FechaMatricula",each try Date.From(_) otherwise null,type date}}),
    Candidates = Table.SelectRows(Clean,each [Periodo]="B26" and [Homologa]="NO" and [MatriculaPrimero]="SI"),
    AddKey = Table.AddColumn(Candidates,"CarreraKey",each FxCareerKey([Carrera]),type text),
    AddType = Table.AddColumn(AddKey,"TipoPrograma",each FxTipoPrograma([CarreraKey]),type text),
    AddTarget = Table.AddColumn(AddType,"TieneMeta",each List.Contains(FactMetasCarrera[CarreraKey],[CarreraKey]),type logical),
    AddFormal = Table.AddColumn(AddTarget,"EsFormalizado",each [Formalizado]="SI",type logical),
    AddPeriod = Table.AddColumn(AddFormal,"EnPeriodo",each [FechaMatricula]<>null and [FechaMatricula]>=#date(2026,5,1) and [FechaMatricula]<=#date(2026,9,30),type logical),
    AddDay = Table.AddColumn(AddPeriod,"DiaPeriodo",each if [EnPeriodo] then Duration.Days([FechaMatricula]-#date(2026,5,1))+1 else null,Int64.Type),
    AddId = Table.AddIndexColumn(AddDay,"RegistroId",1,1,Int64.Type),
    Result = Table.RemoveColumns(AddId,{"Identificacion","Homologa","MatriculaPrimero","Formalizado"})
in
    Result'''


FACT_B25_M = '''let
    Wb = Excel.Workbook(File.Contents(SourceFolder & "\\Datoshistoricob25.xlsx"), null, true),
    Raw = Wb{[Item="Hoja2",Kind="Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(Raw,[PromoteAllScalars=true]),
    Selected = Table.SelectColumns(Promoted,{"PERIODO","SEDE","MODALIDAD","CARRERA","FECHA DE MATRICULA","FORMALIZADA"},MissingField.UseNull),
    Renamed = Table.RenameColumns(Selected,{{"PERIODO","Periodo"},{"SEDE","Sede"},{"MODALIDAD","Modalidad"},{"CARRERA","Carrera"},{"FECHA DE MATRICULA","FechaMatricula"},{"FORMALIZADA","Formalizado"}}),
    Clean = Table.TransformColumns(Renamed,{{"Periodo",FxNormalize,type text},{"Sede",FxNormalize,type text},{"Carrera",FxCleanText,type text},{"Modalidad",FxNormalize,type text},{"Formalizado",FxNormalize,type text},{"FechaMatricula",each try Date.From(_) otherwise null,type date}}),
    Candidates = Table.SelectRows(Clean,each [Periodo]="B25"),
    AddKey = Table.AddColumn(Candidates,"CarreraKey",each FxCareerKey([Carrera]),type text),
    AddType = Table.AddColumn(AddKey,"TipoPrograma",each FxTipoPrograma([CarreraKey]),type text),
    AddTarget = Table.AddColumn(AddType,"TieneMeta",each List.Contains(FactMetasCarrera[CarreraKey],[CarreraKey]),type logical),
    AddFormal = Table.AddColumn(AddTarget,"EsFormalizado",each [Formalizado]="SI",type logical),
    AddPeriod = Table.AddColumn(AddFormal,"EnPeriodo",each [FechaMatricula]<>null and [FechaMatricula]>=#date(2025,5,1) and [FechaMatricula]<=#date(2025,9,30),type logical),
    AddDay = Table.AddColumn(AddPeriod,"DiaPeriodo",each if [EnPeriodo] then Duration.Days([FechaMatricula]-#date(2025,5,1))+1 else null,Int64.Type),
    AddId = Table.AddIndexColumn(AddDay,"RegistroId",1,1,Int64.Type),
    Result = Table.RemoveColumns(AddId,{"Formalizado"})
in
    Result'''


FACT_META_SEDE_M = '''let
    Wb = Excel.Workbook(File.Contents(SourceFolder & "\\Metas.xlsx"), null, true),
    Raw = Wb{[Item="Hoja1",Kind="Sheet"]}[Data],
    Rows = Table.Skip(Raw,2),
    Selected = Table.SelectColumns(Rows,{"Column1","Column2","Column3"}),
    Renamed = Table.RenameColumns(Selected,{{"Column1","Carrera"},{"Column2","ModalidadMeta"},{"Column3","Meta"}}),
    Clean = Table.TransformColumns(Renamed,{{"Carrera",FxCleanText,type text},{"ModalidadMeta",FxNormalize,type text},{"Meta",each try Number.From(_) otherwise null,type number}}),
    AddKey = Table.AddColumn(Clean,"CarreraKey",each FxCareerKey([Carrera]),type text),
    Detail = Table.SelectRows(AddKey,each [CarreraKey]<>"" and [CarreraKey]<>"GENERAL" and [ModalidadMeta]<>"GENERAL" and [Meta]<>null),
    AddSede = Table.AddColumn(Detail,"Sede",each if Text.Contains([ModalidadMeta],"AMB") then "MATRIZ" else if Text.Contains([ModalidadMeta],"UIO") then "QUITO" else if Text.Contains([ModalidadMeta],"LTG") then "LATACUNGA" else null,type text),
    AddModality = Table.AddColumn(AddSede,"Modalidad",each if Text.StartsWith([ModalidadMeta],"PRESENCIAL") then "PRESENCIAL" else if Text.StartsWith([ModalidadMeta],"EN LINEA") then "EN LINEA" else if Text.StartsWith([ModalidadMeta],"SEMIPRESENCIAL") then "SEMIPRESENCIAL" else if Text.StartsWith([ModalidadMeta],"HIBRIDA") then "HIBRIDA" else null,type text),
    Result = Table.SelectColumns(AddModality,{"CarreraKey","Carrera","Sede","Modalidad","ModalidadMeta","Meta"})
in
    Result'''


QUALITY_M = '''let
    Wb26 = Excel.Workbook(File.Contents(SourceFolder & "\\615.xlsx"), null, true),
    R26 = Table.PromoteHeaders(Wb26{[Item="reporte",Kind="Sheet"]}[Data],[PromoteAllScalars=true]),
    C26 = Table.TransformColumns(Table.SelectColumns(R26,{"Periodo","IDENTIFICACION","FECHA MATRICULA","HOMOLOGA","MATRICULA EN PRIMERO"},MissingField.UseNull),{{"Periodo",FxNormalize,type text},{"IDENTIFICACION",FxCleanText,type text},{"HOMOLOGA",FxNormalize,type text},{"MATRICULA EN PRIMERO",FxNormalize,type text},{"FECHA MATRICULA",each try Date.From(_) otherwise null,type date}}),
    Cand26 = Table.SelectRows(C26,each [Periodo]="B26" and [HOMOLOGA]="NO" and [MATRICULA EN PRIMERO]="SI"),
    Groups = Table.Group(Table.SelectRows(C26,each [IDENTIFICACION]<>null),{"IDENTIFICACION"},{{"N",each Table.RowCount(_),Int64.Type}}),
    Duplicados = Table.RowCount(Table.SelectRows(Groups,each [N]>1)),
    FueraPeriodo = Table.RowCount(Table.SelectRows(Cand26,each [FECHA MATRICULA]=null or [FECHA MATRICULA]<#date(2026,5,1) or [FECHA MATRICULA]>#date(2026,9,30))),
    Wb25 = Excel.Workbook(File.Contents(SourceFolder & "\\Datoshistoricob25.xlsx"), null, true),
    R25 = Table.PromoteHeaders(Wb25{[Item="Hoja2",Kind="Sheet"]}[Data],[PromoteAllScalars=true]),
    Hist25 = Table.RowCount(Table.SelectRows(R25,each FxNormalize([PERIODO])="B25")),
    Unassigned = Table.RowCount(Table.SelectRows(FactMetasSede,each [Sede]=null)),
    Result = #table(type table [Registros615=Int64.Type,CandidatosB26=Int64.Type,HistoricoB25=Int64.Type,DuplicadosIdentificacion=Int64.Type,FueraPeriodoB26=Int64.Type,MetasSinSede=Int64.Type],{{Table.RowCount(R26),Table.RowCount(Cand26),Hist25,Duplicados,FueraPeriodo,Unassigned}})
in
    Result'''


def table_tmdl(name: str, columns: list[tuple[str, str, str | None]], source: str, measures: list[tuple[str, str, str]] | None = None) -> str:
    lines = [f"table {name}"]
    if measures:
        for mname, expression, fmt in measures:
            if "\n" in expression:
                lines += [f"\tmeasure '{mname}' = ```", *["\t\t" + x for x in expression.splitlines()], "\t\t```"]
            else:
                lines.append(f"\tmeasure '{mname}' = {expression}")
            if fmt:
                lines.append(f"\t\tformatString: {fmt}")
            lines.append("")
    for col, typ, fmt in columns:
        lines += [f"\tcolumn {col}", f"\t\tdataType: {typ}"]
        if fmt:
            lines.append(f"\t\tformatString: {fmt}")
        lines += [f"\t\tsourceColumn: {col}", ""]
    lines += [f"\tpartition {name} = m", "\t\tmode: import", "\t\tsource ="]
    lines += ["\t\t\t\t" + x for x in source.splitlines()]
    return "\n".join(lines)


MEASURES = [
    ("Dia corte", "VAR MaxDatos = CALCULATE(MAX(FactB26[DiaPeriodo]),REMOVEFILTERS(DimDiaPeriodo),FactB26[EnPeriodo]=TRUE(),FactB26[TieneMeta]=TRUE()) RETURN MIN(MAX(DimDiaPeriodo[DiaPeriodo]),MaxDatos)", "0"),
    ("2025 Total", "CALCULATE(COUNTROWS(FactB25),FactB25[TieneMeta]=TRUE())", "#,0"),
    ("2025 YTD", "VAR D=[Dia corte] RETURN CALCULATE(COUNTROWS(FactB25),FactB25[TieneMeta]=TRUE(),FactB25[EnPeriodo]=TRUE(),FILTER(ALL(FactB25[DiaPeriodo]),FactB25[DiaPeriodo]<=D))", "#,0"),
    ("2025 Real %", "DIVIDE([2025 YTD],[2025 Total])", "0.0%"),
    ("2025 Delta %", "BLANK()", "0.0%"),
    ("2026 Budget", "IF(ISFILTERED(DimSede[Sede]) || ISFILTERED(DimModalidad[Modalidad]),COALESCE(SUM(FactMetasSede[Meta]),0),COALESCE(SUM(FactMetasCarrera[MetaAjustada]),0))", "#,0"),
    ("2026 YTD", "ROUND([2026 Budget]*[2025 Real %],0)", "#,0"),
    ("2026 Real", "VAR D=[Dia corte] RETURN CALCULATE(COUNTROWS(FactB26),FactB26[TieneMeta]=TRUE(),FactB26[EnPeriodo]=TRUE(),FILTER(ALL(FactB26[DiaPeriodo]),FactB26[DiaPeriodo]<=D))", "#,0"),
    ("2026 Real %", "DIVIDE([2026 Real],[2026 YTD])", "0.0%"),
    ("Delta Budget", "[2026 Real]-[2026 YTD]", "#,0;[Red]-#,0"),
    ("Completion", "DIVIDE([2026 Real],[2026 Budget])", "0.0%"),
    ("Real vs LY", "DIVIDE([2026 Real],[2025 YTD])", "0.0%"),
    ("Variance", "[2026 Real]-[2025 YTD]", "#,0;[Red]-#,0"),
    ("Brecha cierre", "[2026 Budget]-[2026 Real]", "#,0"),
    ("Dias periodo", "153", "0"),
    ("Ritmo diario", "DIVIDE([2026 Real],[Dia corte])", "0.0"),
    ("Ritmo requerido", "DIVIDE([Brecha cierre],[Dias periodo]-[Dia corte])", "0.0"),
    ("Proyeccion lineal", "DIVIDE([2026 Real],[Dia corte])*[Dias periodo]", "#,0"),
    ("B26 acumulado", "VAR D=MAX(DimDiaPeriodo[DiaPeriodo]) RETURN IF(D>[Dia corte],BLANK(),CALCULATE(COUNTROWS(FactB26),FactB26[TieneMeta]=TRUE(),FactB26[EnPeriodo]=TRUE(),FILTER(ALL(FactB26[DiaPeriodo]),FactB26[DiaPeriodo]<=D)))", "#,0"),
    ("B25 acumulado", "VAR D=MAX(DimDiaPeriodo[DiaPeriodo]) RETURN CALCULATE(COUNTROWS(FactB25),FactB25[TieneMeta]=TRUE(),FactB25[EnPeriodo]=TRUE(),FILTER(ALL(FactB25[DiaPeriodo]),FactB25[DiaPeriodo]<=D))", "#,0"),
    ("Meta lineal", "DIVIDE([2026 Budget],[Dias periodo])*MAX(DimDiaPeriodo[DiaPeriodo])", "#,0"),
    ("Registros 615", "MAX(FactCalidad[Registros615])", "#,0"),
    ("Candidatos B26", "MAX(FactCalidad[CandidatosB26])", "#,0"),
    ("Registros B25", "MAX(FactCalidad[HistoricoB25])", "#,0"),
    ("Identificaciones duplicadas", "MAX(FactCalidad[DuplicadosIdentificacion])", "#,0"),
    ("B26 fuera de periodo", "MAX(FactCalidad[FueraPeriodoB26])", "#,0"),
    ("Metas sin sede", "MAX(FactCalidad[MetasSinSede])", "#,0"),
]


def build_model() -> None:
    # Overwrite the generated model in place because OneDrive may temporarily
    # lock directories even though the individual files remain writable.
    write(MODEL / "definition.pbism", json.dumps({"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json","version":"4.2","settings":{"qnaEnabled":False}}, indent=2))
    dump(MODEL / ".platform", {"$schema":"https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json","metadata":{"type":"SemanticModel","displayName":"panelAdmisiones"},"config":{"version":"2.0","logicalId":uid("semantic-model")}})
    write(MODEL / "definition" / "database.tmdl", "database\n\tcompatibilityLevel: 1606")
    refs = ["FactMetasCarrera","FactB26","FactB25","FactMetasSede","FactCalidad","DimCarrera","DimSede","DimModalidad","DimDiaPeriodo","Medidas"]
    model = "model Model\n\tculture: es-EC\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tdiscourageImplicitMeasures\n\tsourceQueryCulture: es-EC\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\nannotation PBI_QueryOrder = [" + ",".join(f'\"{x}\"' for x in refs) + ",\"SourceFolder\",\"FxCleanText\",\"FxNormalize\",\"FxCareerKey\",\"FxTipoPrograma\"]\n\nannotation __PBI_TimeIntelligenceEnabled = 0\n\n" + "\n".join(f"ref table {x}" for x in refs)
    write(MODEL / "definition" / "model.tmdl", model)
    write(MODEL / "definition" / "expressions.tmdl", EXPRESSIONS)

    tables = MODEL / "definition" / "tables"
    common_fact_cols = [("RegistroId","int64","0"),("Periodo","string",None),("Sede","string",None),("Carrera","string",None),("CarreraKey","string",None),("Modalidad","string",None),("FechaMatricula","dateTime","Short Date"),("DiaPeriodo","int64","0"),("TipoPrograma","string",None),("TieneMeta","boolean",None),("EsFormalizado","boolean",None),("EnPeriodo","boolean",None)]
    write(tables / "FactMetasCarrera.tmdl", table_tmdl("FactMetasCarrera",[("CarreraKey","string",None),("Carrera","string",None),("MetaOriginal","double","#,0"),("MetaAjustada","int64","#,0")],FACT_METAS_CARRERA_M))
    write(tables / "FactB26.tmdl", table_tmdl("FactB26",common_fact_cols,FACT_B26_M))
    write(tables / "FactB25.tmdl", table_tmdl("FactB25",common_fact_cols,FACT_B25_M))
    write(tables / "FactMetasSede.tmdl", table_tmdl("FactMetasSede",[("CarreraKey","string",None),("Carrera","string",None),("Sede","string",None),("Modalidad","string",None),("ModalidadMeta","string",None),("Meta","double","#,0")],FACT_META_SEDE_M))
    write(tables / "FactCalidad.tmdl", table_tmdl("FactCalidad",[("Registros615","int64","#,0"),("CandidatosB26","int64","#,0"),("HistoricoB25","int64","#,0"),("DuplicadosIdentificacion","int64","#,0"),("FueraPeriodoB26","int64","#,0"),("MetasSinSede","int64","#,0")],QUALITY_M))

    dim_carrera_m = '''let
    Combined = Table.Combine({Table.SelectColumns(FactB26,{"CarreraKey"}),Table.SelectColumns(FactB25,{"CarreraKey"}),Table.SelectColumns(FactMetasCarrera,{"CarreraKey"})}),
    Clean = Table.SelectRows(Combined,each [CarreraKey]<>null and [CarreraKey]<>""),
    DistinctRows = Table.Distinct(Clean),
    AddName = Table.AddColumn(DistinctRows,"Carrera",each [CarreraKey],type text),
    AddTarget = Table.AddColumn(AddName,"TieneMeta",each List.Contains(FactMetasCarrera[CarreraKey],[CarreraKey]),type logical)
in
    AddTarget'''
    dim_sede_m = '''let T=#table(type table [Sede=text],{{"MATRIZ"},{"QUITO"},{"LATACUNGA"}}) in T'''
    dim_mod_m = '''let C=Table.Combine({Table.SelectColumns(FactB26,{"Modalidad"}),Table.SelectColumns(FactB25,{"Modalidad"})}), F=Table.SelectRows(C,each [Modalidad]<>null and [Modalidad]<>""), D=Table.Distinct(F) in D'''
    dim_day_m = '''let D=Table.FromList({1..153},Splitter.SplitByNothing(),{"DiaPeriodo"}), A=Table.AddColumn(D,"FechaB26",each Date.AddDays(#date(2026,5,1),[DiaPeriodo]-1),type date), B=Table.AddColumn(A,"FechaB25",each Date.AddDays(#date(2025,5,1),[DiaPeriodo]-1),type date), C=Table.AddColumn(B,"Etiqueta",each Date.ToText([FechaB26],"dd-MMM"),type text) in C'''
    write(tables / "DimCarrera.tmdl",table_tmdl("DimCarrera",[("CarreraKey","string",None),("Carrera","string",None),("TieneMeta","boolean",None)],dim_carrera_m))
    write(tables / "DimSede.tmdl",table_tmdl("DimSede",[("Sede","string",None)],dim_sede_m))
    write(tables / "DimModalidad.tmdl",table_tmdl("DimModalidad",[("Modalidad","string",None)],dim_mod_m))
    write(tables / "DimDiaPeriodo.tmdl",table_tmdl("DimDiaPeriodo",[("DiaPeriodo","int64","0"),("FechaB26","dateTime","Short Date"),("FechaB25","dateTime","Short Date"),("Etiqueta","string",None)],dim_day_m))
    write(tables / "Medidas.tmdl",table_tmdl("Medidas",[("Clave","int64","0")],'''#table(type table [Clave=Int64.Type],{{1}})''',MEASURES))

    relationships = []
    pairs = [
        ("FactB26.CarreraKey","DimCarrera.CarreraKey"),("FactB25.CarreraKey","DimCarrera.CarreraKey"),("FactMetasCarrera.CarreraKey","DimCarrera.CarreraKey"),("FactMetasSede.CarreraKey","DimCarrera.CarreraKey"),
        ("FactB26.Sede","DimSede.Sede"),("FactB25.Sede","DimSede.Sede"),("FactMetasSede.Sede","DimSede.Sede"),
        ("FactB26.Modalidad","DimModalidad.Modalidad"),("FactB25.Modalidad","DimModalidad.Modalidad"),("FactMetasSede.Modalidad","DimModalidad.Modalidad"),
    ]
    for left,right in pairs:
        relationships += [f"relationship {uid(left + '->' + right)}",f"\tfromColumn: {left}",f"\ttoColumn: {right}",""]
    write(MODEL / "definition" / "relationships.tmdl","\n".join(relationships))


def build_report() -> None:
    definition = REPORT / "definition"
    # OneDrive can mark existing PBIR folders read-only while syncing.  The
    # metadata page order is authoritative, so generated files are overwritten
    # in place and any obsolete page folder is harmless.
    dump(REPORT / ".platform", {"$schema":"https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json","metadata":{"type":"Report","displayName":"panelAdmisiones"},"config":{"version":"2.0","logicalId":uid("report")}})
    dump(REPORT / "definition.pbir", {"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json","version":"4.0","datasetReference":{"byPath":{"path":"../panelAdmisiones.SemanticModel"}}})
    dump(definition / "report.json", {"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.1.0/schema.json","layoutOptimization":"None","objects":{"section":[{"properties":{"verticalAlignment":literal("'Top'")}}]},"resourcePackages":[]})

    pages: dict[str, tuple[str,list[dict]]] = {}
    pages["resumen"] = ("Resumen ejecutivo",[
        slicer("f_sede","DimSede","Sede","Sede",20,20),slicer("f_modalidad","DimModalidad","Modalidad","Modalidad",255,20),slicer("f_carrera","DimCarrera","Carrera","Carrera",490,20,330),slicer("f_corte","DimDiaPeriodo","DiaPeriodo","Día de corte",835,20,180),
        card("k_real","2026 Real","Matrículas B26",20,110),card("k_meta","2026 Budget","Meta B26",285,110),card("k_completion","Completion","Cumplimiento",550,110),card("k_vsly","Real vs LY","Real vs B25",815,110),card("k_projection","Proyeccion lineal","Proyección cierre",1080,110,300),
        line_chart("trend","Acumulado comparable por día del período",[("B26 acumulado","B26"),("B25 acumulado","B25"),("Meta lineal","Meta")],20,235,900,430),
        bar_chart("career","Matrículas B26 por carrera", "2026 Real",940,235,440,430),
    ])
    matrix_projections = [field("DimCarrera","Carrera","Column","CARRERAS")]
    for m,a in [("2025 Total","2025 TOTAL"),("2025 YTD","2025 YTD"),("2025 Real %","2025 REAL"),("2025 Delta %","2025 Δ%"),("2026 Budget","2026 BUDGET"),("2026 YTD","2026 YTD"),("2026 Real","2026 REAL"),("2026 Real %","2026 REAL %"),("Delta Budget","Δ BUDGET"),("Completion","COMPLETION"),("Real vs LY","REAL VS LY"),("Variance","VARIANZA")]:
        matrix_projections.append(field("Medidas",m,alias=a))
    pages["matriz"] = ("Matriz comparativa 2025–2026",[
        slicer("m_sede","DimSede","Sede","Sede",20,20),slicer("m_modalidad","DimModalidad","Modalidad","Modalidad",255,20),slicer("m_corte","DimDiaPeriodo","DiaPeriodo","Día de corte",490,20),
        table_visual("comparison","NE UG · Comparación por carrera",matrix_projections,20,110,1360,650),
    ])
    pages["proyeccion"] = ("Proyección",[
        card("p_real","2026 Real","Real al corte",20,30),card("p_projection","Proyeccion lineal","Proyección lineal",285,30),card("p_gap","Brecha cierre","Brecha a meta",550,30),card("p_rate","Ritmo diario","Ritmo actual",815,30),card("p_required","Ritmo requerido","Ritmo requerido",1080,30,300),
        line_chart("projection_chart","Trayectoria real, histórica y meta",[("B26 acumulado","B26 real"),("B25 acumulado","B25 comparable"),("Meta lineal","Meta lineal")],20,165,1360,560),
    ])
    quality_proj=[field("DimCarrera","Carrera","Column","Carrera"),field("DimCarrera","TieneMeta","Column","Tiene meta"),field("Medidas","2026 Real",alias="B26"),field("Medidas","2025 Total",alias="B25 total")]
    pages["calidad"] = ("Calidad y trazabilidad",[
        card("q_raw","Registros 615","Filas 615.xlsx",20,30),card("q_cand","Candidatos B26","Candidatos B26",285,30),card("q_hist","Registros B25","Filas B25",550,30),card("q_dup","Identificaciones duplicadas","IDs duplicadas",815,30),card("q_out","B26 fuera de periodo","Fuera mayo–sept.",1080,30,300),
        card("q_target","Metas sin sede","Metas detalle sin sede",20,170,300),
        table_visual("q_careers","Cobertura de carreras en metas",quality_proj,340,170,1040,540),
    ])

    page_order=[]
    for key,(display,visuals) in pages.items():
        page_order.append(key)
        page_dir=definition/"pages"/key
        dump(page_dir/"page.json",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.3.0/schema.json","name":key,"displayName":display,"displayOption":"FitToWidth","height":800,"width":1400})
        for visual in visuals:
            dump(page_dir/"visuals"/visual["name"]/"visual.json",visual)
    dump(definition/"pages"/"pages.json",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json","pageOrder":page_order,"activePageName":"resumen"})


def main() -> None:
    missing=[x for x in [SOURCE_FOLDER/"615.xlsx",SOURCE_FOLDER/"Datoshistoricob25.xlsx",SOURCE_FOLDER/"Metas.xlsx"] if not x.exists()]
    if missing:
        raise SystemExit("Fuentes no encontradas: " + ", ".join(map(str,missing)))
    build_model()
    build_report()
    print(f"PBIP generado en {POWERBI}")


if __name__ == "__main__":
    main()
