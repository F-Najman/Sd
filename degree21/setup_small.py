from pathlib import Path
import json,subprocess,concurrent.futures
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;O=W.parent/'degree20';jobs=[];sets={}
for n in json.loads((W/'local_levels.json').read_text())['levels']:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ds={r[0]for r in rs if r[6]};totals=[20,21]if n==61 else[21];use={d for d in ds if any(t-d in ds for t in totals)}
 if n in[59,61,67,71,73]:use.add(7)
 use|={73:{12,15},89:{10},109:{12},113:{14},127:{14}}.get(n,set())
 if not use:continue
 sets[n]=sorted(use);H=W/f'full{n}';src=(O/'full53/stage2_chunk.m').read_text().replace(str((O/'full53').resolve()),str(H.resolve())).replace(str((O/'sources53.m').resolve()),str((W/f'sources{n}.m').resolve())).replace('jprec:=Min(N eq 101 select 4 else 3,160 div d)','jprec:=Min(N in[59,61,67,71,73,97,101]select 16 else 8,672 div d)').replace('if not rec[7]or rec[1]ne 20 then',f'if not rec[7]or rec[1]notin{sorted(use)} then').replace('/hecke_jets_','/small_jets_');(H/'stage2_small.m').write_text(src);ids=[i+1 for i,r in enumerate(rs)if r[6]and r[0]in use]
 for k in range(0,len(ids),8):jobs.append({'N':n,'start':ids[k],'end':ids[min(k+7,len(ids)-1)]})
(W/'small_jet_jobs.json').write_text(json.dumps({'degree_sets':sets,'jobs':jobs},indent=2)+'\n');print('S21_SMALL_JETS_READY',len(jobs),sets,flush=True)
def one(j):
 H=W/f"full{j['N']}";log=H/f"small_chunk_{j['start']}.log"
 with log.open('w')as f:r=subprocess.run(['magma','-b',f"Start:={j['start']}",f"End:={j['end']}",str(H/'stage2_small.m')],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(x in s for x in ['Runtime error','User error','Assertion failed']),j
 print('S21_SMALL_CHUNK_PASS',j,flush=True);return j
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:done=list(ex.map(one,jobs))
for n in sets:
 H=W/f'full{n}';parts=[]
 for name in ['SourceMetadata','SourceRecords','SourceHeckeRecords']:
  vals=[]
  for j in done:
   if j['N']==n:
    s=(H/f"small_jets_{j['start']}.m").read_text();v=s.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');vals.append(v[2:-2].strip())
  parts.append(name+':=[*'+','.join(v for v in vals if v)+'*];')
 (H/'small_hecke_jets.m').write_text('\n'.join(parts)+'\n')
(W/'small_jet_results.json').write_text(json.dumps({'status':'PASS','jobs':done},indent=2)+'\n');print('S21_SMALL_JETS_COMPLETE',flush=True)
