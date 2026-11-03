from pathlib import Path
import json,re,itertools
from sage.all import GF,matrix,ZZ
from unit_arithmetic import lit,matbits
W=Path(__file__).resolve().parent;F=GF(2);p=53;s=(W/'full53/units_data.m').read_text();g=int(re.search(r'genus:=(\d+)',s)[1]);prec=int(re.search(r'precision:=(\d+)',s)[1]);root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);assert root==2
Q=matrix(F,[[v>>j&1 for j in range(prec)]for v in matbits(s,'qcoeffs')]);D=matrix(F,[[v>>j&1 for j in range(g)]for v in matbits(s,'DiamondMatrix')]);I=matrix.identity(F,g);kh=next(k for k in range(26)if pow(root,k,p)in[10,43]);AA=[];cut=(p*p-1)//12;C=Q[:,:cut+1];assert C.rank()==g
for q in[3,5]:
 k=next(k for k in range(26)if pow(root,k,p)in[q,p-q]);DQ=D**k*Q;TQ=matrix(F,[[Q[i,q*n]+(DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;AA.append((D**kh-I)*(T-D**k-I))
CJ=[]
for k in range(26):CJ.append((AA[0]*D**k*Q[:,1:20]).stack(AA[1]*D**k*Q[:,1:20]))
native=lit((W/'full_cusps53_data.m').read_text(),'RelativeCuspJets');assert all(CJ[k]==matrix(F,native[k])for k in range(26));cols=[[sum(int(CJ[k][i,j])<<i for i in range(2*g))for j in range(19)]for k in range(26)]
patterns=[list(map(int,l.split()))for l in(W/'FI/FI53_bad_patterns.txt').read_text().splitlines()];assert len(patterns)==7;count=0
for pat in patterns:
 assert len(pat)==13 and sum(pat)==19 and pat[0]==max(pat)
 for aa in itertools.product(*[range(m+1)for m in pat]):
  mult=list(aa)+[m-a for m,a in zip(pat,aa)];rr=[z for k,m in enumerate(mult)for z in cols[k][:m]];assert len(rr)==19 and matrix(F,[ZZ(z).digits(2,padto=2*g)for z in rr]).rank()==19;count+=1
assert count==20444
out={'status':'PASS','all_cotangent_entries_rebuilt':True,'quotient_bad_patterns':7,'lifts_independently_rank_checked':count,'rank':19,'cusp_generator':2};(W/'cusps53_intrinsic_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_CUSPS53_INTRINSIC_AND_LIFT_REPLAY_PASS',count,flush=True)
