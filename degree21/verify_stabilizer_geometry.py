"""Actual geometric orbit lengths for every formal fixed/pullback family."""
from pathlib import Path
import json,math
from sage.all import GF,PolynomialRing,vector
from intrinsic_model import Model,units,PR
W=Path(__file__).resolve().parent;out=[]
def norm(z):return z/next(a for a in z if a)
def check(M,sd,ordinary,orb,h,expected=None):
 F,z,o=M.point(sd,ordinary,orb);H=M.D**M.log(h);hm=M.m//math.gcd(M.m,M.log(h));HF=H.change_ring(F);v=z
 for k in range(1,hm+1):
  v=norm(HF*v)
  if v==z:break
 assert k<=hm and(hm%k==0)
 if expected is not None:assert k==expected,(M.p,sd,o,h,k,expected)
 assert any(norm(HF*z)==vector(F,[a**(2**j)for a in z])for j in range(sd)),(M.p,sd,o,h,'not closed invariant')
 r={'p':M.p,'degree':sd,'ordinary':ordinary,'closed_diamond_orbit':o,'diamond':h,'diamond_order':hm,'geometric_point_orbit':k};out.append(r);print('S21_STABILIZER_GEOMETRY_PASS',r,flush=True)
for p in[53,61,73,97,109,113,127,137]:
 M=Model(p)
 if p==53:check(M,13,False,1,10,13)
 elif p==61:
  check(M,15,False,1,3,5);check(M,20,False,1,3,5)
 elif p==73:
  check(M,6,False,4,2,3)
  for orb in[1,2,4]:check(M,18,False,orb,2)
 elif p==97:check(M,16,False,2,pow(M.root,16,p),1)
 elif p==109:
  check(M,9,False,3,93,9)
  for sd in[9,12]:check(M,sd,False,3,pow(M.root,3,p))
 elif p==113:
  check(M,8,True,7,40,8);check(M,8,True,7,pow(M.root,28,p));check(M,7,False,4,pow(M.root,4,p))
 elif p==127:
  check(M,9,True,7,pow(M.root,7,p),9)
  check(M,14,False,3,pow(M.root,9,p),7);check(M,14,False,3,pow(M.root,21,p),1)
 elif p==137:
  check(M,17,True,4,pow(M.root,4,p),17);check(M,17,False,2,pow(M.root,2,p))
(W/'stabilizer_geometry_verified.json').write_text(json.dumps({'status':'PASS','all_required_formal_orbits_verified':True,'results':out},indent=2)+'\n');print('S21_ALL_STABILIZER_GEOMETRY_COMPLETE',flush=True)
