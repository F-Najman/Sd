from pathlib import Path
import sys,json,re,ast,math
from sage.all import GF,matrix,QQ,PolynomialRing,EllipticCurve
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit,matbits
F2=GF(2)
def bm(rr,n):return matrix(F2,[[v>>j&1 for j in range(n)]for v in rr])
a=json.loads((W/'dyadic_jets.json').read_text());assert(a['m'],a['M'],a['p_cutoff'])==(36,181,13032)
for v in a['classes']:
 u=v['u'];rr=[sum((int(n*k%181>90)^int(n*u*pow(k,-1,181)%181>90))<<(k-1)for k in range(1,181))for n in range(1,37)];assert rr==[int(z,16)for z in v['rows']]and bm(rr,180).rank()==36
print('S18_DYADIC_INDEPENDENT_PASS',flush=True)
for n in[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131]:
 stem='FI97_i8'if n==97 else f'FI{n}';ls=(W/'FI'/(stem+'.compressed.txt')).read_text().splitlines();p,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert p==n and d==18;rr=[sum(int(v)<<(64*j)for j,v in enumerate(l.split()))for l in ls[1:]];assert len(rr)==nr and bm(rr,512).rank()==rk
 core=rr[:d]+[v for k in range(m-1)for v in rr[d+9*k:d+9*k+6]];C=bm(core,512);rec=json.loads((W/f'FI/FI{n}_verified.json').read_text());assert rec['rank_cap6']==C.rank()and rec['kernel_dimension']==C.nrows()-C.rank()and not rec['exceptional_failures'];assert rec['status']==('FAIL'if n in[103,131]else'PASS')
 print('S18_FI_INDEPENDENT_PASS',n,flush=True)
# Independently reconstruct the supersingular cotangent maps, entry by entry.
relative=[]
for p,h,sd,rd in[(53,4,13,1),(61,9,15,3),(73,2,6,0)]:
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
 cc=18-sd
 for k,cs in enumerate(CJ):
  Bs=[D**k*A*Q[:,1:cc+1]for A in AA];C0=Bs[0]
  for v in Bs[1:]:C0=C0.stack(v)
  assert C0==matrix(F2,cs)
 Nm=sum((D**(math.gcd(kh,m)*k)for k in range(m//math.gcd(kh,m))),matrix(F2,g,g));assert all(Nm*A==0 for A in AA)
 print('S18_RELATIVE_COTANGENT_INDEPENDENT_PASS',p,flush=True);relative.append(p)
# All Frobenius determinants are recomputed from elliptic curves in Sage.
cnt=0
for line in(W/'quotient_quadratic.log').read_text().splitlines():
 if line.startswith('S18_QUADRATIC_QUOTIENT_EXCLUDED'):
  v=re.fullmatch(r'.*p=(\d+) D=(-?\d+) j=\[([^,]+),([^\]]+)\] split_prime=(\d+) theta=(\d+) trace=(-?\d+) exponent=(\d+) determinant=(\d+)',line);assert v
  p,d,a,b,q,theta,tr,e,det=v.groups();p,d,q,theta,e,det=map(int,[p,d,q,theta,e,det]);a,b=QQ(a),QQ(b);assert(theta*theta-d)%q==0;F=GF(q);j=F(a)+F(b)*theta;E=EllipticCurve(j=j);t=q+1-E.cardinality();T=matrix(GF(p),[[0,1],[-q,t]]);assert int((T**e-1).det())==det!=0;cnt+=1
 elif line.startswith('S18_CM_DEGREE18_EXCLUDED'):
  v=re.fullmatch(r'.*p=(\d+) j=(\d+) q=(\d+) trace=(-?\d+) exponent=(\d+) determinant=(\d+)',line);assert v;p,j,q,t,e,det=map(int,v.groups());F=GF(q);E=(EllipticCurve(QQ,[0,0,1,0,0])if j==0 else EllipticCurve(j=QQ(j)).global_minimal_model());assert E.discriminant().valuation(q)==0;EF=E.change_ring(F);tt=q+1-EF.cardinality();T=matrix(GF(p),[[0,1],[-q,tt]]);assert int((T**e-1).det())==det!=0;cnt+=1
assert cnt==25
out={'status':'PASS','degree':18,'dyadic_rank':36,'dyadic_classes':180,'formal_immersion_levels':18,'supersingular_cotangent_maps_rebuilt':relative,'Frobenius_exclusions_rebuilt':cnt};(W/'auxiliary_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S18_AUXILIARY_INDEPENDENT_CHECKS_PASS',flush=True)
