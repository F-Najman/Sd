SetQuitOnError(true);SetColumns(0);tt:=Cputime();
N:=61;assert Order(GF(N)!2)eq 60;
assert Min([k:k in[1..60]|3^k mod N in[1,60]])eq 5;
assert Min([k:k in[1..60]|4^k mod N in[1,60]])eq 15;
assert 2^6 mod 61 eq 3;
SY:=CuspidalSubspace(ModularSymbolsH(61,[3],2,1));SZ:=CuspidalSubspace(ModularSymbolsH(61,[4],2,1));S0:=CuspidalSubspace(ModularSymbols(61,2,1));
assert Dimension(SY)eq 26 and Dimension(SZ)eq 8 and Dimension(S0)eq 4;
print "S15_QUOTIENT61_GENERA",Dimension(SY),Dimension(SZ),Dimension(S0);
assert (2*Dimension(SZ)-2)-2*(2*Dimension(S0)-2)eq 2;
X:=SmallModularCurve(61);assert Genus(X)eq 4 and IsNonsingular(X)and Dimension(Ambient(X))eq 3;
fs:=DefiningEquations(X);assert Sort([TotalDegree(f):f in fs])eq [2,3];Q:=[f:f in fs|TotalDegree(f)eq 2][1];R:=Parent(Q);A:=Matrix(Rationals(),4,4,[i eq j select MonomialCoefficient(Q,R.i^2)else MonomialCoefficient(Q,R.i*R.j)/2:i,j in[1..4]]);
assert Rank(A)eq 4 and Determinant(A)eq -1/4;assert not IsSquare(Determinant(A));
print "S15_XZERO61_CANONICAL_QUADRIC",Q,"determinant",Determinant(A);
// All coefficients are exact. Adjunction for this smooth (2,3) intersection
// identifies O(1) with the canonical sheaf; the nonsquare discriminant
// means neither geometric trigonal ruling is defined over Q.
// The double cover Z -> X0 has exactly two fixed geometric points.
PrintFile("work/degree15/quotient61/curve_data.m",Sprintf("GenusY:=26;GenusZ:=8;GenusX0:=4;QuadricMatrix:=Matrix(Rationals(),4,4,%o);Equations:=%o;",Eltseq(A),fs):Overwrite:=true);
print "S15_SMALL_QUOTIENT61_CHECKS_COMPLETE",Cputime(tt);quit;
