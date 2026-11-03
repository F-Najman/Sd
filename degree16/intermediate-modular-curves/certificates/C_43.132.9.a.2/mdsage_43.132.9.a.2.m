// X_Delta(N) for N = 43, Delta = <-1,2> = {±1,±2,±4,±8,±11,±16,±21}
// LMFDB label 43.132.9.a.2; index 132, genus 9, 6 cusps.
//
// Canonical model: 21 quadrics in P^8 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(43, [8]), minimize_strategy="LLL")
// sage-group: GammaH(43, [8])
// Coordinates x0, ..., x8 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(43, [8]): x0 vanishes to order 1 at infinity and x1, ..., x8 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 43;
Delta := [1, 2, 4, 8, 11, 16, 21, 22, 27, 32, 35, 39, 41, 42];
g := 9;
P<x0,x1,x2,x3,x4,x5,x6,x7,x8> := ProjectiveSpace(Rationals(), 8);
X := Curve(P, [
  x4*x6 - x6^2 - x4*x7 + x7^2 - x0*x8 + x3*x8 - x4*x8 + x5*x8 - x6*x8 + x7*x8 + 2*x8^2,
  x2*x4 - x4*x5 - x0*x6 - x2*x6 + 2*x5*x6 + x6*x7 + x2*x8 - 2*x4*x8 - x6*x8,
  x2*x5 - x5^2 - x2*x6 + x5*x6 - x0*x7 - x2*x7 + 2*x5*x7 + x7^2 - x4*x8 - x5*x8 + x6*x8 + x7*x8,
  x2*x5 - x5^2 - x2*x6 - x3*x6 + x4*x6 + 2*x6^2 - x0*x7 + x3*x7 + x4*x7 + x5*x7 - x7^2 - x0*x8 + x3*x8 - x5*x8 + x7*x8 + x8^2,
  x1*x6 - x2*x6 - x3*x6 + x5*x6 - x0*x7 + x2*x7 - x4*x7 - x6*x7 + 2*x7^2 + x0*x8 + x2*x8 - x3*x8 - x5*x8 - 2*x8^2,
  x2*x5 - x5^2 - x1*x6 - x2*x6 + x3*x6 + x4*x6 + x5*x6 - x6^2 + x1*x7 - x2*x7 - x3*x7 + x5*x7 + x6*x7 - 2*x7^2 + x2*x8 - 2*x5*x8 - x8^2,
  -x2*x4 + x3*x4 + x0*x6 - x1*x6 + x2*x6 - x5*x6 - x3*x7 + x5*x7 + x6*x7 - x1*x8 + x3*x8 + 2*x4*x8 - x6*x8 - 2*x7*x8 - x8^2,
  -x2*x4 + x4^2 + x1*x5 - x3*x5 - x1*x6 + 2*x2*x6 + x3*x6 - x4*x6 - x5*x6 + x0*x7 - x1*x7 - x2*x7 + x3*x7 - x5*x7 + x6*x7 + x0*x8 + x1*x8 - x2*x8 - 2*x3*x8 + x5*x8 - x6*x8,
  -x2^2 + x2*x3 + x0*x4 - x1*x4 + x4*x5 + 2*x2*x6 - x3*x6 - x4*x6 - x5*x6 + x6^2 - x1*x7 + x2*x7 + x3*x7 - x5*x7 - x0*x8 - x1*x8 + x2*x8 + 2*x3*x8 + x4*x8 + x6*x8 - 2*x7*x8,
  -x2*x3 + x1*x4 + x2*x5 - 2*x4*x5 - x1*x6 + 2*x3*x6 + x4*x6 - x5*x6 - x6^2 + x4*x7 + x2*x8 - x4*x8 - 4*x6*x8,
  x2^2 - x1*x3 - x2*x3 + x3^2 + x1*x4 - x2*x4 - 2*x4^2 + x3*x5 + x4*x5 - x5^2 + x5*x6 - x6^2 + x1*x7 - x2*x7 - x3*x7 + x5*x7 - x7^2 - x1*x8 - 2*x2*x8 + x3*x8 + x5*x8 - x6*x8 + x7*x8 + x8^2,
  -x1*x3 + x3^2 + x0*x4 - x2*x4 + x1*x5 + x2*x5 - x3*x5 - x5^2 - x0*x6 - x4*x6 + x5*x6 + x6^2 - x0*x7 + 2*x3*x7 - x5*x7 + x6*x7 - x0*x8 - x1*x8 + x2*x8 + x3*x8 + 3*x7*x8,
  -x1*x3 + x0*x4 - x4^2 + x1*x5 + x3*x5 - x5^2 - x0*x6 + x3*x6 - x4*x6 - x5*x6 + 2*x3*x7 - 2*x5*x7 + 2*x6*x7 - x7^2 - x0*x8 - x3*x8 - x4*x8 + 2*x5*x8 + x7*x8 + x8^2,
  x1*x3 + x2*x3 - x3^2 - x0*x4 - x1*x4 + x3*x4 + x4^2 - x3*x5 + x4*x5 + x0*x6 - 2*x1*x6 + x4*x6 + 2*x6^2 + x0*x7 + x1*x7 - 2*x2*x7 - x3*x7 + x4*x7 - 2*x7^2 + x1*x8 - x3*x8 + x4*x8 - x5*x8 - x6*x8 + x7*x8,
  -x1*x4 + 2*x3*x4 - x4^2 + x0*x5 + x1*x5 - x3*x5 + x4*x5 - 2*x5^2 - x0*x6 - x1*x6 + x2*x6 + 2*x5*x6 + x6^2 - x0*x7 - x2*x7 - x4*x7 + x5*x7 + x0*x8 - x2*x8 - x4*x8 - x5*x8 - x6*x8 - x7*x8,
  -x2*x3 + x3^2 + x1*x4 + x2*x4 - x3*x4 - x4^2 - x1*x5 - x4*x5 + x5^2 - x0*x6 + x1*x6 + x2*x6 - x6^2 - x1*x7 - x3*x7 + x4*x7 + 2*x5*x7 + x6*x7 + x7^2 - 2*x4*x8 + 2*x7*x8,
  -x2^2 + x0*x4 + 2*x2*x4 - x3*x4 - x4^2 - x1*x5 + x3*x5 + x5^2 - x0*x6 + x1*x6 + x3*x6 - 2*x4*x6 - x5*x6 + x2*x7 - x4*x7 - 2*x5*x7 + x6*x7 + 2*x7^2 + x1*x8 + 2*x2*x8 - x3*x8 - x4*x8 - x5*x8 - x6*x8,
  x1*x3 - x3^2 - x0*x4 + x2*x4 + x4^2 - x1*x5 - x4*x5 + x5^2 + x0*x6 - x2*x6 + x5*x6 - 3*x6^2 + 2*x4*x7 - x1*x8 + 2*x2*x8 + x3*x8 - x5*x8 - 2*x8^2,
  -x2^2 + x2*x3 + x0*x4 + x2*x4 - x3*x4 - x4^2 - x0*x5 - x1*x5 + x3*x5 + x5^2 + x2*x6 + x5*x6 - 2*x6^2 + x0*x7 - x3*x7 - 2*x4*x7 + 2*x5*x7 - x6*x7 - x7^2 - x0*x8 + 2*x2*x8 - x4*x8,
  -x1*x2 + x0*x3 + x2*x3 - x0*x5 + x1*x5 - 2*x3*x5 - x4*x5 + x5^2 - x0*x6 + 2*x2*x6 + x4*x6 - x6^2 + x2*x7 - x3*x7 + x4*x7 + x5*x7 - x6*x7 - x7^2 + x1*x8 - x2*x8 - x3*x8 + x4*x8 + x5*x8 - x7*x8 + x8^2,
  -x1^2 + x0*x2 + x1*x2 - x2^2 - x0*x3 + x1*x3 - x3*x4 - 2*x4^2 + x1*x5 - x2*x5 + x3*x5 + 2*x4*x5 - x5^2 - x0*x6 + x1*x6 - x3*x6 + 2*x4*x6 + x6^2 + x0*x7 - 2*x2*x7 - x4*x7 - x1*x8 + x2*x8 - x4*x8 + x5*x8 - x8^2
]);
