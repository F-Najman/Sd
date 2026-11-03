// Alternative exact verifier: use only certified quadratic relations.
// Success is sufficient regardless of Petri's theorem; failure is inconclusive.
load "canonical_input.m";
quadrics := [f:f in equations|TotalDegree(f) eq 2];
S := Scheme(ProjectiveSpace(Rationals(),expected_genus-1),quadrics);
assert Dimension(S) eq 1;
print "dimension verified";
assert Degree(S) eq 2*expected_genus-2;
assert ArithmeticGenus(S) eq expected_genus;
print "degree and genus verified";
assert IsNonsingular(S);
print "smoothness verified";
assert IsIrreducible(S);
P := S!cusp_coordinates;
// Smooth + Q-irreducible + Q-point implies geometric integrality.
// The certified nonhyperelliptic canonical image is contained in S, hence
// equals S. Full explanation is in verify_canonical.m.
print "SUCCESS: geometrically integral canonical model", expected_genus;
print "Rational q-expansion cusp:", P;
quit;
