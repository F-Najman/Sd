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
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree14/sources53.m";ss[53]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree14/sources113.m";ss[113]:=AuditSources;
for dat in[[53,13,1,4],[113,7,4,2],[113,8,7,40]]do
 N,d,orb,h:=Explode(dat);ord:=Min([k:k in[1..N-1]|h^k mod N in[1,N-1]]);assert ord eq (N eq 53 select 13 else (d eq 7 select 14 else 8));
 rr:=[r:r in ss[N]|r[1]eq d and r[6]eq orb];assert #rr eq 1;rec:=rr[1];PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];
 xy:=TateNormalForm_xy(E,P);xyh:=TateNormalForm_xy(E,h*P);assert XYKey(xy[1],xy[2])eq XYKey(xyh[1],xyh[2]);
 printf "S14_STABILIZER N=%o degree=%o orbit=%o diamond=%o order=%o verified=true\n",N,d,orb,h,ord;
end for;print "S14_NEW_STABILIZERS_COMPLETE";quit;
