from pathlib import Path
import json,time,subprocess
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;O=W.parent/'degree19';ns=json.loads((W/'local_levels.json').read_text())['levels']
while not((W/'census_sources.log').exists()and'S20_ALL_FINITE_SOURCE_ORBITS_COMPLETE'in(W/'census_sources.log').read_text()):time.sleep(5)
jobs=[]
for n in ns:
 H=W/f'full{n}';H.mkdir(exist_ok=True)
 src=(O/('full137'if n==139 else f'full{n}')/'stage2_chunk.m').read_text()
 src=src.replace(str(O/f'full{137 if n==139 else n}'),str(H)).replace(str(O/f'sources{137 if n==139 else n}.m'),str(W/f'sources{n}.m')).replace('152 div d','160 div d')
 if n!=139:
  if n==137:src=src.replace('if not rec[7] then','if not rec[7]or rec[1]ne 20 then')
  else:src=src.replace('rec[1]ne 19','rec[1]ne 20')
 (H/'stage2_chunk.m').write_text(src)
 records=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');inds=[i+1 for i,r in enumerate(records)if r[6]and(n==139 or r[0]==20)]
 for k in range(0,len(inds),8):jobs.append({'N':n,'start':inds[k],'end':inds[min(k+7,len(inds)-1)]})
 if n!=139:
  s=(O/'match127.m').read_text().replace('work/degree18/','work/PARENT/').replace('work/degree19/','work/degree20/').replace('work/PARENT/','work/degree19/').replace('sources127.m',f'sources{n}.m').replace('r[1]eq 19','r[1]eq 20').replace('S19_','S20_');(W/f'match{n}.m').write_text(s)
(W/'new_ordinary_jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
for name in ['full_sieve.py','pipeline_sieves.py','run_new_ordinary.py']:
 s=(O/name).read_text().replace('S19_','S20_')
 if name=='full_sieve.py':
  s=s.replace('N in[47,53,61]', 'N in[47,53,61,67]').replace('97:{12:1,0:-1}', '97:{7:1,6:-1,1:1,0:-1}')
  s=s.replace('sturm=(N*N-1)//3', 'sturm=(8*g-4 if N==67 else(N*N-1)//3)')
 if name=='pipeline_sieves.py':s=s.replace('n==137 or r[0]==19','n==139 or r[0]==20').replace('max_workers=2','max_workers=1')
 if name=='run_new_ordinary.py':s=s.replace("n,a,b=j['N'],j['start'],j['end'];H=W/f'full{n}';log=H/f'chunk_{a}.log'","n,a,b=j['N'],j['start'],j['end'];H=W/f'full{n}';log=H/f'chunk_{a}.log'\n while not(H/'units_data.m').exists():time.sleep(5)")
 (W/name).write_text(s)
print('S20_LOCAL_PIPELINE_READY',len(jobs),'chunks',flush=True)
ps=[]
for name in ['run_new_ordinary.py','pipeline_sieves.py','run_matches.py']:
 f=(W/name.replace('.py','.log')).open('w');ps.append((subprocess.Popen(['python3',str(W/name)],stdout=f,stderr=subprocess.STDOUT),f))
for p,f in ps:assert p.wait()==0;f.close()
print('S20_NEW_LOCAL_PIPELINE_COMPLETE',flush=True)
