SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree20/sources97.m";R97:=AuditSources;
load "work/degree20/sources73.m";R73:=AuditSources;
load "work/degree20/sources109.m";R109:=AuditSources;
load "work/degree20/sources113.m";R113:=AuditSources;
for dat in[<97,16,5^16 mod 97,R97,3,true>,<73,6,8,R73,3,true>,<109,9,93,R109,9,false>,<113,7,4,R113,7,false>,<113,7,98,R113,2,true>]do
 p,d,h,rs,o,fixed:=Explode(dat);r:=Rep([r:r in rs|not r[7]and r[1]eq d]);PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];xy:=TateNormalForm_xy(E,P);assert Min([k:k in[1..p]|h^k mod p in[1,p-1]])eq o;
 if fixed then assert TateNormalForm_xy(E,h*P)eq xy;
 else assert &and[TateNormalForm_xy(E,h^k*P)ne xy:k in[1..o-1]];end if;
 assert &or[TateNormalForm_xy(E,h*P)eq[a^(2^k):a in xy]:k in[0..d-1]];
 printf "S20_RELATIVE_STABILIZER p=%o degree=%o diamond=%o order=%o pointwise_fixed=%o verified=true\n",p,d,h,o,fixed;
end for;print "S20_RELATIVE_STABILIZERS_COMPLETE";quit;
