// X_Delta(N) for N = 44, Delta = <-1,5> = {±1,±5,±7,±9,±19}
// LMFDB label 44.144.8.c.4; index 144, genus 8, 10 cusps.
//
// Canonical model: 15 quadrics in P^7 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(44, [35]), minimize_strategy="LLL")
// sage-group: GammaH(44, [35])
// Coordinates x0, ..., x7 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(44, [35]): x0 vanishes to order 1 at infinity and x1, ..., x7 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 44;
Delta := [1, 5, 7, 9, 19, 25, 35, 37, 39, 43];
g := 8;
P<x0,x1,x2,x3,x4,x5,x6,x7> := ProjectiveSpace(Rationals(), 7);
X := Curve(P, [
  -x3*x6 + x4*x6 + x6^2 + x2*x7 - x4*x7 - x6*x7,
  x1*x6 - x5*x6 - x6^2 - x0*x7 - x1*x7 + x3*x7 + x4*x7 + x5*x7 + x7^2,
  -x1*x2 + x0*x3 + x2*x5 - x0*x6 + x1*x6 - x6^2 - x0*x7 + x1*x7 - x5*x7 + x7^2,
  -x1*x2 + x0*x3 + x1*x3 - x3^2 - x0*x4 + x4^2 + x2*x5 - x3*x5 - x0*x6 + x2*x6 + x4*x6 + x2*x7 - x3*x7,
  x2*x3 - x3^2 - x0*x5 + x3*x5 + x4*x5 - x1*x6 - x2*x6 + x3*x6 + x5*x6 + x6^2 + x3*x7 - x4*x7,
  -x1*x4 + x0*x5 + x1*x5 - x3*x5 - x5^2 + x1*x6 + x2*x6 - x3*x6 - x5*x6 - x1*x7 - x5*x7 + 2*x6*x7,
  -x2*x3 + x3^2 + x1*x4 - x1*x5 - x4*x5 + x5^2 + x2*x6 - x3*x6 + 2*x5*x6 - 2*x6^2,
  x1*x3 - x3^2 - x0*x4 + x4^2 + x3*x5 - 2*x1*x6 + x2*x6 + x4*x6 + x2*x7 - 2*x5*x7 + x6*x7,
  -x2*x4 + 2*x3*x4 + x1*x5 - x2*x5 + x4*x5 - x1*x6 + x5*x6 - x6^2 - x0*x7 + x2*x7 + x3*x7 - x4*x7 - x5*x7 + x7^2,
  2*x3*x4 - 2*x0*x6 - x4*x6 + 2*x6^2 + x3*x7 - x4*x7 + x5*x7,
  -x1*x4 + x3*x4 + x0*x5 + x1*x5 - x2*x5 + x2*x6 - x3*x6 - x4*x6 - x5*x6 + x6^2 - x0*x7 - x2*x7 + 2*x3*x7 + x4*x7 - x5*x7 - x6*x7 + x7^2,
  -x2^2 + x1*x3 + x2*x3 - x3^2 - x1*x4 + x3*x4 + x1*x5 - x2*x5 + x4*x5 + x5^2 - x1*x6 + x2*x6 + x4*x6 - 2*x5*x6 - x6^2,
  -x3*x4 + x4^2 + x2*x5 - x4*x5 + 2*x5^2 - x1*x6 + x3*x6 - x5*x6 + x0*x7 + x1*x7 - 2*x2*x7 + x3*x7 - x5*x7 - x6*x7 - x7^2,
  -x3^2 + x2*x4 - x3*x4 + x2*x5 - x4*x5 - x5^2 + x1*x6 + x2*x6 + x3*x6 - x4*x6 - x6^2 + x0*x7 - x4*x7 - x6*x7 - x7^2,
  -x1^2 + x0*x2 + x1*x3 - x3^2 - x0*x4 - x1*x4 + x3*x4 + x0*x5 + x1*x5 - x2*x5 - x3*x5 - 2*x5^2 - 2*x0*x6 + x1*x6 + x3*x6 + x4*x6 + 2*x5*x6 + x6^2 + x1*x7 - x2*x7 + x4*x7 - x5*x7
]);
