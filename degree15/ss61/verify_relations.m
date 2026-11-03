// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/full61/units_data.m";
g:=genus;
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);d:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xy]);if d lt Degree(F)then L:=sub<F|d>;else L:=F;end if;x:=L!xy[1];y:=L!xy[2];r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);EE:=EllipticCurve([1-c,-b,-b,L!0,L!0]);PP:=EE![0,0];assert N*PP eq EE!0 and PP ne EE!0 and TateNormalForm_xy(EE,PP)eq [x,y];return EE,PP;
end function;
function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;bb:=[1,0];
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/hecke_jets.m";
PF:=PolynomialRing(GF(2));closedkeys:=[];
for rr in SourceRecords do FF:=ext<GF(2)|PF!rr[1]>;uv:=[FF!PF!v:v in rr[5]];Append(~closedkeys,XYKey(uv[1],uv[2]));end for;assert #Seqset(closedkeys)eq 4;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/further_hecke_data.m";
MM:=ZeroMatrix(Integers(),4,4);
for i in[1..4]do for rr in SourceHeckeRecords[i]do r:=rr[4];FF:=ext<GF(2)|PF!r[1]>;uv:=[FF!PF!v:v in r[5]];j:=Index(closedkeys,XYKey(uv[1],uv[2]));assert j gt 0;MM[i,j]+:=rr[3];end for;end for;
u:=Vector(Integers(),[1,0,0,0]);v7:=Vector(Integers(),[0,0,0,0]);for r in FurtherHecke[1][2]do v7[r[1]]+:=r[2];end for;assert FurtherHecke[1][1]eq 7;
r3:=(u*MM-4*u)*(MM+2);r7:=(v7-8*u)*(MM+2);short:=r7-3*r3;print "S15_SS61_T3_MATRIX",MM;print "S15_SS61_R3",r3;print "S15_SS61_R7_MINUS3R3",short;assert short eq Vector(Integers(),[-4,3,-2,0]);
M0:=CuspidalSubspace(ModularSymbols(61,2,1));e0:=WindingElementProjection(M0);T20:=Transpose(DualHeckeOperator(M0,2));T30:=Transpose(DualHeckeOperator(M0,3));rs:=[];v:=e0;for k in[0..3]do Append(~rs,Eltseq(v));v:=v*T20;end for;WW:=Matrix(Rationals(),rs);assert Rank(WW)eq 3 and Rank(VerticalJoin(WW,T30+2))eq 3;
assert 2^6 mod 61 eq 3 and Min([k:k in[1..60]|3^k mod 61 in[1,60]])eq 5;assert Dimension(CuspidalSubspace(ModularSymbolsH(61,[3],2,1)))eq 26;
print "S15_SS61_RELATIONS_AND_RESTRICTIONS_VERIFIED";quit;
