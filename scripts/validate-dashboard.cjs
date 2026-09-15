const vm=require('vm'),fs=require('fs'),assert=require('assert');
const src=fs.readFileSync('dist/app.js','utf8').replace(/init\(\);\s*$/,'');
const ctx=vm.createContext({Intl,Date,Map,Set,Math,console,document:{getElementById:()=>({value:''})}});
vm.runInContext(src+'\nDATA='+fs.readFileSync('dist/data.json','utf8')+';',ctx);
const s={scope:'target',sede:'',career:'',modality:'',formal:'',start25:'2025-05-01',end25:'2025-09-30',start26:'2026-05-01',end26:'2026-09-30',cutoff:'2026-09-15'};
function run(filters){return vm.runInContext('metrics('+JSON.stringify(filters)+')',ctx);}
const m=run(s);
assert.equal(m.meta,2400);
assert.equal(m.elapsed,138);
assert.equal(m.duration,153);
assert.equal(m.daysLeft,15);
const sedes=['MATRIZ','QUITO','LATACUNGA'].map(sede=>run({...s,sede}));
assert.equal(sedes.reduce((a,x)=>a+x.real,0),m.real);
assert.equal(sedes.reduce((a,x)=>a+x.ytd,0),m.ytd);
assert.ok(run({...s,formal:'yes'}).real<=m.real);
assert.equal(run({...s,sede:'QUITO',career:'DERECHO'}).meta,0);
assert.equal(run({...s,modality:'EN LINEA'}).meta,null);
assert.equal(run({...s,scope:'all'}).meta,null);
assert.equal(run({...s,scope:'uncovered'}).meta,null);
assert.equal(run({...s,cutoff:'2026-04-30'}).real,0);
assert.equal(run({...s,cutoff:'2026-04-30'}).projection,null);
const careers=vm.runInContext('[...new Set(DATA.targets.map(x=>x.career))]',ctx);
const byCareer=careers.map(career=>run({...s,career}));
assert.equal(byCareer.reduce((a,x)=>a+x.meta,0),2400);
assert.equal(byCareer.reduce((a,x)=>a+x.real,0),m.real);
assert.equal(byCareer.reduce((a,x)=>a+x.ytd,0),m.ytd);
for(const view of ['overview','matrix','forecast','quality']){
  assert.ok(vm.runInContext(view+'('+JSON.stringify(s)+',metrics('+JSON.stringify(s)+'))',ctx).includes('<'));
}
console.log(JSON.stringify({checks:'PASS',real:m.real,ytd:m.ytd,finalB25:m.final,meta:m.meta,projection:m.projection,sedes:sedes.map(x=>({real:x.real,meta:x.meta})),careerCount:careers.length}));
