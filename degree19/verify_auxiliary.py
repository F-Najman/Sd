from pathlib import Path
import sys,json,re,ast,math
from sage.all import GF,matrix,QQ,PolynomialRing,EllipticCurve
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit,matbits
F2=GF(2)
def bm(rr,n):return matrix(F2,[[v>>j&1 for j in range(n)]for v in rr])
a=json.loads((W/'dyadic_jets.json').read_text());assert(a['m'],a['M'],a['p_cutoff'])==(38,181,13756)
for v in a['classes']:
 u=v['u'];rr=[sum((int(n*k%181>90)^int(n*u*pow(k,-1,181)%181>90))<<(k-1)for k in range(1,181))for n in range(1,39)];assert rr==[int(z,16)for z in v['rows']]and bm(rr,180).rank()==38
print('S19_DYADIC_INDEPENDENT_PASS',flush=True)
# Independently reconstruct the supersingular cotangent maps, entry by entry.
relative=[]
for p,h,sd,rd in[(53,10,13,1),(61,9,15,3),(73,2,6,0)]:
 s=(W/f'full{p}/units_data.m').read_text();g=int(re.search(r'genus:=(\d+)',s)[1]);prec=int(re.search(r'precision:=(\d+)',s)[1]);root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);m=(p-1)//2
 Q=bm(matbits(s,'qcoeffs'),prec);D=bm(matbits(s,'DiamondMatrix'),g);I=matrix.identity(F2,g);assert D**m==I;kh=next(k for k in range(m)if pow(root,k,p)in[h,p-h]);AA=[]
 for q in([3,5]if p==53 else([3]if p==61 else[3,5,7])):
  cut=min((p*p-1)//12,(prec-1)//q);C=Q[:,:cut+1]
  if C.rank()<g:continue
  k=next(k for k in range(m)if pow(root,k,p)in[q,p-q]);DQ=D**k*Q;TQ=matrix(F2,[[Q[i,q*n]+(DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;AA.append((D**kh-I)*(T-D**k-I))
 rs=lit((W/f'sources{p}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');r=next(r for r in rs if not r[6]and r[0]==sd);PR=PolynomialRing(F2,'t');F=GF(2**sd,name='a',modulus=PR(r[1]));aa=[F(PR(v))for v in r[2]];x,y=[F(PR(v))for v in r[3]];a1,a2,a3,a4,a6=aa
 u3=a3+a1*x;u2=x+a2;u4=x*x+a4+a1*y;v2=u2+(u4/u3)**2+a1*u4/u3;b=v2**3/u3**2;c=(a1*v2+u3)/u3;rv=b/c;sv=c*c/(b+c);tv=rv*sv+1;xu=(sv+rv)/tv;yu=tv/(sv*sv+sv+rv+1)
 RX=bm(matbits(s,'UnitXRelations'),2*g);RY=bm(matbits(s,'UnitYRelations'),2*g);RM=matrix(F,[[F(row[j])+u*F(row[g+j])for j in range(g)]for R,u in[(RX,xu),(RY,yu)]for row in R.rows()]);assert RM.rank()==g-1;z=RM.right_kernel().basis()[0];z/=next(v for v in z if v)
 dat=(W/f'relative{p}_data.m').read_text();SS=lit(dat,'RelativeSSMatrices');CJ=lit(dat,'RelativeCuspJets');assert len(SS)==r[5]
 for k,ssmat in enumerate(SS):
  zk=D.change_ring(F)**k*z;Bs=[]
  for A in AA:
   v=A.change_ring(F)*zk;Bs.append(matrix(F2,[list(a.polynomial())+[0]*(sd-len(list(a.polynomial())))for a in v]))
  C0=Bs[0]
  for v in Bs[1:]:C0=C0.stack(v)
  assert C0==matrix(F2,ssmat)and C0.rank()==sd-rd
 cc=19-sd
 for k,cs in enumerate(CJ):
  Bs=[D**k*A*Q[:,1:cc+1]for A in AA];C0=Bs[0]
  for v in Bs[1:]:C0=C0.stack(v)
  assert C0==matrix(F2,cs)
 Nm=sum((D**(math.gcd(kh,m)*k)for k in range(m//math.gcd(kh,m))),matrix(F2,g,g));assert all(Nm*A==0 for A in AA)
 print('S19_RELATIVE_COTANGENT_INDEPENDENT_PASS',p,flush=True);relative.append(p)
out={'status':'PASS','degree':19,'dyadic_rank':38,'dyadic_classes':180,'relative_maps_rebuilt':relative};(W/'auxiliary_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_AUXILIARY_INDEPENDENT_CHECKS_PASS',flush=True)
