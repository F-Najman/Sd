// X_Delta(N) for N = 34, Delta = <-1,13> = {±1,±13}
// LMFDB label 34.216.9.a.1; index 216, genus 9, 16 cusps.
//
// Canonical model: 21 quadrics in P^8 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(34, [13]), minimize_strategy="LLL")
// sage-group: GammaH(34, [13])
// Coordinates x0, ..., x8 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(34, [13]): x0 vanishes to order 1 at infinity and x1, ..., x8 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 34;
Delta := [1, 13, 21, 33];
g := 9;
P<x0,x1,x2,x3,x4,x5,x6,x7,x8> := ProjectiveSpace(Rationals(), 8);
X := Curve(P, [
  -x2*x3 + x3*x4 + x0*x5 - x4*x5 - x5^2 + x2*x6 - x4*x6 - x5*x6 - x0*x7 + x2*x7 + x3*x7 + x3*x8 - x5*x8 - x6*x8,
  -x2*x4 + x4^2 + x4*x5 + x0*x6 - x4*x6 - x5*x6 - x6^2 - x0*x7 + x2*x7 + x7^2 + x2*x8 - x5*x8 - x6*x8 - x8^2,
  -x4*x6 + x5*x6 + x6^2 + x2*x7 - 2*x5*x7 - x6*x7 - x2*x8 + x4*x8 + x5*x8 - 2*x6*x8 + x7*x8 + x8^2,
  -x2*x4 + x4^2 + x1*x5 - x3*x5 + x2*x6 - x4*x6 - x5*x6 - x1*x7 + x3*x7 + x4*x7 + 2*x5*x7 - 2*x7^2 + x2*x8 - 2*x5*x8 - x6*x8 + x7*x8 - x8^2,
  -x2*x4 + x3*x4 + x1*x5 - x2*x5 + x5^2 + x2*x6 - x3*x6 - x4*x6 - x5*x6 + x6^2 - x1*x7 + x2*x7 + x4*x7 - x7^2 + x2*x8 - x3*x8 + 2*x4*x8 - x6*x8 - x7*x8 - 2*x8^2,
  -x2*x5 + x4*x5 + x5^2 + x1*x6 - x3*x6 - x1*x7 + x2*x7 + x3*x7 - x4*x7 - x5*x7 - x6*x7 + x7^2 + x5*x8 + 2*x6*x8 - 3*x7*x8,
  x2*x3 - x1*x4 - x2*x4 - x3*x4 + 2*x4^2 + x1*x5 - 2*x3*x5 + x4*x5 + x1*x6 - x6^2 - x1*x7 + x3*x7 - x0*x8 + x5*x8 + x6*x8 + 2*x7*x8,
  x3*x4 - x4^2 - x1*x6 + x2*x6 - x5*x6 - 2*x2*x7 + x4*x7 + 2*x5*x7 + x6*x7 + x7^2 + x1*x8 + x2*x8 - 2*x3*x8 + x4*x8 - x5*x8 - x6*x8 - x7*x8,
  x3*x4 - x3*x5 + x5^2 - x1*x6 + x2*x6 - 2*x4*x6 + x5*x6 - x2*x7 + x3*x7 - x5*x7 + 2*x6*x7 - x0*x8 - x3*x8 + 2*x4*x8 + 2*x7*x8,
  x1*x2 - x0*x3 + x2*x3 - x1*x4 - x3*x4 + x4^2 - x1*x5 - x2*x5 + x3*x5 + x5^2 + x0*x6 + x1*x6 - 2*x2*x6 + x3*x6 + x5*x6 - x6^2 - x1*x7 + x3*x7 + x4*x7 - x6*x7 - x6*x8 + x7*x8 + x8^2,
  -x1*x3 + x3^2 + x0*x4 - x2*x4 - x4^2 + x1*x5 + x2*x5 - x3*x5 - 2*x5^2 - x0*x6 + x2*x6 + x3*x6 - x4*x6 + x6^2 + x0*x7 - x2*x7 - x3*x7 + x4*x7 - x6*x7 - x0*x8 + x2*x8 - x3*x8 + x5*x8 - x6*x8 + x8^2,
  x2*x5 - 2*x5^2 - x1*x6 - x2*x6 + x3*x6 + x4*x6 + x6^2 + x0*x7 + x1*x7 - x3*x7 - 2*x4*x7 - 2*x6*x7 - x0*x8 + x4*x8 + 2*x5*x8 + x6*x8 - x7*x8 + x8^2,
  x1*x4 - x3*x4 - x0*x5 + x2*x5 - x1*x6 + x3*x6 + x5*x6 + x0*x7 - x2*x7 - x4*x7 + x5*x7 - x7^2 - x1*x8 + x3*x8 + 2*x4*x8 - 2*x6*x8 + x7*x8 - 2*x8^2,
  -x1*x3 + x3^2 + x0*x4 + x1*x4 - x3*x4 - 2*x4^2 - x0*x5 + x3*x5 + x4*x5 - x0*x6 + x1*x6 - x3*x6 + x5*x6 + 2*x6^2 + x0*x7 - x4*x7 - x5*x7 - x6*x7 - x7^2 + x0*x8 - x1*x8 - x3*x8 - x4*x8 + 2*x5*x8 - x6*x8 - x8^2,
  -x4^2 + x4*x5 + 2*x4*x6 - x5*x6 - x6^2 + x0*x7 - x2*x7 - x6*x7 - x7^2 - x0*x8 + x2*x8 - x4*x8 - x5*x8 + 2*x6*x8 + x7*x8 + 2*x8^2,
  -x3*x4 + x4^2 + x2*x5 - 2*x5^2 - x2*x6 + x3*x6 + x2*x7 - x4*x7 + x6*x7 - x7^2 - x2*x8 + x3*x8 - x4*x8 + 2*x5*x8 - x6*x8 - x7*x8 + 2*x8^2,
  x1*x3 - x3^2 - x0*x4 + x2*x4 - x1*x5 + x3*x5 + x4*x5 + x0*x6 - x1*x6 - x2*x6 + x4*x6 + 2*x3*x7 - 2*x5*x7 - 2*x6*x7 + x0*x8 - x2*x8 - 2*x3*x8 + x5*x8 + x6*x8,
  x2^2 - x0*x4 - x1*x4 + x3*x4 + x4^2 + x0*x5 - 3*x2*x5 - x3*x5 + x4*x5 + x5^2 + 2*x1*x6 - x2*x6 - x3*x6 + x5*x6 - x1*x7 + x4*x7 + x5*x7 - x7^2 + x0*x8 + x1*x8 - 2*x2*x8 - x4*x8 + x6*x8 - x8^2,
  -x1^2 + x0*x2 + x1*x3 - x2*x3 - x0*x4 + 2*x3*x4 + x0*x5 - x2*x5 - 2*x5^2 + x1*x6 - 2*x2*x6 - x3*x6 - x4*x6 + x5*x6 + 2*x6^2 - x0*x7 + x1*x7 + x2*x7 - x3*x7 - x5*x7 + x6*x7 - x0*x8 - x1*x8 + x4*x8 + 2*x5*x8 + x6*x8,
  -x1*x3 - x2*x3 + x0*x4 + x1*x4 + x3*x4 - 2*x4^2 - x2*x5 + 2*x3*x5 - x4*x5 + x5^2 + x1*x6 + x2*x6 + x3*x6 - 2*x4*x6 - 2*x5*x6 - x6^2 - x0*x7 + x2*x7 + x5*x7 - x6*x7 + x7^2 + x2*x8 - x3*x8 - x5*x8 + 2*x6*x8 - x7*x8,
  -x1*x4 + x2*x4 + x3*x4 - x4^2 + x0*x5 - x2*x5 - x3*x5 - x5^2 - x0*x6 + x1*x6 + x4*x6 + x5*x6 + x6^2 + x0*x7 - x1*x7 - 3*x4*x7 - x6*x7 + x7^2 - x0*x8 + 2*x1*x8 + x2*x8 - x3*x8 + x4*x8 + x5*x8 - x6*x8 - 2*x7*x8 - x8^2
]);
