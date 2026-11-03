// X_Delta(N) for N = 39, Delta = <-1,5> = {±1,±5,±8,±14}
// LMFDB label 39.168.9.a.1; index 168, genus 9, 12 cusps.
//
// Canonical model: 21 quadrics in P^8 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(39, [14, 31]), minimize_strategy="LLL")
// sage-group: GammaH(39, [14, 31])
// Coordinates x0, ..., x8 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(39, [14, 31]): x0 vanishes to order 1 at infinity and x1, ..., x8 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 39;
Delta := [1, 5, 8, 14, 25, 31, 34, 38];
g := 9;
P<x0,x1,x2,x3,x4,x5,x6,x7,x8> := ProjectiveSpace(Rationals(), 8);
X := Curve(P, [
  -x7^2 + x6*x8 + x7*x8,
  -x5*x7 + x6*x7 + x4*x8,
  x4*x7 - x5*x7 - x3*x8 + x7*x8,
  -x5*x6 + x6^2 + x4*x7 - x4*x8,
  -x4*x6 + x5*x6 + x3*x7 - x3*x8 - x6*x8,
  -x4^2 + x3*x5 + x4*x5 - x3*x6 - x4*x8,
  x1*x6 - x3*x6 - x4*x6 + x5*x6 - x0*x7 + x5*x7 + x7^2,
  -x3*x5 + x1*x6 - x0*x7 + x4*x7 + x0*x8 + x3*x8 - x7*x8,
  x4^2 - x4*x5 - x1*x7 + x7^2 + x1*x8 - x3*x8 + x6*x8,
  x1*x7 - x2*x7 - x6*x7 + x7^2 - x0*x8 + x4*x8 + x6*x8 + x7*x8,
  x3*x4 - x3*x5 - x1*x6 + x3*x6 + x6*x7 - x7^2 + x0*x8 - x4*x8,
  x3^2 - x3*x5 - x0*x6 + x5*x6 + x6^2 + x1*x7 - x2*x7 + x5*x7,
  -x1*x3 + x0*x4 - x4*x5 + x1*x6 - x5*x6 - x0*x7 + x2*x7,
  -x2*x6 + x3*x6 - x6^2 + x1*x7 - x2*x7 + x3*x7 + x6*x7,
  x3*x5 - x4*x5 - x3*x6 + x6^2 + x4*x7 + x5*x7 - x0*x8 + x1*x8 - x3*x8 - x7*x8,
  x2*x4 - x1*x5 - x3*x5 + x3*x6 + x4*x6 - x4*x7 + x0*x8 - x3*x8 - x6*x8,
  -x1*x4 + x0*x5 + x1*x5 + x3*x5 - x4*x5 - x0*x6 - x3*x6 + x6^2 + x3*x7 - x0*x8 - x4*x8,
  -x2*x3 + x3^2 + x1*x4 - x1*x5 - x3*x5 + x4*x6 - x5*x6 + x1*x7 + x3*x7 - x7^2 + x4*x8,
  -x4*x5 + x5^2 + x4*x6 - x5*x6 + x1*x8 - x2*x8 + x3*x8 + x4*x8 - x5*x8 - x6*x8,
  -x1^2 + x0*x2 + x1*x2 - x0*x3 + x3^2 - x2*x4 + x3*x5 + x6^2 - x1*x7 - x2*x7,
  x1^2 - x0*x2 - x1*x3 + x0*x4 + x2*x4 - x4^2 - x1*x5 - x4*x5 + x2*x6 + x5*x6 - x3*x7 + x4*x7 + x7^2 + x4*x8 + x5*x8
]);
