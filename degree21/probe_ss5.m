SetQuitOnError(true);SetColumns(0);load "work/degree21/sources127.m";
for r in[r:r in AuditSources|not r[7]and r[1]eq 14]do
 PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);print "S21_SS127_5_FACTORS",r[6],[Degree(a[1]):a in Factorization(DivisionPolynomial(E,5))];
end for;quit;
