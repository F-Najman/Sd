from pathlib import Path
import json,re,time,hashlib
from sage.all import GF,matrix
from unit_arithmetic import lit,matbits,decode_record,xorrows
from profile_kernels import Span,profiles,check_profile
W=Path(__file__).resolve().parent
while not(W/'ss73/hecke_jets.m').exists():time.sleep(5)
raw=(W/'ss73/hecke_jets.m').read_text();r=lit(raw,'SourceRecords');assert len(r)==1;z=decode_record(r[0])['jets'];assert len(z)==187 and len(z[0])>=2
s=(W/'full73/units_data.m').read_text();g=187;prec=int(re.search(r'precision:=(\d+)',s)[1]);F=GF(2);Q=matrix(F,[[v>>j&1 for j in range(prec)]for v in matbits(s,'qcoeffs')]);D=matrix(F,[[v>>j&1 for j in range(g)]for v in matbits(s,'DiamondMatrix')]);root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);I=matrix.identity(F,g);kh=next(k for k in range(36)if pow(root,k,73)in[2,71]);AA=[]
for q in[3,5,7]:
 cut=min(444,(prec-1)//q);C=Q[:,:cut+1]
 if C.rank()<g:continue
 k=next(k for k in range(36)if pow(root,k,73)in[q,73-q]);DQ=D**k*Q;TQ=matrix(F,[[Q[i,q*n]+(DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;AA.append((D**kh-I)*(T-D**k-I))
dat=(W/'relative73_data.m').read_text();SS=lit(dat,'RelativeSSMatrices');CJ=lit(dat,'RelativeCuspJets');assert len(CJ)==36 and len(SS)==4 and len(CJ[0])==g*len(AA)
def bitrows(A):return[sum(int(v)<<j for j,v in enumerate(row))for row in A.rows()]
z0=[v[0]for v in z];z1=[v[1]for v in z];out=[];bases=[]
for offset in[0,1,2]:
 for shift in range(4):
  rr=[]
  for A in AA:
   a=bitrows(A*D**shift);b=bitrows(A*D**(shift+offset))
   for i in range(g):
    v=xorrows(a[i],z0);w=xorrows(a[i],z1)if offset==0 else xorrows(b[i],z0);rr.append(v|(w<<6))
  assert [v&63 for v in rr]==[sum(v<<j for j,v in enumerate(row))for row in SS[shift]]
  BM=matrix(F,[[v>>j&1 for j in range(12)]for v in rr]);assert BM.rank()==12
  B=Span()
  for j in range(12):assert B.add(sum((v>>j&1)<<i for i,v in enumerate(rr)))
  cols=[[B.red(sum(CJ[k][i][j]<<i for i in range(len(rr))))for j in range(8)]for k in range(36)];groups=[list(range(o,36,4))for o in range(4)]
  for pi,pr in enumerate(profiles(36,8,4)):
   a=check_profile(cols,pr,8,groups,4);assert a['status']=='PASS',(offset,a);a.update({'offset':offset,'shift':shift,'caps':pr,'base_rank':12,'relative_rank':20,'profile':pi});out.append(a)
  bases.append({'offset':offset,'shift':shift,'rows':list(map(hex,rr))})
(W/'ss73_double_base_matrices.json').write_text(json.dumps({'bases':bases,'raw_jets_sha256':hashlib.sha256(raw.encode()).hexdigest()},indent=2)+'\n')
(W/'ss73_double_verified.json').write_text(json.dumps({'status':'PASS','degree':20,'supports':'SS6+SS6+C8, including repeated closed point','base_rank':12,'profiles':out,'base_matrices':'ss73_double_base_matrices.json'},indent=2)+'\n');print('S20_SS73_DOUBLE_RELATIVE_PROOF_PASS',len(out),flush=True)
