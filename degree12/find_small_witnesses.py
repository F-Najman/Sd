from pathlib import Path
import json,itertools,time
from sage.all import PolynomialRing,QQ,GF
W=Path(__file__).resolve().parent;L=Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/models_X1_n');R=PolynomialRing(QQ,'x');x=R.gen();S=PolynomialRing(QQ,('X','Y'));X,Y=S.gens();out=[]
for N in [23,29]:
 s=''.join((L/f'FFFc{N}.txt').read_text().replace('\\','').split()).replace('^','**');F=S(s.replace('x','X').replace('y','Y'));terms=F.dict();dy=int(F.degree(Y));found=False
 pairs=[(R.one(),x+2)]if N==23 else [(R(2),R.one())]if N==29 else []
 if N==31:
  pairs=[(a*x+b,c*x+d)for a,b,c,d in itertools.product(range(-2,3),repeat=4)if a*d-b*c and (c or d)]
  pairs.sort(key=lambda z:sum(abs(t)for f in z for t in f.list()))
 for P,Q in pairs:
  poly=sum(c*x**i*P**j*Q**(dy-j)for (i,j),c in terms.items());fac=poly.factor()
  for f,m in fac:
   if f.degree()!=12:continue
   if f.gcd(Q).degree():continue
   dat={'N':N,'polynomial':[str(c)for c in f.monic().list()],'y_numerator':[str(c)for c in P.list()],'y_denominator':[str(c)for c in Q.list()]};out.append(dat);print('S12_SMALL_WITNESS_FOUND',dat,flush=True);found=True;break
  if found:break
 assert found,N
(W/'small_witnesses.json').write_text(json.dumps(out,indent=2)+'\n')
ms=['SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());']
for a in out:
 def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
 ms.append(f"f:={expr(a['polynomial'])};assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq 12;x:=z;y:=Evaluate({expr(a['y_numerator'])},z)/Evaluate({expr(a['y_denominator'])},z);r:=(x^2*y-x*y+y-1)/(x^2*y-x);s:=(x*y-y+1)/(x*y);b:=r*s*(r-1);c:=s*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and {a['N']}*P eq E!0;print \"S12_OCCURRENCE_VERIFIED prime={a['N']} exact_field_degree=12 exact_point_order=true\";")
ms.append('print "S12_SMALL_EXPLICIT_OCCURRENCES_COMPLETE";quit;');(W/'verify_small_witnesses.m').write_text('\n'.join(ms)+'\n')
