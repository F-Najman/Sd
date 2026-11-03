SetQuitOnError(true);SetColumns(0);tt:=Cputime();
X:=SmallModularCurve(61);P:=ProjectiveSpace(GF(2),3);R:=CoordinateRing(P);Y:=Curve(P,[R!f:f in DefiningEquations(X)]);assert IsNonsingular(Y);print "X0_F2",Genus(Y),#Points(Y);
function RedCusp(d)
 a:=Eltseq(Cusp(X,61,d));v:=Min([Valuation(t,2):t in a|t ne 0]);return Y![GF(2)!(t/2^v):t in a];end function;
print "CUSPS",RedCusp(1),RedCusp(61);
for Q in Points(Y) do print "POINT",Eltseq(Q);end for;
G,toD,toG:=ClassGroup(Y);print "CLASSGROUP",Invariants(G);
c:=Place(RedCusp(61));c0:=Place(RedCusp(1));gc:=toG(c0-c);print "CUSP_CLASS",Eltseq(gc),Order(gc);
Spts:=[Q:Q in Points(Y)|Q ne RedCusp(1) and Q ne RedCusp(61)];assert #Spts eq 1;ds:=15*(Place(Spts[1])-c);gs:=toG(ds);print "TARGET_CLASS",Eltseq(gs),Order(gs);
S:=CuspidalSubspace(ModularSymbols(61,2,1));assert Dimension(S) eq 4;
EE:=EllipticCurve([Rationals()|1,0,0,-2,1]);assert Conductor(EE) eq 61;
for q in [2,3,5,7,11,13,17,19,23,29,31] do
 n:=Integers()!Determinant((q+1)*IdentityMatrix(Rationals(),4)-HeckeOperator(S,q));e:=#BaseChange(EE,GF(q));print "RED_ORDERS",q,n,e,n div e;end for;
print "X0_FINITE_COMPLETE",Cputime(tt);quit;
