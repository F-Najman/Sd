// gon_Q(43.308.15.b.1) <= 9: a base-point-free pencil of degree 9 on the MD Sage canonical model.
// D = 3*C3 + C4 + P5 with C3, C4 rational points (cusps) and P5 a closed point of degree 5 (points.m).
// See README.md for the argument. Run from this folder:  magma -b certificate.m
SetQuitOnError(true); SetColumns(0);
t0 := Realtime();

// ---- The model: a smooth canonical curve of genus 15 ----
load "../../../models/43.308.15.b.1.m";        // X in P^14 (78 quadrics), g = 15
eqs := DefiningEquations(X);
assert g eq 15 and Dimension(X) eq 1 and Degree(X) eq 2*g - 2;
assert IsIrreducible(X) and IsReduced(X);
h := HilbertPolynomial(Ideal(X)); assert h eq (2*g - 2)*Parent(h).1 + 1 - g;
// Its reduction mod 2 is integral of geometric genus 15 with a nonsingular F_2-point, so the model has good
// reduction at 2 (Adzaga et al., Lemma 2.3); in particular X is smooth of genus 15 over Q.
X2 := Curve(Reduction(X, 2));
assert IsIrreducible(X2) and IsReduced(X2) and Genus(X2) eq g;
assert IsNonsingular(X2, X2 ! ([GF(2) | 1] cat [GF(2) | 0 : i in [2..g]]));
print "MODEL: smooth canonical curve of genus 15";

// ---- The points ----
load "points.m";                                // K<a>, P5coeffs, P5coords, C3Jets, C4
JacobianRank := func< pt | Rank(Matrix([[Evaluate(Derivative(f, j), pt) : j in [1..g]] : f in eqs])) >;
// P5: on the curve and nonsingular; K has prime degree 5 and the coordinates are not all rational,
// so P5 is a closed point of degree 5.
assert Degree(K) eq 5 and P5coords[1] eq 1;
assert &and[Evaluate(f, P5coords) eq 0 : f in eqs] and JacobianRank(P5coords) eq g - 2;
assert Rank(Matrix(Rationals(), P5coeffs)) eq 5;
// C3, C4: distinct rational points, nonsingular.
C3 := C3Jets[1];
assert &and[Evaluate(f, C3) eq 0 and Evaluate(f, C4) eq 0 : f in eqs];
assert JacobianRank(C3) eq g - 2 and JacobianRank(C4) eq g - 2;
assert Rank(Matrix(Rationals(), [C3, C4])) eq 2;
// The jet at C3: the curve equations vanish to order 3 on C3 + C3Jets[2]*t + C3Jets[3]*t^2, and the tangent
// vector C3Jets[2] is nonzero, so t is a local parameter at C3 (up to order 3).
R<t> := PowerSeriesRing(Rationals(), 3);
arc := [&+[R | C3Jets[n + 1][j]*t^n : n in [0..2]] + O(t^3) : j in [1..g]];
assert &and[Valuation(Evaluate(f, arc)) ge 3 : f in eqs];
assert Rank(Matrix(Rationals(), C3Jets[1..2])) eq 2;
i0 := [j : j in [1..g] | C3[j] ne 0][1];
assert C3Jets[1][i0] eq 1 and C3Jets[2][i0] eq 0 and C3Jets[3][i0] eq 0;   // x_{i0} = 1 along the jet
print "POINTS: P5 of degree 5, C3 and C4 rational, all nonsingular";

// ---- h^0(D) = 2 ----
// A canonical section is a linear form in x_0, ..., x_14. Vanishing to order 3 at C3 is vanishing of the
// coefficients of t^0, t^1, t^2 along the jet (x_{i0} = 1 trivializes the canonical bundle there);
// vanishing at C4 is one condition; vanishing at P5 is one condition over K, i.e. five over Q.
rows := C3Jets cat [C4] cat [[P5coeffs[j][n] : j in [1..g]] : n in [1..5]];
r := Rank(Matrix(Rationals(), rows));
assert #rows eq 9 and r eq 8;
h0KD := g - r;                     // = 7
h0D := 9 + 1 - g + h0KD;           // Riemann-Roch
assert h0D eq 2;
printf "H0: rank of the 9 conditions = %o, h0(K-D) = %o, h0(D) = %o\n", r, h0KD, h0D;

// ---- No base points ----
// Removing one copy of C3, or C4, or the whole orbit P5 (a rational base locus containing one conjugate
// contains all five) leaves h0 = 1, i.e. the conditions keep rank 8 resp. drop to rank 4 for 3*C3 + C4.
assert Rank(Matrix(Rationals(), rows[1..2] cat rows[4..9])) eq 8;   // 2*C3 + C4 + P5
assert Rank(Matrix(Rationals(), rows[1..3] cat rows[5..9])) eq 8;   // 3*C3 + P5
assert Rank(Matrix(Rationals(), rows[1..4])) eq 4;                  // 3*C3 + C4
print "BASE POINTS: none";
printf "Q_GONALITY_UPPER_BOUND=9 VERIFIED=true  (%.1os)\n", Realtime(t0);
quit;
