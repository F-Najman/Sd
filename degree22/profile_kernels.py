"""Complete binary relation spaces on dominating multiplicity profiles."""
import itertools
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
def profiles(m,c,cap):
 """Move a maximal multiplicity to cusp0; dominate every high partition."""
 yield[c]+[cap]*(m-1)
 for h in range(2,c//(cap+1)+1):
  def parts(left,slots,upper):
   if slots==0:
    if left==0:yield[]
    return
   for a in range(min(upper,left-(slots-1)*(cap+1)),cap,-1):
    for z in parts(left-a,slots-1,a):yield[a]+z
  for pp in parts(c,h,c):
   for pos in itertools.permutations(range(1,m),h-1):
    if len(set(pp[1:]))==1 and tuple(sorted(pos))!=pos:continue
    pr=[cap]*m;pr[0]=pp[0]
    for j,a in zip(pos,pp[1:]):pr[j]=a
    yield pr
def check_profile(cols,pr,c,groups=(),cap=5):
 m=len(cols);loc=[(j,k)for j,a in enumerate(pr)for k in range(a)];rr=[cols[j][k]for j,k in loc];ix={v:i for i,v in enumerate(loc)};fib=[sum(1<<ix[j,k]for j in orb)for orb in groups for k in range(cap)];F=Span()
 for r in fib:
  assert F.add(r);z=0
  for i,x in enumerate(rr):
   if r>>i&1:z^=x
  assert z==0
 rels=kernel(rr);Q=Span();qb=[]
 for r in rels:
  r=F.red(r)
  if Q.add(r):qb.append(r)
 assert len(rels)==len(fib)+len(qb)
 assert len(qb)<=22,(pr,len(qb))
 mins=[];v=0;covered={j for orb in groups for j in orb}
 for i in range(1,1<<len(qb)):
  v^=qb[(i&-i).bit_length()-1];coeff=[0]*m
  for bit,(j,k)in enumerate(loc):
   if v>>bit&1:coeff[j]|=1<<k
  cost=sum(coeff[j].bit_length()for j in range(m)if j not in covered)
  for orb in groups:cost+=min(sum((coeff[j]^mask).bit_length()for j in orb)for mask in range(1<<cap))
  mins.append(cost)
 return{'status':'PASS'if all(a>c for a in mins)else'FAIL','columns':len(rr),'rank':len(rr)-len(rels),'known_fiber_relations':len(fib),'quotient_kernel_dimension':len(qb),'quotient_basis':list(map(hex,qb)),'min_unexpected_cost':min(mins)if mins else None,'classes_checked':len(mins)}
