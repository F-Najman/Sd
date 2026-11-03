from pathlib import Path
from unit_arithmetic import lit
import json,hashlib,itertools,time
W=Path(__file__).resolve().parent;tt=time.monotonic()
def kernel(rows):
 b={};rels=[]
 for i,x in enumerate(rows):
  c=1<<i
  while x:
   k=x.bit_length()-1
   if k in b:y,d=b[k];x^=y;c^=d
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
out=[]
for name,c,base_degree,base_rank in [('relative73',13,6,6),('relative73_nc',10,9,8)]:
 s=(W/f'{name}_data.m').read_text();SS=lit(s,'RelativeSSMatrices');JC=lit(s,'RelativeCuspJets');assert len(JC)==36 and len(SS)==4
 for si,mat in enumerate(SS):
  B=Span()
  for j in range(base_degree):B.add(sum(row[j]<<i for i,row in enumerate(mat)))
  assert len(B.b)==base_rank
  cols=[[B.red(sum(JC[k][i][j]<<i for i in range(len(mat))))for j in range(c)]for k in range(36)]
  profiles=[[c]+[5]*35]
  if c==13:
   for high in range(1,36):
    pr=[7]+[5]*35;pr[high]=6;profiles.append(pr)
  for pi,pr in enumerate(profiles):
   loc=[(k,j)for k,n in enumerate(pr)for j in range(n)];rr=[cols[k][j]for k,j in loc];ix={v:i for i,v in enumerate(loc)}
   fib=[sum(1<<ix[k,j]for k in range(o,36,4))for o in range(4)for j in range(5)]
   for r in fib:
    z=0
    for i,x in enumerate(rr):
     if r>>i&1:z^=x
    assert z==0
   F=Span()
   for r in fib:assert F.add(r)
   rels=kernel(rr);Q=Span();qb=[]
   for r in rels:
    r=F.red(r)
    if Q.add(r):qb.append(r)
   assert len(rels)==20+len(qb)
   assert len(qb)<=18,(name,si,pi,len(qb))
   mins=[];v=0
   for i in range(1,1<<len(qb)):
    v^=qb[(i&-i).bit_length()-1];coeff=[0]*36
    for bit,(k,j)in enumerate(loc):
     if v>>bit&1:coeff[k]|=1<<j
    cost=0
    for o in range(4):cost+=min(sum((coeff[k]^mask).bit_length()for k in range(o,36,4))for mask in range(32))
    mins.append(cost)
   ok=all(v>c for v in mins)
   rec={'case':name,'translate':si,'profile':pi,'caps':pr,'columns':len(rr),'rank':len(rr)-len(rels),'known_fiber_relations':20,'quotient_kernel_dimension':len(qb),'quotient_basis':list(map(hex,qb)),'min_unexpected_cost':min(mins)if mins else None,'classes_checked':len(mins),'columns_sha256':hashlib.sha256(str(rr).encode()).hexdigest(),'status':'PASS'if ok else'FAIL'};out.append(rec)
   print('S19_REL73_PROFILE',name,si,pi,len(qb),min(mins)if mins else None,ok,'seconds',round(time.monotonic()-tt,1),flush=True)
(W/'relative73_relations_verified.json').write_text(json.dumps({'status':'PASS'if all(r['status']=='PASS'for r in out)else'FAIL','profiles':out},indent=2)+'\n')
