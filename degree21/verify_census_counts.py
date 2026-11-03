"""Independent ordinary class-number and supersingular quaternion counts.

For odd t, Schoof, Families of curves and weight distributions of codes,
Proposition5.2, gives H(t^2-4q) ordinary isomorphism classes over F_q.
H is enumerated directly by reduced integral quadratic forms, with no GRH.
For E:y^2+y=x^3, End(E) is the Hurwitz order. Its24 units act on E[p];
Frobenius is a norm2 element, in the unique unit coset represented by i+j.
Thus the calculation below gives its action on all supersingular X1(p)
points without elliptic-curve torsion or twist enumeration.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from sage.all import primitive_root
import json,math,time,hashlib
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;tt=time.monotonic();ns=json.loads((W/'local_levels.json').read_text())['levels'];maxa=math.isqrt((4*2**21)//3);roots=[None]
for a in range(1,maxa+1):
 d={}
 for b in range(-a+1,a+1):d.setdefault(b*b%(4*a),[]).append(b)
 roots.append(d)
@lru_cache(None)
def H(D):
 assert D<0 and D%4 in[0,1];total=0
 for a in range(1,math.isqrt((-D)//3)+1):
  for b in roots[a].get(D%(4*a),[]):
   c=(b*b-D)//(4*a)
   if c>=a and(c!=a or b>=0):total+=1
 return total
assert[H(d)for d in[-7,-15,-39,-55,-63]]==[1,2,4,4,5]
for f in range(1,22):
 q=2**f;s=math.isqrt(4*q);assert sum(H(t*t-4*q)for t in range(-s,s+1)if t%2)==2*(q-1)
print('S21_CLASS_NUMBER_TOTALS_VERIFIED',H.cache_info(),flush=True)
def supersingular(p):
 def mul(A,B):
  a,b,c,d=A;e,f,g,h=B
  return((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)
 def act(A,v):return((A[0]*v[0]+A[1]*v[1])%p,(A[2]*v[0]+A[3]*v[1])%p)
 def inv(A):
  a,b,c,d=A;k=pow((a*d-b*c)%p,-1,p);return(d*k%p,-b*k%p,-c*k%p,a*k%p)
 Id=(1,0,0,1);minus=(p-1,0,0,p-1);ii=(0,1,p-1,0);sq={b*b%p:b for b in range(p)};a=next(a for a in range(p)if(-1-a*a)%p in sq);b=sq[(-1-a*a)%p];jj=(a,b,b,-a%p);ij=mul(ii,jj);half=pow(2,-1,p);u=tuple((x+y+z+w)*half%p for x,y,z,w in zip(Id,ii,jj,ij));assert mul(ii,ii)==mul(jj,jj)==minus
 G={Id};todo=[Id]
 while todo:
  A=todo.pop()
  for B in[ii,jj,u]:
   C=mul(A,B)
   if C not in G:G.add(C);todo.append(C);assert len(G)<=24
 assert len(G)==24 and minus in G
 Fro=tuple((x+y)%p for x,y in zip(ii,jj));assert mul(Fro,Fro)==(p-2,0,0,p-2)and all(mul(mul(Fro,A),inv(Fro))in G for A in G)
 which=[-1]*(p*p);reps=[]
 for index in range(1,p*p):
  if which[index]!=-1:continue
  v=divmod(index,p);orb={act(A,v)for A in G};assert len(orb)==24
  for x,y in orb:assert which[x*p+y]==-1;which[x*p+y]=len(reps)
  reps.append(v)
 assert len(reps)==(p*p-1)//24
 F=[which[x*p+y]for x,y in[act(Fro,v)for v in reps]];r=int(primitive_root(p));D=[which[(r*x%p)*p+r*y%p]for x,y in reps];assert all(F[D[i]]==D[F[i]]for i in range(len(reps)))
 cycles=[];closed=[-1]*len(reps)
 for i in range(len(reps)):
  if closed[i]!=-1:continue
  cyc=[];j=i
  while closed[j]==-1:closed[j]=len(cycles);cyc.append(j);j=F[j]
  assert j==i;cycles.append(cyc)
 dc=[closed[D[v[0]]]for v in cycles];seen=set();types=[]
 for i in range(len(cycles)):
  if i in seen:continue
  j=i;orb=[]
  while j not in seen:seen.add(j);orb.append(j);j=dc[j]
  assert j==i and all(len(cycles[j])==len(cycles[i])for j in orb);types.append((len(cycles[i]),len(orb)))
 return sorted(types),Counter(map(len,cycles))
out=[]
for p in ns:
 text=(W/f'sources{p}.m').read_text();rs=lit(text.replace('true','True').replace('false','False'),'AuditSources');ss,cycles=supersingular(p);assert sorted((r[0],r[5])for r in rs if not r[6])==[v for v in ss if v[0]<=21],p
 ordinary=[];m=(p-1)//2;nc=next(f for f in range(1,p)if pow(2,f,p)in[1,p-1]);g=(p-5)*(p-7)//24
 for f in range(1,22):
  q=2**f;s=math.isqrt(4*q);t=-s+(q+1+s)%p
  if t%2==0:t+=p
  traces=list(range(t,s+1,2*p));assert all((q+1-t)%p==0 and t%2 for t in traces)
  # The following necessary full-p-torsion conditions never occur in this range.
  full=[t for t in traces if(q-1)%p==0 and(q+1-t)%(p*p)==0 and(t-2)%p==0];assert all((t*t-4*q)%(p*p)==0 for t in full)
  predicted=m*(sum(H(t*t-4*q)for t in traces)+p*sum(H((t*t-4*q)//(p*p))for t in full));observed=sum(r[0]*r[5]for r in rs if r[6]and f%r[0]==0);assert predicted==observed,(p,f,predicted,observed)
  ss_points=sum(d*c for d,c in cycles.items()if f%d==0);cusps=m*(1+int(f%nc==0));assert(observed+ss_points+cusps-q-1)**2<=4*g*g*q
  ordinary.append({'degree':f,'rational_ordinary_points':observed,'trace_class_numbers':[[t,H(t*t-4*q)]for t in traces],'full_p_torsion_class_numbers':[[t,H((t*t-4*q)//(p*p))]for t in full]})
 out.append({'p':p,'status':'PASS','ordinary_counts':ordinary,'supersingular_closed_diamond_orbits':ss,'source_sha256':hashlib.sha256(text.encode()).hexdigest()});print('S21_CENSUS_INDEPENDENT_COUNTS_PASS',p,'seconds',round(time.monotonic()-tt,1),flush=True)
result={'status':'PASS','degree':21,'ordinary_method':'unconditional reduced quadratic forms and Schoof Proposition5.2','supersingular_method':'24 Hurwitz units and Frobenius coset i+j on Fp^2 minus0','results':out};(W/'census_counts_independent.json').write_text(json.dumps(result,indent=2)+'\n');print('S21_CENSUS_COUNTS_INDEPENDENT_COMPLETE',len(out),flush=True)
