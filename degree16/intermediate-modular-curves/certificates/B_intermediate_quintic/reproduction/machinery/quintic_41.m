// Exact degree-five function from K-3P on the newly verified model.
load "model_41.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and Degree(C) eq 8 and ArithmeticGenus(C) eq 5;
P := C![0,1,0,0,1];
D := CanonicalDivisor(C)-3*Divisor(Place(P));
assert Degree(D) eq 5;
V,mp := RiemannRochSpace(D);
assert Dimension(V) eq 2;
f := mp(Basis(V)[2])/mp(Basis(V)[1]);
assert Degree(Denominator(Divisor(f))) eq 5;
print "SUCCESS quintic_41: exact degree-five function from K-3P.";
quit;
