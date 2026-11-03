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

N:=127;load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree14/sources127.m";total:=0;orbits:=0;
assert Min([k:k in[1..126]|2^k mod 127 in[1,126]])eq 7;assert Min([k:k in[1..126]|3^k mod 127 in[1,126]])eq 63;
for rec in AuditSources do
 if rec[7]then continue;end if;assert rec[1]eq 14;PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];
 assert #Seqset([TateNormalForm_xy(E,(2^k)*P):k in[0..6]])eq 7;
 xy:=TateNormalForm_xy(E,P);uv:=TateNormalForm_xy(E,2*P);assert XYKey(xy[1],xy[2])eq XYKey(uv[1],uv[2]);total+:=rec[6];orbits+:=1;
 printf "S14_QUOTIENT127_SS_ORBIT degree=%o closed_points=%o fixed_by_diamond2=true\n",rec[1],rec[6];
end for;assert total eq 48 and orbits eq 6;pointsF4:=2*total;gon:=Ceiling(pointsF4/5);assert gon eq 20 and gon gt 7*2;assert 325*(127^2-1)/65536 gt 5*14;
printf "S14_QUOTIENT127_COMPLETE H_order=7 quotient_diamond_order=9 closed_degree2_points=%o F4_point_lower_bound=%o gonality_lower_bound=%o\n",total,pointsF4,gon;quit;
