from pathlib import Path
from fractions import Fraction
import json,math
from sage.all import QQ,PolynomialRing,NumberField,matrix
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;s=(W/'odd_anti163_character_norms_data.m').read_text();data=lit(s,'OddAnti163CharacterNormData');expected=lit(s,'OddAnti163TotalNorm');P=PolynomialRing(QQ,'x');out=[];prod=1;dimension=0
for n,f,pol,d,aa,dc,nd in data:
 K=NumberField(P(pol),'z');assert K.degree()==f
 def elt(a):return K([QQ(u)/QQ(v)for u,v in a])
 A=matrix(K,d,d,[elt(a)for a in aa]);det=A.det();assert det==elt(dc);norm=det.norm();assert norm.denominator()==1 and int(norm)%2==1 and norm==nd;prod*=int(norm);dimension+=d*f;out.append({'character_order':n,'coefficient_degree':f,'homology_dimension':d,'norm':str(norm),'odd':True});print('S20_ANTI163_NORM_INDEPENDENT_PASS',n,flush=True)
assert prod==expected and dimension==1980 and prod%2==1
assert next(k for k in range(1,163)if pow(8,k,163)in[1,162])==27
assert 6*20*65536<325*(163**2-1)
(W/'anti163_norms_verified.json').write_text(json.dumps({'status':'PASS','degree':20,'diamond':8,'diamond_order':27,'anti_homology_dimension':dimension,'total_degree_odd':True,'gonality_comparison':'6*20 < 325*(163^2-1)/65536','results':out},indent=2)+'\n');print('S20_GLOBAL163_EXCLUSION_CERTIFIED',flush=True)
