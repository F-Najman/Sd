// Mandatory companion: exact relations and complete canonical-basis rank
// from canonical_relations.py/export_canonical.py. See MODEL_IDENTIFICATION.md.
load "canonical_input.m";
S := Scheme(ProjectiveSpace(Rationals(),expected_genus-1),equations);
assert Dimension(S) eq 1;
assert Degree(S) eq 2*expected_genus-2;
assert ArithmeticGenus(S) eq expected_genus;
P := S!cusp_coordinates;
// Containment of the known canonical image plus equal Hilbert polynomials
// proves equality as schemes, hence smoothness and geometric integrality.
print "SUCCESS: canonical model identified by Hilbert polynomial", expected_genus;
print "Rational q-expansion cusp:", P;
quit;
