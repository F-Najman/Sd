// X_Delta(N) for N = 32, Delta = <-1,15> = {±1,±15}
// LMFDB label 32.192.5.bu.1; index 192, genus 5, 24 cusps.
//
// Canonical model: 3 quadrics in P^4 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(32, [17, 31]), minimize_strategy="LLL")
// sage-group: GammaH(32, [17, 31])
// Coordinates x0, ..., x4 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(32, [17, 31]): x0 vanishes to order 1 at infinity and x1, ..., x4 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 32;
Delta := [1, 15, 17, 31];
g := 5;
P<x0,x1,x2,x3,x4> := ProjectiveSpace(Rationals(), 4);
X := Curve(P, [
  x3^2 - x0*x4 + x4^2,
  -x1*x2 + x0*x3 + 2*x1*x4 - 2*x3*x4,
  -x1^2 + x0*x2 - x2^2 + 2*x1*x3 - x3^2 - x0*x4 + 2*x2*x4 - x4^2
]);
