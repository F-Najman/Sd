"""Rebuild native relative cotangents using Sage and the integral canonical model."""
from pathlib import Path
import sys,re,json,math,time
from sage.all import GF,matrix,PolynomialRing,vector
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W))
from unit_arithmetic import lit,matbits
F2=GF(2);PR=PolynomialRing(F2,'t');start=time.monotonic();results=[]
def bm(rows,n):return matrix(F2,[[v>>j&1 for j in range(n)]for v in rows])
def units(aa,x,y):
 a1,a2,a3,a4,a6=aa;u3=a3+a1*x;u2=x+a2;u4=x*x+a4+a1*y
 v2=u2+(u4/u3)**2+a1*u4/u3;b=v2**3/u3**2;c=(a1*v2+u3)/u3
 rv=b/c;sv=c*c/(b+c);tv=rv*sv+1
 return (sv+rv)/tv,tv/(sv*sv+sv+rv+1)
class Model:
 def __init__(self,p):
  self.p=p;s=(W/f'full{p}/units_data.m').read_text();self.g=g=int(re.search(r'genus:=(\d+)',s)[1]);self.prec=prec=int(re.search(r'precision:=(\d+)',s)[1]);self.root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);self.m=(p-1)//2
  self.Q=bm(matbits(s,'qcoeffs'),prec);self.D=bm(matbits(s,'DiamondMatrix'),g);self.I=matrix.identity(F2,g)
  assert self.D**self.m==self.I
  self.RX=bm(matbits(s,'UnitXRelations'),2*g);self.RY=bm(matbits(s,'UnitYRelations'),2*g);self.cache={}
  self.sources=lit((W/f'sources{p}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
 def log(self,a):return next(k for k in range(self.m)if pow(self.root,k,self.p)in[a,self.p-a])
 def hecke(self,q):
  if q in self.cache:return self.cache[q]
  cut=min((self.p*self.p-1)//12,(self.prec-1)//q);C=self.Q[:,:cut+1]
  if C.rank()<self.g:self.cache[q]=None;return None
  DQ=self.D**self.log(q)*self.Q
  TQ=matrix(F2,[[self.Q[i,q*n]+(F2(q)*DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(self.g)])
  T=C.solve_left(TQ);assert T*C==TQ;self.cache[q]=T;return T
 def operators(self,h,qs):
  return [(self.D**self.log(h)-self.I)*(self.hecke(q)-self.D**self.log(q)-F2(q)*self.I)for q in qs if self.hecke(q)is not None]
 def cv(self,F,xy):
  R=matrix(F,[[F(v[j])+u*F(v[self.g+j])for j in range(self.g)]for M,u in zip([self.RX,self.RY],xy)for v in M.rows()])
  assert R.rank()==self.g-1;z=R.right_kernel().basis()[0];return z/next(a for a in z if a)
 def point(self,sd,ordinary=False,orbit=None):
  r=next(r for r in self.sources if bool(r[6])==ordinary and r[0]==sd and(orbit is None or r[5]==orbit))
  F=GF(2**sd,name='a',modulus=PR(r[1]));aa=[F(PR(v))for v in r[2]];x,y=[F(PR(v))for v in r[3]]
  return F,self.cv(F,units(aa,x,y)),r[5]
def stack(xs):
 a=xs[0]
 for b in xs[1:]:a=a.stack(b)
 return a
def coeff(v,d):return matrix(F2,[list(x.polynomial())+[0]*(d-len(list(x.polynomial())))for x in v])
def compare(M,name,AA,sd=0,br=0,ordinary=False,orbit=None,nc=False):
 dat=(W/f'{name}_data.m').read_text();SS=lit(dat,'RelativeSSMatrices');CJ=lit(dat,'RelativeCuspJets');c=21-sd
 if sd:
  if nc:
   F=GF(2**sd,name='a',modulus=PR(lit(dat,'RelativeNCPolynomial')));a=F(PR(lit(dat,'RelativeNCZeta')));assert a.multiplicative_order()==M.p
   z=M.cv(F,units([F(1),F(0),F(0),F(0),F(0)],a/(1+a)**2,a*a/(1+a)**3));assert z==vector(F,[F(PR(v))for v in lit(dat,'RelativeNCZ')]);orb=len(SS)
  else:F,z,orb=M.point(sd,ordinary,orbit)
  assert len(SS)==orb
  for k,rr in enumerate(SS):
   zk=M.D.change_ring(F)**k*z;B=stack([coeff(A.change_ring(F)*zk,sd)for A in AA]);assert B==matrix(F2,rr)and B.rank()==br,(name,k)
 for k,rr in enumerate(CJ):assert stack([A*M.D**k*M.Q[:,1:c+1]for A in AA])==matrix(F2,rr),(name,k,'cusp')
 a={'case':name,'status':'PASS','all_entries_rebuilt':True,'operators':len(AA),'base_degree':sd,'base_rank':br,'translates':len(SS),'cusp_blocks':len(CJ)};results.append(a)
 print('S21_INTRINSIC_REBUILD_PASS',name,'seconds',round(time.monotonic()-start,1),flush=True)
