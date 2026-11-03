from pathlib import Path
import json,time,hashlib
from unit_arithmetic import lit
from profile_kernels import Span,profiles,check_profile
W=Path(__file__).resolve().parent;tt=time.monotonic();out=[]
cases=[('relative53',7,13,12,2,3),('full_cusps53',20,0,0,2,3),('relative73',14,6,6,4,5),('relative73_nc',11,9,8,4,5),('relative113',13,7,6,8,5)]
for name,c,bd,br,step,cap in cases:
 p=W/f'{name}_data.m'
 while not p.exists():time.sleep(5)
 # Export marker avoids reading an incompletely written data file.
 while not(W/f'{name}.log').exists()or'EXPORT_COMPLETE'not in(W/f'{name}.log').read_text():time.sleep(5)
 s=p.read_text();SS=lit(s,'RelativeSSMatrices');JC=lit(s,'RelativeCuspJets');m=len(JC);groups=[list(range(o,m,step))for o in range(step)]
 if bd==0:SS=[[[]for row in JC[0]]]
 for si,mat in enumerate(SS):
  B=Span()
  for j in range(bd):B.add(sum(row[j]<<i for i,row in enumerate(mat)))
  assert len(B.b)==br
  cols=[[B.red(sum(JC[k][i][j]<<i for i in range(len(mat))))for j in range(c)]for k in range(m)]
  for pi,pr in enumerate(profiles(m,c,cap)):
   a=check_profile(cols,pr,c,groups,cap);a.update({'case':name,'translate':si,'profile':pi,'caps':pr,'base_degree':bd,'base_rank':br,'columns_sha256':hashlib.sha256(str(cols).encode()).hexdigest()});out.append(a)
   print('S20_RELATIVE_PROFILE',name,si,pi,a['quotient_kernel_dimension'],a['min_unexpected_cost'],a['status'],'seconds',round(time.monotonic()-tt,1),flush=True)
   if a['status']!='PASS':break
  if a['status']!='PASS':break
 (W/f'{name}_profiles_verified.json').write_text(json.dumps({'status':'PASS'if all(a['status']=='PASS'for a in out if a['case']==name)else'FAIL','profiles':[a for a in out if a['case']==name]},indent=2)+'\n')
(W/'relative_profiles_verified.json').write_text(json.dumps({'status':'PASS'if all(a['status']=='PASS'for a in out)else'FAIL','profiles':out},indent=2)+'\n')
