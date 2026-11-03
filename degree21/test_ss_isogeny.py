from pathlib import Path
from sage.all import *
from compact_records import compact
from unit_arithmetic import lit,decode_record,bits
W=Path(__file__).resolve().parent;s=compact((W/'ss7_127/hecke_jets.m').read_text());r=decode_record(lit(s,'SourceRecords')[0]);R=PolynomialRing(GF(2),'t');F=GF(2**r['F'].d,'a',modulus=R(ZZ(r['F'].p).digits(2)));cv=lambda z:F(R(ZZ(z).digits(2)));E=EllipticCurve([cv(v)for v in r['ainv']]);P=E([cv(v)for v in r['point']]);print(E,127*P,flush=True);ff=E.division_polynomial(7).factor();print([(f.degree(),e)for f,e in ff],flush=True);phi=E.isogeny(ff[0][0]);print(phi,phi(P),flush=True)
