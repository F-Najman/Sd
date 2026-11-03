from pathlib import Path
import sys
import json,time,hashlib
from unit_arithmetic import lit
from profile_kernels import Span,profiles,check_profile
W=Path(__file__).resolve().parent
while not(W/'run_relative.log').exists()or'S22_RELATIVE_EXPORTS_COMPLETE'not in(W/'run_relative.log').read_text():time.sleep(5)
cases=[('relative61_o20', 2, 20, 16, 6, 1), ('full_cusps61_sharp', 22, 0, 0, 1, 4), ('full_cusps89', 22, 0, 0, 1, 5), ('full_cusps97_sharp', 22, 0, 0, 1, 5), ('full_cusps71', 22, 0, 0, 0, 4), ('full_cusps127', 22, 0, 0, 1, 5), ('relative61', 7, 15, 12, 6, 3), ('relative61_ss20', 2, 20, 16, 6, 1), ('relative73', 16, 6, 6, 4, 5), ('relative73_nc', 13, 9, 8, 4, 5), ('relative109', 13, 9, 8, 6, 5), ('relative113_ordinary', 14, 8, 7, 7, 5), ('relative97_sharp', 6, 16, 16, 16, 3), ('full_cusps101_sharp', 22, 0, 0, 1, 6)]
for name,c,bd,br,step,cap in cases:
 if len(sys.argv)>1 and name not in sys.argv[1:]:continue
 s=(W/f'{name}_data.m').read_text();SS=lit(s,'RelativeSSMatrices');JC=lit(s,'RelativeCuspJets');m=len(JC);groups=[list(range(o,m,step))for o in range(step)]if step else[];out=[];tt=time.monotonic()
 if not bd:SS=[[[]for row in JC[0]]]
 for si,mat in enumerate(SS):
  B=Span()
  for j in range(bd):B.add(sum(row[j]<<i for i,row in enumerate(mat)))
  assert len(B.b)==br,(name,si,len(B.b),br)
  cols=[[B.red(sum(JC[k][i][j]<<i for i in range(len(mat))))for j in range(c)]for k in range(m)]
  for pi,pr in enumerate(profiles(m,c,cap)):
   a=check_profile(cols,pr,c,groups,cap);a.update({'case':name,'translate':si,'profile':pi,'caps':pr,'base_degree':bd,'base_rank':br,'columns_sha256':hashlib.sha256(str(cols).encode()).hexdigest()});out.append(a)
   if pi%10000==0 or a['status']!='PASS':print('S22_RELATIVE_PROFILE',name,si,pi,a['quotient_kernel_dimension'],a['min_unexpected_cost'],a['status'],round(time.monotonic()-tt,1),flush=True)
   if a['status']!='PASS':break
  if a['status']!='PASS':break
 a={'status':'PASS'if all(r['status']=='PASS'for r in out)else'FAIL','parameters':[c,bd,br,step,cap],'profiles':out};(W/f'{name}_profiles_verified.json').write_text(json.dumps(a,indent=2)+'\n');print('S22_RELATIVE_CASE_FINISHED',name,a['status'],len(out),flush=True)
