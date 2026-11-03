// Certify smoothness at p=3 without the prohibitively expensive direct
// Jacobian-minor computation on 21 quadrics in P^8.
//
// For a geometrically integral projective curve over the perfect field
// F_3, p_a-p_g is the sum of the nonnegative delta invariants of its
// singular points.  Thus p_a=p_g proves that the curve is normal, hence
// smooth.
None := 0;
load "lmfdb_43.132.9.a.2.m";
XQ := Curve(ProjectiveSpace(Pol),model_0);
assert Degree(XQ) eq 16;
assert ArithmeticGenus(XQ) eq 9;
k := GF(3);
P8 := ProjectiveSpace(k,8);
S := CoordinateRing(P8);
X3 := Curve(P8,[Evaluate(q,[S.i:i in [1..9]]):q in model_0]);
assert IsAbsolutelyIrreducible(X3);
assert Degree(X3) eq 16;
pa := ArithmeticGenus(X3);
pg := GeometricGenus(X3);
assert pa eq 9;
assert pg eq 9;
assert pa eq pg;
printf "CHECK|ABSOLUTELY_IRREDUCIBLE_MOD_3=true\n";
printf "CHECK|GENERIC_HILBERT_POLYNOMIAL=16*n-8\n";
printf "CHECK|CANONICAL_DEGREE_MOD_3=16\n";
printf "CHECK|ARITHMETIC_GENUS=%o|GEOMETRIC_GENUS=%o\n",pa,pg;
printf "CHECK|CANONICAL_MODEL_SMOOTH_MOD_3_BY_DELTA_INVARIANTS=true\n";
exit;
