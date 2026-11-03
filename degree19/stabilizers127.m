SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree19/sources73.m";
r:=Rep([r:r in AuditSources|not r[7]and r[1]eq 6]);PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);
assert TateNormalForm_xy(E,8*P)eq u;assert TateNormalForm_xy(E,2*P)ne u;assert Min([k:k in[1..72]|2^k mod 73 in[1,72]])eq 9;
print "S19_SS73_GEOMETRIC_STABILIZER_ORDER3_VERIFIED";
load "work/degree19/sources127.m";
for r in[r:r in AuditSources|not r[7]and r[1]eq 14]do
 F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);v:=TateNormalForm_xy(E,2*P);assert &or[v eq[a^(2^k):a in u]:k in[0..13]];
end for;
rr:=[r:r in AuditSources|r[7]and r[1]eq 9 and r[6]eq 7];assert #rr eq 1;r:=rr[1];F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);h:=3^7 mod 127;v:=TateNormalForm_xy(E,h*P);assert &or[v eq[a^(2^k):a in u]:k in[0..8]];
assert Min([k:k in[1..126]|2^k mod 127 in[1,126]])eq 7;assert Min([k:k in[1..126]|h^k mod 127 in[1,126]])eq 9;
assert Min([k:k in[1..136]|2^k mod 137 in[1,136]])eq 34;
print "S19_LEVEL127_STABILIZERS_VERIFIED";print "S19_ALL_STABILIZERS_COMPLETE";quit;
