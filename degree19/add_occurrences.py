from pathlib import Path
import json
from sage.all import QQ,PolynomialRing
W=Path(__file__).resolve().parent;R=PolynomialRing(QQ,'x');s=Path('/home/fnajman/webpage_sporadic/data/knowledge/sources/vanhoeij_LowDegreePlaces.txt').read_text();out=[a for a in json.loads((W/'occurrences.json').read_text())if a['N']<41]
for N in [41,43]:
 l=next(l for l in s.splitlines()if l.startswith(f'N = {N}, degv = 19,'));fe,ye=l.split('[',1)[1].rsplit(']',1)[0].replace(' = 0','').split(', ');f=R(fe);YY=PolynomialRing(R,'y');vv=YY(ye);v=(-vv[0]*vv[1].inverse_mod(f))%f
 out.append({'N':N,'polynomial':list(map(str,f.list())),'y_numerator':list(map(str,v.list())),'y_denominator':['1']})
(W/'occurrences.json').write_text(json.dumps(out,indent=2)+'\n')
ms=['SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());']
def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
for a in out:
 ms.append(f"f:={expr(a['polynomial'])};assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq 19;x:=z;y:=Evaluate({expr(a['y_numerator'])},z)/Evaluate({expr(a['y_denominator'])},z);r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and {a['N']}*P eq E!0;print \"S19_OCCURRENCE_VERIFIED prime={a['N']} exact_field_degree=19\";")
ms+=['print "S19_ALL_OCCURRENCES_COMPLETE";quit;'];(W/'verify_occurrences.m').write_text('\n'.join(ms)+'\n')
print('Explicit examples prepared', [a['N']for a in out])
