// X_Delta(N) for N = 29, Delta = <-1,12> = {±1,±12}
// LMFDB label 29.210.8.b.2; index 210, genus 8, 14 cusps.
//
// Canonical model: 15 quadrics in P^7 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(29, [12]), minimize_strategy="LLL")
// sage-group: GammaH(29, [12])
// Coordinates x0, ..., x7 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(29, [12]): x0 vanishes to order 1 at infinity and x1, ..., x7 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 29;
Delta := [1, 12, 17, 28];
g := 8;
P<x0,x1,x2,x3,x4,x5,x6,x7> := ProjectiveSpace(Rationals(), 7);
X := Curve(P, [
  x3*x5 - x4*x5 - x3*x6 + x4*x6 + x5*x6 - x6^2 - x0*x7 + x1*x7 + x2*x7 - x4*x7,
  x3*x4 - x1*x5 - x3*x5 + 2*x5^2 - x3*x6 + x5*x6 + x1*x7 - x2*x7 - x3*x7 + x7^2,
  x2*x4 - x4^2 - x0*x5 - x2*x5 + x3*x5 + x4*x5 + x5^2 - x2*x6 + x4*x6 + 2*x5*x6 + x0*x7 - x2*x7 - x3*x7 - x6*x7 + x7^2,
  -x3*x4 + x1*x5 + x3*x5 - x4*x5 + x2*x6 - x5*x6 - x6^2 - x0*x7 + 2*x3*x7 + x4*x7 - 2*x5*x7 + x7^2,
  -x2*x3 + x1*x4 - x4^2 - x1*x5 + x2*x5 + x3*x5 - x1*x6 + 2*x3*x6 + x4*x6 - x5*x6 + x0*x7 - x1*x7 + x4*x7 - x5*x7 - 2*x6*x7,
  x3*x5 - x4*x5 + x5*x6 - x0*x7 + x2*x7 - x3*x7 + 2*x4*x7 - x6*x7 - 3*x7^2,
  x1*x2 - x0*x3 - x1*x3 + x3^2 + x0*x4 - x1*x4 - x2*x4 + 2*x3*x4 - x2*x5 + x4*x5 - x0*x6 + x5*x6 + x6^2 - x0*x7 + x5*x7 + 2*x6*x7 + x7^2,
  x2^2 - x1*x3 - 2*x2*x4 + x3*x4 + x4^2 + x0*x5 + x1*x5 - x2*x5 - x5^2 + x1*x6 - x2*x6 - x3*x6 - x4*x6 - x5*x6 + 2*x6^2 - x0*x7 - x1*x7 + x2*x7 + x3*x7 + x4*x7 - x5*x7 + x6*x7,
  x3^2 - x2*x4 - x3*x4 + x4^2 + x1*x5 + 2*x2*x5 - 2*x3*x5 - x4*x5 - 2*x5^2 - x1*x6 + x2*x6 + 2*x3*x6 - x5*x6 - x6^2 + x0*x7 - x2*x7 + x3*x7 - 2*x5*x7 + x7^2,
  x1*x2 - x0*x3 - x1*x4 + x3*x4 + x0*x5 - 3*x2*x5 + x4*x5 + 3*x5^2 + x3*x6 - x5*x6 - x1*x7 + x4*x7 - x5*x7 + x7^2,
  -x2*x6 + x3*x6 + x5*x6 + x6^2 + x0*x7 + 2*x2*x7 - 2*x3*x7 - x4*x7 - 3*x5*x7 - 2*x6*x7 - x7^2,
  -x3^2 + x0*x5 + x1*x5 + x3*x5 - 3*x4*x5 + x5^2 - x0*x6 + x2*x6 + x4*x6 - 2*x5*x6 + x1*x7 - x3*x7 - x4*x7 - x5*x7 + x7^2,
  -x2*x5 + x4*x5 + x1*x6 - x3*x6 - x4*x6 + x6^2 - 2*x1*x7 + 2*x2*x7 + 2*x3*x7 + x5*x7 - 3*x6*x7,
  x1^2 - x0*x2 + x2^2 - 2*x1*x3 + x3^2 + x0*x4 - x1*x4 - x2*x4 + x3*x4 - x1*x5 + 2*x3*x5 + x2*x6 - x6^2 + x0*x7 - x2*x7 - x3*x7 + x4*x7 - 2*x6*x7,
  -x3*x4 + x4^2 + x1*x5 - 2*x4*x5 - x1*x6 + 3*x3*x6 - 2*x4*x6 + 2*x5*x6 + x6^2 + x0*x7 - x2*x7 - x3*x7 - x4*x7 + x5*x7 + 3*x6*x7 - x7^2
]);
