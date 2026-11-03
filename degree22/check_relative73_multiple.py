from pathlib import Path
import itertools,json
from unit_arithmetic import lit
from profile_kernels import Span,profiles,check_profile
W=Path(__file__).resolve().parent;s=(W/'relative73_multiple_data.m').read_text();SS=lit(s,'SS73ClosedJets');NC=lit(s,'SS73NC');JC=lit(s,'SS73CuspJets');groups=[list(range(i,36,4))for i in range(4)];cases=[]
for cnt,c,cap in [(2,10,4)]:
 for pos in itertools.combinations_with_replacement(range(4),cnt):
  counts={i:pos.count(i)for i in set(pos)};base=[[a for i,m in counts.items()for a in SS[i][r][:6*m]]for r in range(len(SS[0]))];expected=16 if cnt==3 and len(counts)==1 else 6*cnt;cases.append((f'SS{cnt}',pos,base,expected,c,cap))
for i,j in itertools.product(range(4),repeat=2):cases.append(('SS_NC',(i,j),[SS[i][r][:6]+NC[j][r]for r in range(len(SS[0]))],14,7,3))
out=[]
for name,pos,base,br,c,cap in cases:
 B=Span()
 for j in range(len(base[0])):B.add(sum(row[j]<<i for i,row in enumerate(base)))
 assert len(B.b)==br,(name,pos,len(B.b),br)
 cols=[[B.red(sum(JC[k][i][j]<<i for i in range(len(base))))for j in range(c)]for k in range(36)]
 for pi,pr in enumerate(profiles(36,c,cap)):
  a=check_profile(cols,pr,c,groups,cap);a.update({'case':name,'positions':pos,'base_rank':br,'base_degree':len(base[0]),'cusp_degree':c,'cap':cap,'profile':pi,'caps':pr});out.append(a);print('S22_SS73_MULTIPLE_PROFILE',name,pos,br,a['quotient_kernel_dimension'],a['min_unexpected_cost'],a['status'],flush=True)
  if a['status']!='PASS':break
assert len(out)==376
(W/'relative73_multiple_verified.json').write_text(json.dumps({'status':'PASS'if all(r['status']=='PASS'for r in out)else'FAIL','profiles':out},indent=2)+'\n')
