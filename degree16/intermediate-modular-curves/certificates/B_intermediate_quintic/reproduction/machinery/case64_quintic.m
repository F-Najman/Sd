// A short positive certificate; no j-map, cusp classification, or torsion
// assumption is needed once this explicit quadratic point is given.
load "canonical_input.m";
assert expected_genus eq 5;
C := Curve(ProjectiveSpace(Rationals(),4),equations);
RC := CoordinateRing(Ambient(C));
P := C![3,0,0,1,1];
Qscheme := Scheme(C,[RC.1-2*RC.4-3*RC.5,RC.2-2*RC.4,
                      RC.3-RC.4-RC.5,RC.4^2-2*RC.4*RC.5-RC.5^2]);
assert Dimension(Qscheme) eq 0 and Degree(Qscheme) eq 2;
assert IsReduced(Qscheme) and IsIrreducible(Qscheme);
Q := Divisor(C,Qscheme);
assert Degree(Q) eq 2;
E := Divisor(Place(P))+Q;
D := CanonicalDivisor(C)-E;
assert Degree(D) eq 5;
V,to_function := RiemannRochSpace(D);
assert Dimension(V) eq 2;
basis := Basis(V);
f := to_function(basis[2])/to_function(basis[1]);
assert Degree(Denominator(Divisor(f))) eq 5;
print "rational point",P;
print "quadratic point (2a+3:2a:a+1:a:1), a^2-2a-1=0";
print "function",f;
print "SUCCESS exact degree five at level 64";
quit;
