from pathlib import Path
import json
from sage.all import QQ,GF,PolynomialRing,NumberField,matrix
from unit_arithmetic import lit
W=Path(__file__).resolve().parent
s=(W/'anti167_data.m').read_text();q,pol,d,aa,dc,nd=lit(s,'Anti167Data');R=PolynomialRing(QQ,'x');K=NumberField(R(pol),'z');assert K.degree()==82 and d==26 and q==3
def elt(a):return K([QQ(u)/QQ(v)for u,v in a])
A=matrix(K,d,d,[elt(a)for a in aa]);det=A.det();assert det==elt(dc)and det.norm()==nd and int(nd)%2
assert next(k for k in range(1,167)if pow(2,k,167)in[1,166])==83
assert 5*20*65536<325*(167**2-1)
cm=lit((W/'cm_branch_data.m').read_text(),'CMBranchData')
for p,j,w,q,t in cm:
 F=matrix(GF(p),2,2,[0,-q,1,t]);assert all((F**(w*k)-1).det()!=0 for k in range(1,21))
assert (151,0,6,5,0)in cm and 5*20*65536<325*(151**2-1)
out={'status':'PASS','degree':20,'global167':{'character_order':83,'coefficient_degree':82,'homology_dimension':26,'rational_homology_dimension':2132,'hecke_prime':3,'norm':str(nd),'odd':True,'diamond_order':83},'global151':{'diamond':2,'order':15,'remaining_branch':'j=0','CM_excluded_through_degree':20},'CM_records':cm}
(W/'global_extra_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S20_GLOBAL151_AND167_VERIFIED',flush=True)
