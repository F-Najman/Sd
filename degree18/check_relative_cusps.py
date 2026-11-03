from pathlib import Path
import itertools,json,sys,subprocess
W=Path(__file__).resolve().parent;H=W/'FI'
def kernel(rr):
 b={};out=[]
 for i,x in enumerate(rr):
  c=1<<i
  while x:
   k=x.bit_length()-1
   if k in b:y,z=b[k];x^=y;c^=z
   else:b[k]=(x,c);break
  else:out.append(c)
 return len(b),out
out=[]
for p in [103,131]:
 name=f'FI{p}_relative'if p==103 else'FI131'
 if not(H/(name+'.compressed.txt')).exists():subprocess.run(['python',str(W/'compress_FI.py'),str(H/(name+'.txt'))],check=True)
 ls=(H/(name+'.compressed.txt')).read_text().splitlines();_,m,_,_,_,_,d,_=map(int,ls[0].split());assert d==18
 rows=[sum(int(v)<<(64*j)for j,v in enumerate(l.split()))for l in ls[1:]]
 cusp=lambda j,k:rows[:k]if j==0 else rows[d+9*(j-1):d+9*(j-1)+k]
 core=rows[:d]+[v for j in range(1,m)for v in cusp(j,6)];rank,rels=kernel(core);badrels=[]
 for mask in range(1,1<<len(rels)):
  z=0
  for j,v in enumerate(rels):
   if mask>>j&1:z^=v
  cost=[0]*m
  for j in range(len(core)):
   if z>>j&1:
    k,order=(0,j+1)if j<d else(1+(j-d)//6,1+(j-d)%6);cost[k]=max(cost[k],order)
  if sum(cost)<=d:badrels.append(cost)
 assert badrels==[[1]*m],(p,badrels)
 counts={};fail=[]
 for pos in itertools.combinations_with_replacement(range(m),d-m):
  mult=[1+pos.count(j)for j in range(m)];rr=[v for j,k in enumerate(mult)for v in cusp(j,k)];r,_=kernel(rr);counts[r]=counts.get(r,0)+1
  if r!=d-1:fail.append([mult,r])
 assert not fail
 rec={'N':p,'status':'PASS','degree':d,'family_dimension':1,'relative_rank':17,'fixed_cusp_degree':d-m,'cusp_fiber_degree':m,'patterns_checked':sum(counts.values()),'ranks':counts,'sole_small_relation':badrels[0],'kernel_dimension':len(rels)};out.append(rec);(W/f'relative{p}_cusps_verified.json').write_text(json.dumps(rec,indent=2)+'\n');print(rec,flush=True)
(W/'relative_cusps_verified.json').write_text(json.dumps(out,indent=2)+'\n')
