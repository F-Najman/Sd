from pathlib import Path
import json,itertools,random,re
from sage.all import QQ,GF,PolynomialRing,NumberField
W=Path(__file__).resolve().parent;L=Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/models_X1_n');R=PolynomialRing(QQ,'x');x=R.gen();S=PolynomialRing(QQ,('X','Y'));X,Y=S.gens();out=[];rng=random.Random(13)
s=Path('/home/fnajman/webpage_sporadic/data/knowledge/sources/vanhoeij_LowDegreePlaces.txt').read_text()
for N in[41,43]:
 line=next(l for l in s.splitlines()if l.startswith(f'N = {N}, degv = 18,'));body=line.split('[',1)[1].rsplit(']',1)[0];fe,ye=body.replace(' = 0','').split(', ');f=R(fe);YY=PolynomialRing(R,'y');v=R(-YY(ye)[0]/YY(ye)[1]);out.append({'N':N,'polynomial':list(map(str,f.list())),'y_numerator':list(map(str,v.list())),'y_denominator':['1']})
(W/'occurrences.json').write_text(json.dumps(out,indent=2)+'\n')
ms=['SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());']
def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
for a in out:
 ms.append(f"f:={expr(a['polynomial'])};assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq 18;x:=z;y:=Evaluate({expr(a['y_numerator'])},z)/Evaluate({expr(a['y_denominator'])},z);r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and {a['N']}*P eq E!0;print \"S18_OCCURRENCE_VERIFIED prime={a['N']} exact_field_degree=18\";")
ms+=['print "S18_ALL_OCCURRENCES_COMPLETE";quit;'];(W/'verify_occurrences.m').write_text('\n'.join(ms)+'\n')
