from pathlib import Path
import json
from sage.all import QQ,PolynomialRing,prime_range
W=Path(__file__).resolve().parent;R=PolynomialRing(QQ,'x');x=R.gen();out=json.loads((W/'occurrence23.json').read_text())+json.loads((W/'occurrences.json').read_text());s=Path('/home/fnajman/webpage_sporadic/data/knowledge/sources/vanhoeij_LowDegreePlaces.txt').read_text()
for N in[41,43,47]:
 line=next(l for l in s.splitlines()if l.startswith(f'N = {N}, degv = 21,'));body=line.split('[',1)[1].rsplit(']',1)[0];fe,ye=body.replace(' = 0','').split(', ');f=R(fe);YY=PolynomialRing(R,'y');v=R(-YY(ye)[0]*YY(ye)[1].inverse_mod(f))%f;out.append({'N':N,'polynomial':list(map(str,f.list())),'y_numerator':list(map(str,v.list())),'y_denominator':['1']})
assert [a['N']for a in out]==[23,29,31,37,41,43,47]
(W/'occurrences.json').write_text(json.dumps(out,indent=2)+'\n')
ms=['SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());']
def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
for a in out:
 d=len(a['polynomial'])-1;assert 21%d==0
 ms.append(f"f:={expr(a['polynomial'])};assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq {d};x:=z;y:=Evaluate({expr(a['y_numerator'])},z)/Evaluate({expr(a['y_denominator'])},z);r:=(x^2*y-x*y+y-1)/(x^2*y-x);s:=(x*y-y+1)/(x*y);b:=r*s*(r-1);c:=s*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and {a['N']}*P eq E!0;print \"S21_OCCURRENCE_VERIFIED prime={a['N']} exact_field_degree={d}\";")
ms+=['for p in[11,13,17,19]do g:=ExactQuotient((p-5)*(p-7),24);assert 20 gt 2*g-2;end for;assert IsIrreducible(t^21-2);print "S21_ALL_OCCURRENCES_COMPLETE";quit;'];(W/'verify_occurrences.m').write_text('\n'.join(ms)+'\n')
