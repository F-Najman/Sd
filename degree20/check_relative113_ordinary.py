from pathlib import Path
import json,time,hashlib
from unit_arithmetic import lit
from profile_kernels import Span,profiles,check_profile
W=Path(__file__).resolve().parent;out=[]
for name,c,bd,br,step,cap in [('relative113_ordinary',12,8,7,7,5)]:
 s=(W/f'{name}_data.m').read_text();SS=lit(s,'RelativeSSMatrices');JC=lit(s,'RelativeCuspJets');m=len(JC);groups=[list(range(o,m,step))for o in range(step)]
 if bd==0:SS=[[[]for row in JC[0]]]
 for si,mat in enumerate(SS):
  B=Span()
  for j in range(bd):B.add(sum(row[j]<<i for i,row in enumerate(mat)))
  assert len(B.b)==br
  cols=[[B.red(sum(JC[k][i][j]<<i for i in range(len(mat))))for j in range(c)]for k in range(m)]
  for pi,pr in enumerate(profiles(m,c,cap)):
   a=check_profile(cols,pr,c,groups,cap);a.update({'case':name,'translate':si,'profile':pi,'caps':pr,'base_degree':bd,'base_rank':br,'columns_sha256':hashlib.sha256(str(cols).encode()).hexdigest()});out.append(a)
   print('S20_SHARP_PROFILE',name,si,pi,a['quotient_kernel_dimension'],a['min_unexpected_cost'],a['status'],flush=True)
   if a['status']!='PASS':break
  if a['status']!='PASS':break
 (W/f'{name}_profiles_verified.json').write_text(json.dumps({'status':'PASS'if all(a['status']=='PASS'for a in out if a['case']==name)else'FAIL','profiles':[a for a in out if a['case']==name]},indent=2)+'\n')
(W/'ordinary113_relative_verified.json').write_text(json.dumps({'status':'PASS'if all(a['status']=='PASS'for a in out)else'FAIL','profiles':out},indent=2)+'\n')
