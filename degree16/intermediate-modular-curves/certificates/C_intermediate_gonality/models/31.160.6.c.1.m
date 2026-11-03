// X_Delta(N) for N = 31, Delta = <-1,5> = {±1,±5,±6}
// LMFDB label 31.160.6.c.1; index 160, genus 6, 10 cusps.
//
// Canonical model: 6 quadrics in P^5 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(31, [6]), minimize_strategy="LLL")
// sage-group: GammaH(31, [6])
// Coordinates x0, ..., x5 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(31, [6]): x0 vanishes to order 1 at infinity and x1, ..., x5 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 31;
Delta := [1, 5, 6, 25, 26, 30];
g := 6;
P<x0,x1,x2,x3,x4,x5> := ProjectiveSpace(Rationals(), 5);
X := Curve(P, [
  -x2^2 + x2*x3 + x0*x4 - x4^2 - x0*x5 - x2*x5 + x4*x5,
  -x1^2 + x0*x2 + x1*x2 - x0*x3 - x2*x4 + x4^2 + x1*x5 - x2*x5 + x3*x5 - x4*x5,
  x1*x4 - x2*x4 + x3*x4 - x4^2 - x0*x5 - x1*x5 + x2*x5 - x3*x5 + 2*x4*x5 + x5^2,
  x1^2 - x0*x2 - x1*x2 + x0*x3 - x1*x3 + x2*x3 + x0*x4 + x2*x4 - x3*x4 - x4^2 - x0*x5 - x1*x5 + x3*x5 - x4*x5 + x5^2,
  x1^2 - x0*x2 + x2^2 - x1*x3 - x3^2 + 2*x3*x4 - x4^2 + 2*x2*x5 - x4*x5 + x5^2,
  -x1*x2 - x2^2 + x0*x3 + x1*x3 + x2*x3 - x1*x4 - x3*x4 + x4^2 + x1*x5 - 2*x3*x5
]);
