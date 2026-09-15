from pathlib import Path
from collections import Counter
from datetime import datetime,date
import argparse,openpyxl,json,unicodedata,re,math,csv

parser=argparse.ArgumentParser(description='Genera datos agregados del panel sin datos personales.')
parser.add_argument('--source-dir',required=True,type=Path)
args=parser.parse_args()
SOURCE=args.source_dir
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
OUT.mkdir(parents=True,exist_ok=True)
def norm(s):
    s=str(s or '').strip().upper()
    return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)))
def career(s):
    n=norm(s)
    n=re.sub(r'^INGENIERIA (EN |DE )?','',n)
    return {
        'PSICOLOGIA':'PSICOLOGIA GENERAL',
        'ELECTRICIDAD':'ELECTRICA',
        'PEDAGOGIA DE LA ACTIVIDAD FISICA Y DEPORTE':'PEDAGOGIA DE LA ACTIVIDAD FISICA Y DEL DEPORTE',
        'COMUNICACION, PERIODISMO Y PRODUCCION AUDIVISUAL':'COMUNICACION, PERIODISMO Y PRODUCCION AUDIOVISUAL'
    }.get(n,n)
def day(v):
    if isinstance(v,(date,datetime)):return v.strftime('%Y-%m-%d')
    if not v:return None
    for f in ['%d/%m/%Y','%Y-%m-%d','%d/%m/%Y %H:%M:%S','%Y-%m-%d %H:%M:%S','%d-%m-%Y']:
        try:return datetime.strptime(str(v).strip(),f).strftime('%Y-%m-%d')
        except ValueError:pass
    return None
def read(name,sheet):
    wb=openpyxl.load_workbook(SOURCE/name,read_only=True,data_only=True)
    rows=list(wb[sheet].values);wb.close();return rows
a=read('615.xlsx','reporte');b=read('Datoshistoricob25.xlsx','Hoja2');m=read('Metas.xlsx','Hoja1')
rows=[];raw=[];ids=Counter();ids25=Counter();missing=Counter();mapping={}
def ingest(data,period):
    heads=[norm(h) for h in data[0]]
    for vals in data[1:]:
        if not any(x is not None for x in vals):continue
        r=dict(zip(heads,vals))
        ident=vals[0] if period=='B25' else r.get('IDENTIFICACION')
        (ids25 if period=='B25' else ids)[str(ident)]+=1
        if period=='B26':
            raw.append(norm(r.get('PERIODO')))
            if norm(r.get('PERIODO'))!='B26' or norm(r.get('HOMOLOGA'))!='NO' or norm(r.get('MATRICULA EN PRIMERO'))!='SI':continue
        elif norm(r.get('PERIODO'))!='B25':continue
        c=career(r.get('CARRERA'));mapping[norm(r.get('CARRERA'))]=c
        d=day(r.get('FECHA MATRICULA') if period=='B26' else r.get('FECHA DE MATRICULA'))
        if not d:missing[period]+=1
        rows.append({'period':period,'sede':norm(r.get('SEDE')),'career':c,'modality':norm(r.get('MODALIDAD')),'date':d,'formal':norm(r.get('FORMALIZADO') if period=='B26' else r.get('FORMALIZADA'))=='SI'})
ingest(a,'B26');ingest(b,'B25')
targets=[];details=[]
for v in m[2:]:
    if not v[1] or not isinstance(v[3],(int,float)):continue
    c=career(v[1]);mod=norm(v[2]);value=int(v[3])
    if c=='GENERAL':continue
    if mod=='GENERAL':targets.append({'career':c,'original':value})
    else:
        sede=next((s for code,s in [('AMB','MATRIZ'),('UIO','QUITO'),('LTG','LATACUNGA')] if re.search(r'\b'+code+r'\b',mod)),None)
        details.append({'career':c,'modality':mod or None,'sede':sede,'target':value})
total=sum(t['original'] for t in targets)
for t in targets:
    x=t['original']*2400/total;t['target']=math.floor(x);t['remainder']=x-t['target']
for t in sorted(targets,key=lambda t:(-t['remainder'],t['career']))[:2400-sum(t['target'] for t in targets)]:t['target']+=1
for t in targets:t.pop('remainder')
assert sum(t['target'] for t in targets)==2400
aggregate=Counter((r['period'],r['sede'],r['career'],r['modality'],r['date'],r['formal']) for r in rows)
records=[dict(zip(['period','sede','career','modality','date','formal'],key),count=count) for key,count in aggregate.items()]
target_careers=set(t['career'] for t in targets)
qa={'rawB26':len(a)-1,'rawPeriods':dict(Counter(raw)),'candidateB26':sum(r['period']=='B26' for r in rows),'totalB25':sum(r['period']=='B25' for r in rows),'duplicateIdentifiersB26':sum(v>1 for v in ids.values()),'duplicateIdentifiersB25':sum(v>1 for v in ids25.values()),'missingDates':dict(missing),'originalTargets':total,'adjustedTargets':2400,'unassignedTargetRows':sum(t['sede'] is None for t in details),'targetDetailRows':len(details),'unmappedCareers':sorted(set(r['career'] for r in rows)-target_careers),'coveredCounts':{p:sum(r['count'] for r in records if r['period']==p and r['career'] in target_careers) for p in ['B25','B26']},'uncoveredCounts':{p:sum(r['count'] for r in records if r['period']==p and r['career'] not in target_careers) for p in ['B25','B26']},'sourceDateRanges':{p:{'start':min(r['date'] for r in rows if r['period']==p and r['date']),'end':max(r['date'] for r in rows if r['period']==p and r['date'])} for p in ['B25','B26']}}
data={'records':records,'targets':targets,'targetDetails':details,'qa':qa,'careerMapping':mapping,'sources':['615.xlsx / reporte','Datoshistoricob25.xlsx / Hoja2','Metas.xlsx / Hoja1'],'snapshot':'2026-09-15'}
(OUT/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
local=ROOT/'data-quality'/'generated';local.mkdir(exist_ok=True)
for name,rr in [('admisiones',records),('metas_carrera',targets),('metas_detalle',details)]:
    with (local/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
(local/'calidad.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(qa,ensure_ascii=True));print('CANONICAL_CAREERS',json.dumps(sorted(set(r['career'] for r in rows)),ensure_ascii=True))
