// X_Delta(N) for N = 35, Delta = <-1,8> = {±1,±6,±8,±13}
// LMFDB label 35.144.7.a.2; index 144, genus 7, 12 cusps.
//
// Canonical model: 10 quadrics in P^6 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(35, [8, 34]), minimize_strategy="LLL")
// sage-group: GammaH(35, [8, 34])
// Coordinates x0, ..., x6 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(35, [8, 34]): x0 vanishes to order 1 at infinity and x1, ..., x6 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 35;
Delta := [1, 6, 8, 13, 22, 27, 29, 34];
g := 7;
P<x0,x1,x2,x3,x4,x5,x6> := ProjectiveSpace(Rationals(), 6);
X := Curve(P, [
  -x3*x4 + x2*x5 - x3*x6 + x4*x6 - x5*x6 + x6^2,
  -x2*x4 + x3*x4 + x1*x5 - x2*x5 + x4*x5 - x5^2 - x2*x6 + x3*x6,
  -x2*x4 + x3*x4 + x2*x5 - x3*x5 + x0*x6 - x3*x6 - x4*x6,
  x3^2 - x1*x5 + x3*x5 - 2*x3*x6 + x5*x6 + x6^2,
  -x2*x3 + x1*x4 - x3*x4 + x1*x6 + x2*x6 - x4*x6 - 2*x6^2,
  -x1*x4 + x2*x4 + x0*x5 - x1*x5 + x3*x5 - x4*x5 - x5^2 - x1*x6 + x2*x6 + x4*x6 - x5*x6 + x6^2,
  -x2^2 + x1*x3 + x2*x4 - x2*x5 - x0*x6 - x1*x6 + 2*x2*x6 + x5*x6,
  x2^2 - x2*x3 - x3^2 - x0*x4 + x2*x4 - x3*x4 + x0*x5 + x2*x5 - x3*x5 + x4*x5 - x5^2 + x2*x6,
  x1*x2 - x2^2 - x0*x3 + x1*x3 + x1*x4 - x3*x4 - x0*x5 + 2*x3*x5 + x4*x5 + x5^2 - x1*x6 - x2*x6 + x6^2,
  -x1^2 + x0*x2 + x1*x2 - x0*x3 + x1*x3 - x3^2 - x0*x4 - x1*x4 + x2*x4 + x0*x5 - x2*x5 + x3*x5 + x4*x5 - x5^2 + x1*x6 - x2*x6 - x3*x6 + x4*x6 + x6^2
]);
