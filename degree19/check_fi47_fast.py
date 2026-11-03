from pathlib import Path
import json,itertools,time
W=Path(__file__).resolve().parent;H=W/'FI';ls=(H/'FI47.compressed.txt').read_text().splitlines();p,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert(p,m,d)==(47,23,19);tt=time.monotonic()
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
base=[v for j in range(m)for v in cusp(j,3)];labels=[(j,n)for j in range(m)for n in range(1,4)];assert kernel(base)[0]==69
configs=[]
def parts(total,k,maximum):
 if k==0:
  if total==0:yield []
  return
 for a in range(min(maximum,total-4*(k-1)),3,-1):
  for tail in parts(total-a,k-1,a):yield[a]+tail
for k in range(1,5):
 for vv in parts(19,k,19):
  for positions in itertools.permutations(range(1,m),k-1):configs.append(list(zip([0]+list(positions),vv)))
count=0;minimum=10000;checks=[]
for ci,cfg in enumerate(configs):
 rr=base[:];lab=labels[:]
 for j,n in cfg:rr+=cusp(j,n)[3:];lab +=[(j,k)for k in range(4,n+1)]
 rank,rels=kernel(rr);assert len(rels)<=18
 rel=0;mincost=10000
 for i in range(1,1<<len(rels)):
  rel^=rels[(i&-i).bit_length()-1];cost=[0]*m;x=rel
  while x:
   bit=x&-x;j,n=lab[bit.bit_length()-1];cost[j]=max(cost[j],n);x^=bit
  c=sum(cost);assert c>19,(cfg,c,cost);mincost=min(mincost,c);count+=1
 minimum=min(minimum,mincost);checks.append({'high_cusps':cfg,'kernel_dimension':len(rels),'minimum_relation_cost':mincost})
 if ci%2000==0:print('S19_FI47_PROGRESS',ci,len(configs),minimum,round(time.monotonic()-tt,1),flush=True)
core=rows[:d]+[v for j in range(1,m)for v in cusp(j,6)];cr,kr=kernel(core)
out={'N':47,'status':'PASS','degree':19,'method':'uniform cap3 and complete relation spaces on at most four high cusps','uniform_rank':69,'profiles':len(configs),'relations_checked':count,'minimum_relation_cost':minimum,'rows_cap6':len(core),'rank_cap6':cr,'kernel_dimension':len(kr),'exceptional_failures':[],'checks':checks}
(H/'FI47_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_FI47_PROFILES_PASS',len(configs),count,minimum,flush=True)
