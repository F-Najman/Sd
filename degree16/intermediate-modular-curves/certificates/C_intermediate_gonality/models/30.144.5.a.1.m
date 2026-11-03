// X_Delta(N) for N = 30, Delta = <-1,11> = {±1,±11}
// LMFDB label 30.144.5.a.1; index 144, genus 5, 16 cusps.
//
// Canonical model: 3 quadrics in P^4 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(30, [11, 19]), minimize_strategy="LLL")
// sage-group: GammaH(30, [11, 19])
// Coordinates x0, ..., x4 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(30, [11, 19]): x0 vanishes to order 1 at infinity and x1, ..., x4 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 30;
Delta := [1, 11, 19, 29];
g := 5;
P<x0,x1,x2,x3,x4> := ProjectiveSpace(Rationals(), 4);
X := Curve(P, [
  x1*x2 - x0*x3 + x3^2 - x2*x4 + x4^2,
  -x1^2 + x0*x2 + x1*x3 - x0*x4 + x1*x4 - x2*x4 + x4^2,
  -x1*x3 + x2*x3 + x3^2 + x0*x4 - 2*x3*x4 - x4^2
]);
