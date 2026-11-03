from pathlib import Path
import json,itertools
from sage.all import matrix,GF
W=Path(__file__).resolve().parent;H=W/'FI';ls=(H/'FI59.compressed.txt').read_text().splitlines();p,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());rr=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]]
def cusp(j,n):return rr[:n]if j==0 else rr[17+8*(j-1):17+8*(j-1)+n]
base=[v for j in range(29)for v in cusp(j,4)];lab0=[(j,n)for j in range(29)for n in range(1,5)]
def M(rows):return matrix(GF(2),[[v>>j&1 for j in range(512)]for v in rows])
assert M(base).rank()==116
configs=[[(0,17)]]+[[ (0,4+a),(j,4+b)]for j in range(1,29)for a,b in[(8,1),(7,2),(6,3),(5,4)]]+[[ (0,4+a),(j,4+b),(k,4+c)]for j in range(1,29)for k in range(1,29)if j!=k for a,b,c in[(3,1,1),(2,2,1)]]
count=0;minimum=100
for cfg in configs:
 rows=base[:];lab=lab0[:]
 for j,n in cfg:rows+=cusp(j,n)[4:];lab +=[(j,k)for k in range(5,n+1)]
 A=M(rows);K=A.left_kernel();assert K.dimension()<=12;basis=[sum(int(v)<<j for j,v in enumerate(a))for a in K.basis()];x=0;prev=0
 for i in range(1,1<<len(basis)):
  gray=i^(i>>1);x^=basis[(gray^prev).bit_length()-1];prev=gray;z=x;cost=[0]*29
  while z:
   bit=z&-z;j,n=lab[bit.bit_length()-1];cost[j]=max(cost[j],n);z^=bit
  c=sum(cost);assert c>17;minimum=min(minimum,c);count+=1
assert len(configs)==1625 and count==55335 and minimum==58
out={'status':'PASS','independent_uniform_cap4_rank':116,'configurations':1625,'relations':55335,'minimum_relation_cost':58};(H/'FI59_independent.json').write_text(json.dumps(out)+'\n');print('S17_FI59_INDEPENDENT_BLOCK_RANK_PASS',out,flush=True)
