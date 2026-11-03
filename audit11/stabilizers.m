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

root:="/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/";
ss:=AssociativeArray();
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/sources37.m";ss[37]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/sources67.m";ss[67]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/sources71.m";ss[71]:=AuditSources;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/sources73.m";ss[73]:=AuditSources;
for dat in[[37,6,3,8],[37,9,2,4],[37,9,1,4],[37,10,9,6],[67,9,11,38],[71,7,5,32],[73,6,4,2]]do
 N,d,orb,h:=Explode(dat);AuditSources:=ss[N];rr:=[r:r in AuditSources|r[1]eq d and r[6]eq orb];assert #rr eq 1;rec:=rr[1];PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];
 xy:=TateNormalForm_xy(E,P);xyh:=TateNormalForm_xy(E,h*P);assert XYKey(xy[1],xy[2])eq XYKey(xyh[1],xyh[2]);
 printf "AUDIT_STABILIZER N=%o degree=%o orbit=%o diamond=%o verified=true\n",N,d,orb,h;
end for;
AuditSources:=ss[37];PF<t>:=PolynomialRing(GF(2));f:=t^10+t^8+t^7+t^4+t^3+t+1;gp:=t^8+t^6+t^5+t^2+t+1;F<a>:=ext<GF(2)|f>;x:=a;y:=Evaluate(gp,a);r:=(x^2*y+x*y+y+1)/(x^2*y+x);s:=(x*y+y+1)/(x*y);b:=r*s*(r+1);c:=s*(r+1);E:=EllipticCurve([1+c,-b,0-b,0,0]);P:=E![0,0];assert 37*P eq E!0 and P ne E!0;assert TateNormalForm_xy(E,P)eq[x,y];key:=XYKey(x,y);
matches:=[];for i in[1..#AuditSources]do rec:=AuditSources[i];if rec[1]ne 10 then continue;end if;FF:=ext<GF(2)|PF!rec[2]>;EE:=EllipticCurve([FF!PF!a:a in rec[3]]);PP:=EE![FF!PF!a:a in rec[4]];oo:={XYKey(xy[1],xy[2])where xy:=TateNormalForm_xy(EE,k*PP):k in[1..36]};if key in oo then Append(~matches,i);end if;end for;assert matches eq[12];
printf "AUDIT37_DECIC_WITNESS_MATCH source=12 verified=true\n";
print "AUDIT_ALL_STABILIZERS_AND_WITNESS_MATCH_COMPLETE";quit;
