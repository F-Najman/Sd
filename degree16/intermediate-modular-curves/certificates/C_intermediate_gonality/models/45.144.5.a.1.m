// X_Delta(N) for N = 45, Delta = <-1,4> = {±1,±4,±11,±14,±16,±19}
// LMFDB label 45.144.5.a.1; index 144, genus 5, 16 cusps.
//
// Canonical model: 3 quadrics in P^4 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(45, [11, 44]), minimize_strategy="LLL")
// sage-group: GammaH(45, [11, 44])
// Coordinates x0, ..., x4 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(45, [11, 44]): x0 vanishes to order 1 at infinity and x1, ..., x4 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 45;
Delta := [1, 4, 11, 14, 16, 19, 26, 29, 31, 34, 41, 44];
g := 5;
P<x0,x1,x2,x3,x4> := ProjectiveSpace(Rationals(), 4);
X := Curve(P, [
  x2^2 - x1*x3 + x0*x4,
  x1^2 - x0*x2 + x2*x3 - x1*x4 - x4^2,
  x1*x2 - x0*x3 + 2*x3^2 - 3*x2*x4
]);
