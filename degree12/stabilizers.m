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
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree12/sources73.m";ss[73]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree12/sources109.m";ss[109]:=AuditSources;
for dat in[[73,6,4,2],[109,9,3,23],[109,12,3,23]]do
 N,d,orb,h:=Explode(dat);if N eq 109 then assert Minimum([i:i in[1..54]|((GF(N)!h)^i eq GF(N)!1 or (GF(N)!h)^i eq GF(N)!(-1))])eq 18;end if;AuditSources:=ss[N];rr:=[r:r in AuditSources|r[1]eq d and r[6]eq orb];assert #rr eq 1;rec:=rr[1];PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];
 xy:=TateNormalForm_xy(E,P);xyh:=TateNormalForm_xy(E,h*P);assert XYKey(xy[1],xy[2])eq XYKey(xyh[1],xyh[2]);
 printf "AUDIT_STABILIZER N=%o degree=%o orbit=%o diamond=%o verified=true\n",N,d,orb,h;
end for;
print "S12_EXCEPTIONAL_STABILIZERS_COMPLETE";quit;
