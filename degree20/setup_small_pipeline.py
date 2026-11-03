from pathlib import Path
import json,subprocess,time,concurrent.futures,re
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;O=W.parent/'degree19';ns=json.loads((W/'local_levels.json').read_text())['levels']
while not'S20_ALL_FINITE_SOURCE_ORBITS_COMPLETE'in(W/'census_sources.log').read_text():time.sleep(5)
jobs=[];sets={}
for n in ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ds=sorted({z[0]for z in rs if z[6]});use={d for d in ds if 20-d in ds}
 if n==139:use|={d for d in ds if any(d+e<=20 for e in ds)}
 if n in[73,89,113,127]:use.add({73:14,89:9,113:13,127:13}[n])
 if not use:continue
 sets[n]=sorted(use);H=W/f'full{n}';inds=[i+1 for i,z in enumerate(rs)if z[6]and z[0]in use]
 src=(O/'full137/stage2_chunk.m').read_text().replace(str(O/'full137'),str(H)).replace(str(O/'sources137.m'),str(W/f'sources{n}.m')).replace('152 div d','320 div d').replace('d le 12 select 8 else 3','N in[97,101]select 16 else 8')
 src=src.replace('if not rec[7] then',f'if not rec[7]or rec[1]notin{sorted(use)} then').replace('/hecke_jets_','/small_jets_');(H/'stage2_small.m').write_text(src)
 for k in range(0,len(inds),8):jobs.append({'N':n,'start':inds[k],'end':inds[min(k+7,len(inds)-1)]})
(W/'small_jet_jobs.json').write_text(json.dumps({'degree_sets':sets,'jobs':jobs},indent=2)+'\n')
print('S20_SMALL_JOBS',len(jobs),sets,flush=True)
def one(j):
 H=W/f"full{j['N']}";log=H/f"small_chunk_{j['start']}.log"
 if not(log.exists()and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in log.read_text()):
  with log.open('w')as f:r=subprocess.run(['magma','-b',f"Start:={j['start']}",f"End:={j['end']}",str(H/'stage2_small.m')],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();assert'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and'Runtime error'not in s,j
 print('S20_SMALL_CHUNK_PASS',j,flush=True);return j
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:done=list(ex.map(one,jobs))
for n in sets:
 H=W/f'full{n}';parts=[]
 for name in['SourceMetadata','SourceRecords','SourceHeckeRecords']:
  vv=[]
  for j in done:
   if j['N']!=n:continue
   s=(H/f"small_jets_{j['start']}.m").read_text();v=s.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');vv.append(v[2:-2].strip())
  parts.append(name+':=[*'+','.join(v for v in vv if v)+'*];')
 (H/'small_hecke_jets.m').write_text('\n'.join(parts)+'\n')
 print('S20_SMALL_LEVEL_READY',n,flush=True)
(W/'small_jet_results.json').write_text(json.dumps({'status':'PASS','jobs':done},indent=2)+'\n');print('S20_ALL_SMALL_JETS_COMPLETE',flush=True)
