SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");load "work/degree19/sources137.m";
rs:=[r:r in AuditSources|r[7]and r[1]eq 17 and r[6]eq 4];assert #rs gt 0;h:=81;assert Min([k:k in[1..136]|h^k mod 137 in[1,136]])eq 17;
for r in rs do PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);v:=TateNormalForm_xy(E,h*P);assert &or[v eq[a^(2^k):a in u]:k in[0..16]];end for;
assert 2*(19+2)*65536 lt 325*(137^2-1);print "S19_ORDINARY137_STABILIZER_EXCLUSION degree=17 diamond=81 order=17 verified=true";quit;
