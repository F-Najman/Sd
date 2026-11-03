from pathlib import Path
import time,json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent
while 'S22_ALL_FINITE_SOURCE_ORBITS_COMPLETE'not in(W/'census_sources.log').read_text():time.sleep(10)
ns=json.loads((W/'local_levels.json').read_text())['levels'];jobs=[];counts=[]
for n in ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');old=lit((W.parent/f'degree21/sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');assert rs[:len(old)]==old
 ids=[i+1 for i,r in enumerate(rs)if r[6]and r[0]==22]
 for k in range(0,len(ids),8):jobs.append({'N':n,'start':ids[k],'end':ids[min(k+7,len(ids)-1)]})
 counts.append({'p':n,'old_sources':len(old),'new_ordinary_sources':len(ids),'new_supersingular_sources':len([r for r in rs[len(old):]if not r[6]])})
(W/'new_ordinary_jobs.json').write_text(json.dumps(jobs,indent=2)+'\n');(W/'source_prefixes_verified.json').write_text(json.dumps({'status':'PASS','results':counts},indent=2)+'\n');print('S22_ORDINARY_JOB_LIST_COMPLETE',len(jobs),flush=True)
