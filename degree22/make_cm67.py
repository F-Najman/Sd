from pathlib import Path
import json
from sage.all import QQ,PolynomialRing,NumberField
W=Path(__file__).resolve().parent
P=PolynomialRing(QQ,'z');z=P.gen();K=NumberField(z*z+z+1,'zeta');zeta=K.gen()
R=PolynomialRing(K,'u');u=R.gen();F=R.fraction_field()
r3=lambda v:(v**3-96*v**2+48*v+64)/(9*v*(v+4)**2)
a=r3(F(u));r9=a*r3(F(u)*a**3);r2=(F(u)-8)/(4*(F(u)+1));f=(r9-zeta*r2).numerator()
print('S22_CM67_KERNEL_POLYNOMIAL_DEGREE',f.degree(),flush=True)
facs=[g.monic()for g,e in f.factor()if g.degree()==11];assert len(facs)==1
h=facs[0];hbar=R([K([c[0]-c[1],-c[1]])for c in h.list()]);g=h*hbar;Q=PolynomialRing(QQ,'u');g=Q([QQ(c)for c in g.list()]);assert g.degree()==22 and g.is_irreducible()
(W/'cm67.json').write_text(json.dumps({'prime':67,'degree':22,'polynomial':list(map(str,g.list())),'curve':'Y^2=X^3+u^2/(u+1)^3','point':['u/(u+1)','u/(u+1)'],'construction':'x(9P)=zeta*x(2P) on Y^2=X^3+1, degree11 horizontal factor over Q(zeta3)'},indent=2)+'\n')
print('S22_CM67_EXACT_FIELD_FOUND',flush=True)
