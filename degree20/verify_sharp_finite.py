from pathlib import Path
from sage.all import QQ,PolynomialRing,NumberField,matrix
import json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;data=lit((W/'sharp_finite_data.m').read_text(),'SharpFiniteData');out=[];R=PolynomialRing(QQ,'x')
for p,n,r,q,pol,d,w,u,rk in data:
 K=NumberField(R(pol),'z')
 def elt(a):return K([QQ(b)/QQ(c)for b,c in a])
 A=matrix(K,d,d,[elt(a)for a in w]);B=matrix(K,d,d,[elt(a)for a in u]);assert A.rank()==rk==d-1 and A.stack(B).rank()==rk
 out.append({'p':p,'character_order':n,'diamond':r,'hecke_prime':q,'dimension':d,'winding_rank':rk,'status':'PASS'})
assert len(out)==8
(W/'sharp_finite_verified.json').write_text(json.dumps({'status':'PASS','independent_exact_number_field_ranks':out},indent=2)+'\n');print('S20_SHARP_FINITE_INDEPENDENT_PASS',len(out),flush=True)
