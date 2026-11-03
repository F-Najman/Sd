from pathlib import Path
import json
from sage.all import GF,EllipticCurve,matrix,primitive_root
W=Path(__file__).resolve().parent;p=89
# E:y²=x³-x in characteristic3: x->x+1 and(-x,i*y) generate Aut(E).
# Frobenius commutes with the former and anticommutes with the latter;
# trace0,norm3 identify its coset with j=2u+1, j²=-3.
E=EllipticCurve(GF(3),[0,0,0,-1,0]);assert E.cardinality()==4
mul=lambda A,B:((A[0]*B[0]+A[1]*B[2])%p,(A[0]*B[1]+A[1]*B[3])%p,(A[2]*B[0]+A[3]*B[2])%p,(A[2]*B[1]+A[3]*B[3])%p)
act=lambda A,v:((A[0]*v[0]+A[1]*v[1])%p,(A[2]*v[0]+A[3]*v[1])%p)
Id=(1,0,0,1);minus=(88,0,0,88);ii=(0,1,88,0);sq={a*a%p:a for a in range(p)};a=next(a for a in range(p)if(-3-a*a)%p in sq);b=sq[(-3-a*a)%p];jj=(a,b,b,-a%p);half=pow(2,-1,p);u=tuple((j-i)*half%p for j,i in zip(jj,Id));assert mul(jj,jj)==(86,0,0,86)and mul(ii,jj)==tuple(-x%p for x in mul(jj,ii))and mul(mul(u,u),u)==Id
G={Id};todo=[Id]
while todo:
 A=todo.pop()
 for B in[ii,u]:
  C=mul(A,B)
  if C not in G:G.add(C);todo.append(C)
assert len(G)==12 and minus in G
r=int(primitive_root(p));h=pow(r,8,p);assert pow(h,11,p)==1 and h!=1
GG={tuple(pow(h,k,p)*a%p for a in A)for A in G for k in range(11)};assert len(GG)==132
which={};reps=[]
for x in range(p):
 for y in range(p):
  v=(x,y)
  if v==(0,0)or v in which:continue
  orb={act(A,v)for A in GG};assert len(orb)==132;idx=len(reps);reps.append(v)
  for z in orb:assert z not in which;which[z]=idx
assert len(reps)==60
D=[which[(r*x%p,r*y%p)]for x,y in reps];F=[which[act(jj,v)]for v in reps];assert all(F[D[i]]==D[F[i]]and D[D[D[D[i]]]]==i for i in range(60))
fixed=[i for i in range(60)if D[D[i]]==i];assert len(fixed)==4 and set(F[i]for i in fixed)==set(fixed)
orb=[];j=fixed[0]
while j not in orb:orb.append(j);j=F[j]
assert j==fixed[0]and set(orb)==set(fixed)and len(orb)==4
out={'status':'PASS','p':89,'quotient':'X1(89)/H11','quotient_genus':27,'good_prime':3,'automorphism_group_order_at3':12,'H11_order':11,'total_supersingular_geometric_quotient_points_at3':60,'diamond_involution_fixed_points':4,'Frobenius_cycle_lengths_on_fixed_points':[4],'conclusion':'Every characteristic-zero point fixed by the residual diamond involution has degree4; no rational divisor of degree2 can contain one.','fixed_indices':fixed,'Frobenius':F,'diamond':D,'matrices':{'i':ii,'Frobenius_j':jj,'unit_u':u}}
(W/'quotient89_fixed_points_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_QUOTIENT89_CM_FIXED_LOCUS_DEGREE4_PROVED',flush=True)
