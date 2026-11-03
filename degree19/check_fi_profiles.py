from pathlib import Path
import json,itertools,sys,time
W=Path(__file__).resolve().parent;H=W/'FI';tt=time.monotonic()
def kernel(rr):
 b={};rels=[]
 for i,x in enumerate(rr):
  c=1<<i
  while x:
   k=x.bit_length()-1
   if k in b:y,v=b[k];x^=y;c^=v
   else:b[k]=(x,c);break
  else:rels.append(c)
 return rels
class Span:
 def __init__(self):self.b={}
 def red(self,x):
  for k,v in sorted(self.b.items(),reverse=True):
   if x>>k&1:x^=v
  return x
 def add(self,x):
  x=self.red(x)
  if x:self.b[x.bit_length()-1]=x;return True
  return False
for n in map(int,sys.argv[1:]):
 stem='FI97_i8'if n==97 else f'FI{n}';ls=(H/(stem+'.compressed.txt')).read_text().splitlines();p,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert p==n and d==19
 rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]];assert len(rows)==nr and len(kernel(rows))==nr-rk
 def cusp(j,k):return rows[:k]if j==0 else rows[d+9*(j-1):d+9*(j-1)+k]
 configs=[[(0,19)]]+[[ (0,a),(j,b)]for j in range(1,m)for a,b in [(13,6),(12,7),(11,8),(10,9)]]+[[ (0,7),(j,6),(k,6)]for j in range(1,m)for k in range(1,m)if j!=k]
 base=[x for j in range(m)for x in cusp(j,5)];labs=[(j,k)for j in range(m)for k in range(1,6)];checks=[];bad=[];minimum=10000;cnt=0
 for pi,cfg in enumerate(configs):
  rr=base[:];lab=labs[:]
  for j,k in cfg:rr+=cusp(j,k)[5:];lab +=[(j,t)for t in range(6,k+1)]
  rels=kernel(rr);qb=rels;F=Span();fib=[]
  if n in[103,131]:
   ix={v:i for i,v in enumerate(lab)};fib=[sum(1<<ix[j,k]for j in range(m))for k in range(1,6)]
   for r in fib:
    x=0
    for k,v in enumerate(rr):
     if r>>k&1:x^=v
    assert x==0 and F.add(r)
   Q=Span();qb=[]
   for r in rels:
    r=F.red(r)
    if Q.add(r):qb.append(r)
   assert len(rels)==5+len(qb)
  assert len(qb)<=22,(n,cfg,len(qb))
  v=0;mincost=10000
  for i in range(1,1<<len(qb)):
   v^=qb[(i&-i).bit_length()-1];coeff=[0]*m;x=v
   while x:
    bit=x&-x;j,k=lab[bit.bit_length()-1];coeff[j]|=1<<(k-1);x^=bit
   cost=min(sum((a^mask).bit_length()for a in coeff)for mask in range(32))if fib else sum(a.bit_length()for a in coeff)
   cnt+=1;mincost=min(mincost,cost)
   if cost<=19:bad.append({'profile':pi,'caps':cfg,'cost':cost,'relation':hex(v)})
  minimum=min(minimum,mincost);checks.append({'profile':pi,'high_cusps':cfg,'kernel_dimension':len(rels),'quotient_kernel_dimension':len(qb),'minimum_relation_cost':mincost if qb else None})
  if pi%500==0:print('S19_FI_PROFILE_PROGRESS',n,pi,len(configs),'minimum',minimum,'bad',len(bad),'seconds',round(time.monotonic()-tt,1),flush=True)
 core=rows[:d]+[v for j in range(1,m)for v in cusp(j,6)];rels=kernel(core)
 out={'N':n,'degree':19,'status':'PASS_RELATIVE'if fib and not bad else('PASS'if not bad else'FAIL'),'method':'complete relation spaces on uniform cap5 and at most three high cusps','profiles':len(configs),'relations_checked':cnt,'minimum_unexpected_relation_cost':minimum,'rows_cap6':len(core),'rank_cap6':len(core)-len(rels),'kernel_dimension':len(rels),'exceptional_failures':bad,'checks':checks}
 (H/f'FI{n}_profiles_verified.json').write_text(json.dumps(out,indent=2)+'\n');(H/f'FI{n}_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_FI_PROFILES_DONE',n,out['status'],'profiles',len(configs),'relations',cnt,'mincost',minimum,flush=True)
