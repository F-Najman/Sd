SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
Cases:=[<43,12,7,37>,<43,15,7,37>,<43,14,1,2>,<43,14,3,2>,<53,13,1,4>,<61,15,1,3>,<73,6,4,2>,<97,16,2,64>,<97,16,2,25>,<109,9,3,23>,<109,12,3,23>,<113,7,4,2>,<113,8,7,40>,<113,8,7,98>,<113,8,28,98>,<113,7,4,98>];
Sources:=AssociativeArray();
load "work/degree16/sources43.m";Sources[43]:=AuditSources;
load "work/degree16/sources53.m";Sources[53]:=AuditSources;
load "work/degree16/sources61.m";Sources[61]:=AuditSources;
load "work/degree16/sources73.m";Sources[73]:=AuditSources;
load "work/degree16/sources97.m";Sources[97]:=AuditSources;
load "work/degree16/sources109.m";Sources[109]:=AuditSources;
load "work/degree16/sources113.m";Sources[113]:=AuditSources;
for dat in Cases do
 N,d,o,h:=Explode(dat);rs:=[r:r in Sources[N]|r[1]eq d and r[6]eq o];assert #rs gt 0;
 for rr in rs do
  PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rr[2]>;E:=EllipticCurve([F!PF!a:a in rr[3]]);P:=E![F!PF!a:a in rr[4]];u:=TateNormalForm_xy(E,P);v:=TateNormalForm_xy(E,h*P);assert &or[v eq[a^(2^k):a in u]:k in[0..d-1]];
 end for;printf "S16_STABILIZER p=%o degree=%o orbit=%o diamond=%o representatives=%o verified=true\n",N,d,o,h,#rs;
end for;
assert Min([k:k in[1..88]|2^k mod 89 in[1,88]])eq 11;
assert Min([k:k in[1..192]|2^k mod 193 in[1,192]])eq 48;
assert Min([k:k in[1..12]|2^k mod 193 in[Integers()!((GF(193)!5)^(12*j)):j in[0..15]]])eq 6;
print "S16_ALL_STABILIZERS_COMPLETE";quit;
