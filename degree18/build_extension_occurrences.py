from pathlib import Path
import json
from sage.all import QQ,PolynomialRing
W=Path(__file__).resolve().parent;R=PolynomialRing(QQ,'x');s=Path('/home/fnajman/webpage_sporadic/data/knowledge/sources/vanhoeij_LowDegreePlaces.txt').read_text();out=[]
for a in json.loads((W/'occurrence23.json').read_text()):out.append(a|{'field_degree':18})
assert len(out)==1 and out[0]['N']==23
for N in[29,31]:
 l=next(l for l in s.splitlines()if l.startswith(f'N = {N}, degv = 9,'));fe,ye=l.split('[',1)[1].rsplit(']',1)[0].replace(' = 0','').split(', ');f=R(fe);YY=PolynomialRing(R,'y');v=R(-YY(ye)[0]/YY(ye)[1]);out.append({'N':N,'field_degree':9,'polynomial':list(map(str,f.list())),'y_numerator':list(map(str,v.list())),'y_denominator':['1']})
out.append({'N':37,'field_degree':6,'tower':{'x_polynomial':'x^2-x-1','y_polynomial':'y^3+(-4*x-2)*y^2+(6*x+2)*y-x'},'j':-9317})
(W/'extension_occurrences.json').write_text(json.dumps(out,indent=2)+'\n')
ms=['SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());']
def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
for a in out:
 N=a['N'];d=a['field_degree']
 if N!=37:ms.append(f"f:={expr(a['polynomial'])};assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq {d};xx:=z;yy:=Evaluate({expr(a['y_numerator'])},z)/Evaluate({expr(a['y_denominator'])},z);")
 else:ms.append('assert IsIrreducible(t^2-t-1);F<a>:=NumberField(t^2-t-1);S<u>:=PolynomialRing(F);gg:=u^3+(-4*a-2)*u^2+(6*a+2)*u-a;assert IsIrreducible(gg);K<z>:=NumberField(gg);assert AbsoluteDegree(K)eq 6;xx:=K!a;yy:=z;')
 ms.append(f'r:=(xx^2*yy-xx*yy+yy-1)/(xx^2*yy-xx);ss:=(xx*yy-yy+1)/(xx*yy);bb:=r*ss*(r-1);cc:=ss*(r-1);E:=EllipticCurve([1-cc,-bb,-bb,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and {N}*P eq E!0;print "S18_EXTENSION_OCCURRENCE_VERIFIED prime={N} exact_field_degree={d}";')
 if N==37:ms.append('assert jInvariant(E)eq -9317;')
ms.append('print "S18_EXTENSION_OCCURRENCES_COMPLETE";quit;');(W/'verify_extension_occurrences.m').write_text('\n'.join(ms)+'\n')
