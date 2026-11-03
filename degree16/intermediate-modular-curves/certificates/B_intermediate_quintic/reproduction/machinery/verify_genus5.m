// Independent geometric verification of a genus-five intersection of quadrics.
// Input is exported by export_genus5.py; do not accept arbitrary equations as
// a modular model unless their q-expansion relation certificate is also present.
load "genus5_input.m";
assert #equations eq 3;
C := Scheme(ProjectiveSpace(Rationals(),4),equations);
assert Dimension(C) eq 1 and Degree(C) eq 8;
assert IsNonsingular(C);
assert ArithmeticGenus(C) eq 5;
// A smooth positive-dimensional projective complete intersection is
// geometrically connected, hence geometrically integral. Its degree eight
// matches the nonhyperelliptic canonical image certified by product rank 12.
print "SUCCESS: smooth genus-five complete intersection of degree eight.";
print "Rational modular interpretation is proved in RATIONAL_MODELS.md.";
quit;
