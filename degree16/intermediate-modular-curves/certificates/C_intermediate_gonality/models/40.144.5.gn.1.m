// X_Delta(N) for N = 40, Delta = <-1,9,11> = {±1,±9,±11,±19}
// LMFDB label 40.144.5.gn.1; index 144, genus 5, 16 cusps.
//
// Canonical model: 3 quadrics in P^4 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(40, [9, 21, 31]), minimize_strategy="LLL")
// sage-group: GammaH(40, [9, 21, 31])
// Coordinates x0, ..., x4 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(40, [9, 21, 31]): x0 vanishes to order 1 at infinity and x1, ..., x4 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 40;
Delta := [1, 9, 11, 19, 21, 29, 31, 39];
g := 5;
P<x0,x1,x2,x3,x4> := ProjectiveSpace(Rationals(), 4);
X := Curve(P, [
  -x2^2 + x0*x3 - x3^2 + 2*x2*x4 - x4^2,
  x2*x3 - x0*x4 - 2*x3*x4 + 2*x4^2,
  x1^2 - x0*x2 + 2*x2*x3 - x3^2 + 2*x0*x4 - x3*x4 - 2*x4^2
]);
