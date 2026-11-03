from pathlib import Path
import json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;Ns=json.loads((W/'local_levels.json').read_text())['levels']+[163];out=[]
for n in Ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ds=sorted({z[0]for z in rs if z[6]});ss=sorted({z[0]for z in rs if not z[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',d)for d in ds]+[('SS',d)for d in ss]+([('NC',nc)]if nc<=22 else[]);cases=[]
 def walk(start,left,s):
  cases.append({'support':[list(v)for v in s],'cusp_complement':left})
  for j in range(start,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],s+[types[j]])
 walk(0,22,[]);out.append({'p':n,'ordinary_degrees':ds,'supersingular_degrees':ss,'NC_degree':nc,'types':[list(v)for v in types],'cases':cases});print('S22_SUPPORT_INVENTORY',n,len(cases),'ordinary',ds,'SS',ss,'NC',nc,flush=True)
(W/'support_inventory.json').write_text(json.dumps({'status':'COMPLETE_INVENTORY','degree':22,'levels':out,'support_types':sum(len(a['cases'])for a in out)},indent=2)+'\n')
