// X_Delta(N) for N = 48, Delta = <-1,11> = {±1,±11,±13,±23}
// LMFDB label 48.192.5.ky.2; index 192, genus 5, 24 cusps.
//
// Canonical model: 3 quadrics in P^4 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(48, [13, 47]), minimize_strategy="LLL")
// sage-group: GammaH(48, [13, 47])
// Coordinates x0, ..., x4 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(48, [13, 47]): x0 vanishes to order 1 at infinity and x1, ..., x4 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 48;
Delta := [1, 11, 13, 23, 25, 35, 37, 47];
g := 5;
P<x0,x1,x2,x3,x4> := ProjectiveSpace(Rationals(), 4);
X := Curve(P, [
  -x2*x3 + x0*x4,
  -x1^2 + x0*x2 - x2*x3 - x0*x4,
  -x2^2 + x0*x3 - x3^2 + 3*x2*x4 - 3*x4^2
]);
