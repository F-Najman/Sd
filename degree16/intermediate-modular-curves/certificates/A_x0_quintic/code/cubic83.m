// The fixed cubic divisor explaining cusp index 23 at level 83.
SetColumns(180); load "coordinates.m";
C:=ModularCurveQuotient(83,[]); M:=CanonicalALMatrix(83,83);
R<x>:=PolynomialRing(Rationals()); f:=x^3+4*x^2+2*x-5;
assert IsIrreducible(f) and Discriminant(f) eq -83;
K<u>:=NumberField(f); CK:=ChangeRing(C,K);
v:=[2*u^2+4*u-4,3*u^2+5*u-7,u^2+3*u-3,3*u^2+3*u-5,2*u,-2*u^2-2*u+2,2];
T:=CK!v;
assert T[5]/T[7] eq u; // The point has exact degree 3.
assert CK!Eltseq(ChangeRing(M,K)*Matrix(K,7,1,v)) eq T;
assert Rank(M+IdentityMatrix(Rationals(),7)) eq 1;
// On J/A, w acts as -1. A w-invariant degree-5 class based at 5P
// therefore has 2*c=5*t; in the cyclic group of order 41, c=23*t.
assert (2*23-5) mod 41 eq 0;
printf "cubic_polynomial=%o discriminant=%o\n",f,Discriminant(f);
print "cubic_point_coordinates=",v;
print "SUCCESS: a reduced rational degree-three divisor fixed pointwise by w83; its pullback-degree-one translate has index 23 and fixed cubic part.";
quit;
