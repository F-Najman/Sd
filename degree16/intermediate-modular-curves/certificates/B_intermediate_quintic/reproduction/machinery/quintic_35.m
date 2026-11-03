// Exact degree-five function from K-P-2Q on the newly verified model.
load "model_35.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and Degree(C) eq 8 and ArithmeticGenus(C) eq 5;
P := C![0,1,1,0,0];
Q := C![0,0,1,-1,1];
D := CanonicalDivisor(C)-Divisor(Place(P))-2*Divisor(Place(Q));
assert Degree(D) eq 5;
V,mp := RiemannRochSpace(D);
assert Dimension(V) eq 2;
f := mp(Basis(V)[2])/mp(Basis(V)[1]);
assert Degree(Denominator(Divisor(f))) eq 5;
print "SUCCESS quintic_35: exact degree-five function from K-P-2Q.";
quit;
