// Run in a directory containing canonical_input.m from export_canonical.py.
// Exact modular relations and rational descent are separate required inputs.
load "canonical_input.m";
S := Scheme(ProjectiveSpace(Rationals(),expected_genus-1),equations);
assert Dimension(S) eq 1;
assert IsNonsingular(S);
assert IsIrreducible(S);
assert Degree(S) eq 2*expected_genus-2;
assert ArithmeticGenus(S) eq expected_genus;
P := S!cusp_coordinates;
// A smooth irreducible Q-curve with a Q-point is geometrically integral:
// geometric components are disjoint and Galois acts transitively on them;
// the rational point forces one component to be Galois invariant.
// The independently certified nonhyperelliptic canonical image lies in S.
// Both are integral curves, so they coincide. The degree and genus checks
// are redundant safeguards against an erroneous input or convention.
print "SUCCESS: geometrically integral canonical model", expected_genus;
print "Rational q-expansion cusp:", P;
quit;
