SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
Cases:=[<53,13,1,4>,<73,6,4,2>,<73,18,4,2>,<73,18,2,2>,<73,18,1,2>,<97,16,2,64>,<109,9,3,23>,<109,12,3,23>,<113,7,4,2>,<113,8,7,40>,<113,8,7,98>,<113,8,28,98>,<113,7,4,98>,<137,17,2,2>];
Sources:=AssociativeArray();

load "work/degree20/sources53.m";Sources[53]:=AuditSources;

load "work/degree20/sources73.m";Sources[73]:=AuditSources;
load "work/degree20/sources97.m";Sources[97]:=AuditSources;
load "work/degree20/sources109.m";Sources[109]:=AuditSources;
load "work/degree20/sources113.m";Sources[113]:=AuditSources;
load "work/degree20/sources137.m";Sources[137]:=AuditSources;
for dat in Cases do
 N,d,o,h:=Explode(dat);rs:=[r:r in Sources[N]|r[1]eq d and r[6]eq o];assert #rs gt 0;
 for rr in rs do
  PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rr[2]>;E:=EllipticCurve([F!PF!a:a in rr[3]]);P:=E![F!PF!a:a in rr[4]];u:=TateNormalForm_xy(E,P);v:=TateNormalForm_xy(E,h*P);assert &or[v eq[a^(2^k):a in u]:k in[0..d-1]];
 end for;printf "S20_STABILIZER p=%o degree=%o orbit=%o diamond=%o representatives=%o verified=true\n",N,d,o,h,#rs;
end for;
assert Min([k:k in[1..88]|2^k mod 89 in[1,88]])eq 11;


load "work/degree20/sources73.m";
r:=Rep([r:r in AuditSources|not r[7]and r[1]eq 6]);PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);
assert TateNormalForm_xy(E,8*P)eq u;assert TateNormalForm_xy(E,2*P)ne u;assert Min([k:k in[1..72]|2^k mod 73 in[1,72]])eq 9;
print "S20_SS73_GEOMETRIC_STABILIZER_ORDER3_VERIFIED";
load "work/degree20/sources127.m";
for r in[r:r in AuditSources|not r[7]and r[1]eq 14]do
 F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);v:=TateNormalForm_xy(E,2*P);assert &or[v eq[a^(2^k):a in u]:k in[0..13]];
end for;
rr:=[r:r in AuditSources|r[7]and r[1]eq 9 and r[6]eq 7];assert #rr eq 1;r:=rr[1];F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);h:=3^7 mod 127;v:=TateNormalForm_xy(E,h*P);assert &or[v eq[a^(2^k):a in u]:k in[0..8]];
assert Min([k:k in[1..126]|2^k mod 127 in[1,126]])eq 7;assert Min([k:k in[1..126]|h^k mod 127 in[1,126]])eq 9;
assert Min([k:k in[1..136]|2^k mod 137 in[1,136]])eq 34;
print "S20_LEVEL127_STABILIZERS_VERIFIED";

load "work/degree20/sources137.m";
rs:=[r:r in AuditSources|r[7]and r[1]eq 17 and r[6]eq 4];assert #rs gt 0;h:=81;assert Min([k:k in[1..136]|h^k mod 137 in[1,136]])eq 17;
for r in rs do PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];u:=TateNormalForm_xy(E,P);v:=TateNormalForm_xy(E,h*P);assert &or[v eq[a^(2^k):a in u]:k in[0..16]];end for;
assert 2*(20+3)*65536 lt 325*(137^2-1);print "S20_ORDINARY137_STABILIZER_EXCLUSION degree=17 diamond=81 order=17 verified=true";

print "S20_ALL_STABILIZERS_COMPLETE";quit;
