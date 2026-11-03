from pathlib import Path
import json,subprocess,concurrent.futures,sys
W=Path(__file__).resolve().parent;P=W.parent/'degree21';sys.path.insert(0,str(W));from unit_arithmetic import lit
jobs=[];sets={};oldpieces={}
for n in json.loads((W/'local_levels.json').read_text())['levels']:
 r=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ds={v[0]for v in r if v[6]};use={d for d in ds if 22-d in ds};use|={59:{7,8},61:{7,8},71:{7,8},73:{13,16},89:{11},109:{13},113:{15},127:{15}}.get(n,set())
 if not use:continue
 sets[n]=sorted(use);H=W/f'full{n}';old=P/f'full{n}/small_hecke_jets.m';oldtext=old.read_text()if old.exists()else'';oldids={z[0]for z in lit(oldtext,'SourceMetadata')}if oldtext else set();oldpieces[n]=oldtext
 for z in lit(oldtext,'SourceMetadata')if oldtext else[]:
  v=r[z[0]-1];assert (v[0],v[5],v[4])==z[1:]
 ids=[i+1 for i,v in enumerate(r)if v[6]and v[0]in use and i+1 not in oldids]
 s=(W/'full139/stage2_chunk.m').read_text().replace('full139/',f'full{n}/').replace('sources139.m',f'sources{n}.m').replace('if not rec[7]or rec[1]ne 22 then',f'if not rec[7]or si notin {ids} then').replace('jprec:=Min(d le 12 select 8 else 3,168 div d)','jprec:=Min(N in[59,61,71,73,97,101]select 16 else 8,672 div d)').replace('/hecke_jets_','/small_jets_');(H/'stage2_small.m').write_text(s)
 for k in range(0,len(ids),8):jobs.append({'N':n,'start':ids[k],'end':ids[min(k+7,len(ids)-1)]})
(W/'small_jet_jobs.json').write_text(json.dumps({'degree_sets':sets,'jobs':jobs},indent=2)+'\n');print('S22_SMALL_JETS_READY',len(jobs),sets,flush=True)
def one(j):
 H=W/f"full{j['N']}";log=H/f"small_chunk_{j['start']}.log"
 with log.open('w')as f:r=subprocess.run(['magma','-b',f"Start:={j['start']}",f"End:={j['end']}",str(H/'stage2_small.m')],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(x in s for x in['Runtime error','User error','Assertion failed']),j
 print('S22_SMALL_CHUNK_PASS',j,flush=True);return j
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:done=list(ex.map(one,jobs))
for n in sets:
 H=W/f'full{n}';parts=[];texts=([oldpieces[n]]if oldpieces[n]else[])+[(H/f"small_jets_{j['start']}.m").read_text()for j in done if j['N']==n]
 for name in['SourceMetadata','SourceRecords','SourceHeckeRecords']:
  vals=[]
  for s in texts:
   v=s.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');vals.append(v[2:-2].strip())
  parts.append(name+':=[*'+','.join(v for v in vals if v)+'*];')
 (H/'small_hecke_jets.m').write_text('\n'.join(parts)+'\n')
(W/'small_jet_results.json').write_text(json.dumps({'status':'PASS','jobs':done},indent=2)+'\n');print('S22_SMALL_JETS_COMPLETE',flush=True)
