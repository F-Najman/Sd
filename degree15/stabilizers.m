SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
function Code(z)
 if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return[Integers()!a:a in Eltseq(z,GF(2))];end function;
function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;bb:=[1,0];
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;

ss:=AssociativeArray();
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/sources53.m";ss[53]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/sources73.m";ss[73]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/sources109.m";ss[109]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/sources113.m";ss[113]:=AuditSources;
for dat in[[53,13,1,4,13],[73,6,4,2,9],[109,9,3,23,18],[109,12,3,23,18],[113,7,4,2,14],[113,8,7,40,8],[113,7,4,98,2],[113,8,7,98,2],[113,8,28,98,2]]do
 N,d,orb,h,expected:=Explode(dat);ord:=Min([k:k in[1..N-1]|h^k mod N in[1,N-1]]);assert ord eq expected;
 rr:=[r:r in ss[N]|r[1]eq d and r[6]eq orb];assert #rr gt 0;
 for rec in rr do PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];xy:=TateNormalForm_xy(E,P);xyh:=TateNormalForm_xy(E,h*P);assert XYKey(xy[1],xy[2])eq XYKey(xyh[1],xyh[2]);end for;
 printf "S15_STABILIZER N=%o degree=%o orbit=%o diamond=%o order=%o representatives=%o verified=true\n",N,d,orb,h,ord,#rr;
end for;print "S15_ALL_EXCEPTIONAL_STABILIZERS_COMPLETE";quit;
