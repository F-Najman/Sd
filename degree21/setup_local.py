from pathlib import Path
import json,time
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;O=W.parent/'degree20';ns=json.loads((W/'local_levels.json').read_text())['levels']
while not(W/'census_sources.log').exists()or'S21_ALL_FINITE_SOURCE_ORBITS_COMPLETE'not in(W/'census_sources.log').read_text():time.sleep(5)
jobs=[]
for n in ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ids=[i+1 for i,r in enumerate(rs)if r[6]and(r[0]in[20,21]if n==61 else r[0]==21)]
 for k in range(0,len(ids),8):jobs.append({'N':n,'start':ids[k],'end':ids[min(k+7,len(ids)-1)]})
 parent=W.parent/('degree19'if n==61 else'degree20');s=(O/'match53.m').read_text().replace('work/degree19/sources53.m',f'work/PARENT/sources{n}.m').replace('work/degree20/sources53.m',f'work/degree21/sources{n}.m').replace('work/degree20/inherited','work/degree21/inherited').replace('work/PARENT/',f'work/{parent.name}/').replace('r[1]eq 20',('r[1]ge 20'if n==61 else'r[1]eq 21')).replace('S20_','S21_');(W/f'match{n}.m').write_text(s)
(W/'new_ordinary_jobs.json').write_text(json.dumps(jobs,indent=2)+'\n');print('S21_NEW_JOBS_READY',len(jobs),flush=True)
