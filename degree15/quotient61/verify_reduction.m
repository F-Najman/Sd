SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree15/sources61.m";
rr:=[r:r in AuditSources|not r[7]];assert #rr eq 1;r:=rr[1];assert r[1]eq 15 and r[6]eq 1;
PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];assert P ne E!0 and 61*P eq E!0;uv:=TateNormalForm_xy(E,P);assert LCM([Degree(MinimalPolynomial(a,GF(2))):a in uv])eq 15;
for h in[2,3,4]do vv:=TateNormalForm_xy(E,h*P);ks:=[k:k in[0..14]|vv eq [a^(2^k):a in uv]];assert #ks eq 1;printf "S15_SS61_CLOSED_STABILIZER diamond=%o Frobenius_exponent=%o\n",h,ks[1];if h eq 4 then assert GCD(ks[1],15)eq 1;end if;end for;
print "S15_SS61_REDUCTION_AND_TRANSITIVE_H15_ACTION_COMPLETE";quit;
