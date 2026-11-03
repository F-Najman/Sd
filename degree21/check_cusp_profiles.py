from pathlib import Path
import json,time,sys
from profile_kernels import profiles,check_profile,kernel
W=Path(__file__).resolve().parent;H=W/'FI';start=time.monotonic()
for n in map(int,sys.argv[1:]):
 stem='FI97_i8'if n==97 else f'FI{n}';ls=(H/(stem+'.compressed.txt')).read_text().splitlines();p,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert p==n and d==21
 rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]];assert len(rows)==nr and len(kernel(rows))==nr-rk
 cols=[rows[:d]]+[rows[d+10*(j-1):d+10*j]for j in range(1,m)];cap=4 if n==59 else 5;groups=[list(range(m))]if n in[103,131]else[];checks=[]
 for pi,pr in enumerate(profiles(m,d,cap)):
  a=check_profile(cols,pr,d,groups,cap);a.update({'profile':pi,'caps':pr});checks.append(a)
  if pi%100==0 or a['status']!='PASS':print('S21_CUSP_PROFILE',n,pi,a['quotient_kernel_dimension'],a['min_unexpected_cost'],a['status'],'seconds',round(time.monotonic()-start,1),flush=True)
  if a['status']!='PASS':break
 out={'status':'PASS_RELATIVE'if groups and all(a['status']=='PASS'for a in checks)else('PASS'if all(a['status']=='PASS'for a in checks)else'FAIL'),'N':n,'degree':d,'profiles':checks,'method':'complete profile relation spaces','known_groups':groups};(H/f'FI{n}_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S21_CUSP_PROFILE_DONE',n,out['status'],len(checks),flush=True)
