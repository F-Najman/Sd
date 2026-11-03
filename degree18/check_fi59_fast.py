from pathlib import Path
import json,itertools
W=Path(__file__).resolve().parent;H=W/'FI';ls=(H/'FI59.compressed.txt').read_text().splitlines();p,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert(p,m,d)==(59,29,18)
rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]]
def cusp(j,n):return rows[:n]if j==0 else rows[d+9*(j-1):d+9*(j-1)+n]
def kernel(rr):
 b={};rels=[]
 for i,x in enumerate(rr):
  c=1<<i
  while x:
   k=x.bit_length()-1
   if k in b:y,v=b[k];x^=y;c^=v
   else:b[k]=(x,c);break
  else:rels.append(c)
 return len(b),rels
base=[v for j in range(m)for v in cusp(j,4)];labels=[(j,n)for j in range(m)for n in range(1,5)];assert kernel(base)[0]==116
configs=[[(0,18)]]
configs += [[(0,4+a),(j,4+b)]for j in range(1,m)for a,b in[(9,1),(8,2),(7,3),(6,4),(5,5)]]
configs += [[(0,4+a),(j,4+b),(k,4+c)]for j in range(1,m)for k in range(1,m)if j!=k for a,b,c in[(4,1,1),(3,2,1),(2,2,2)]]
count=0;minimum=100;checks=[]
for cfg in configs:
 rr=base[:];lab=labels[:]
 for j,n in cfg:
  rr+=cusp(j,n)[4:];lab +=[(j,k)for k in range(5,n+1)]
 rank,rels=kernel(rr);assert len(rels)<=16
 rel=0;prev=0;mincost=100
 for i in range(1,1<<len(rels)):
  gray=i^(i>>1);change=gray^prev;rel^=rels[change.bit_length()-1];prev=gray;cost=[0]*m;x=rel
  while x:
   bit=x&-x;j,n=lab[bit.bit_length()-1];cost[j]=max(cost[j],n);x^=bit
  c=sum(cost);assert c>18,(cfg,c,cost);mincost=min(mincost,c);count+=1
 minimum=min(minimum,mincost);checks.append({'high_cusps':cfg,'kernel_dimension':len(rels),'minimum_relation_cost':mincost})
core=rows[:d]+[v for j in range(1,m)for v in cusp(j,6)];cr,kr=kernel(core)
out={'N':59,'status':'PASS','degree':18,'method':'independent uniform cap4 block and exhaustive relations on at most three high cusps','uniform_cap4_rows':116,'uniform_cap4_rank':116,'high_configurations':len(configs),'relations_checked':count,'minimum_relation_cost':minimum,'rows_cap6':len(core),'rank_cap6':cr,'kernel_dimension':len(kr),'exceptional_failures':[],'detail':f'PASS high-cusp configurations={len(configs)} relations={count} minimum_cost={minimum}','checks':checks}
(H/'FI59_fast_verified.json').write_text(json.dumps(out,indent=2)+'\n');(H/'FI59_verified.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k!='checks'},flush=True)
