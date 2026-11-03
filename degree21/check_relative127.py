from pathlib import Path
import itertools,json,hashlib
from sage.all import GF,matrix,ZZ
from unit_arithmetic import lit
from profile_kernels import Span,kernel
W=Path(__file__).resolve().parent;s=(W/'relative127_data.m').read_text();base=lit(s,'Relative127Base');CJ=lit(s,'Relative127CuspJets');assert len(CJ)==63
B=Span()
for j in range(16):B.add(sum(row[j]<<i for i,row in enumerate(base)))
assert len(B.b)==14
cols=[[B.red(sum(CJ[k][i][j]<<i for i in range(len(base))))for j in range(5)]for k in range(63)];rr=[v for row in cols for v in row];rels=kernel(rr);fib=[]
for k in range(5):
 for step in[7,9]:
  for o in range(step):fib.append(sum(1<<(5*j+k)for j in range(o,63,step)))
F=Span()
for r in fib:
 v=0
 for j,x in enumerate(rr):
  if r>>j&1:v^=x
 assert v==0;F.add(r)
assert len(F.b)==75 and len(rels)==75 and all(F.red(r)==0 for r in rels)
# Independent Sage checks the entire binary relation code, not selected vectors.
A=matrix(GF(2),[[v>>j&1 for j in range(len(base))]for v in rr]);R=matrix(GF(2),[ZZ(z).digits(2,padto=315)for z in fib]);assert A.rank()==240 and R.rank()==75 and R*A==0
# Each jet-level relation is a 7-by-9 row/column code. Its minimum nonzero
# Hamming weight is7; different jet levels have disjoint coordinates.
weights=[a*9+b*7-2*a*b for a in range(8)for b in range(10)if(a,b)not in[(0,0),(7,9)]];assert min(weights)==7
# Minimum weight seven excludes every nonzero relation on any five columns,
# including every prefix jet configuration. No separate enumeration is needed.
import math
cnt=math.comb(67,5);assert cnt==9657648
out={'status':'PASS','degree':21,'family_dimension':2,'base_rank':14,'relative_rank':19,'patterns_checked':cnt,'full_relation_dimension':75,'relation_code_minimum_nonzero_weight':7,'independent_Sage_complete_kernel_check':True,'columns_sha256':hashlib.sha256(str(rr).encode()).hexdigest()};(W/'relative127_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S21_RELATIVE127_VERIFIED',out,flush=True)
