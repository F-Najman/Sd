// X_Delta(N) for N = 37, Delta = <-1,10> = {±1,±10,±11}
// LMFDB label 37.228.10.a.2; index 228, genus 10, 12 cusps.
//
// Canonical model: 28 quadrics in P^9 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(37, [11]), minimize_strategy="LLL")
// sage-group: GammaH(37, [11])
// Coordinates x0, ..., x9 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(37, [11]): x0 vanishes to order 1 at infinity and x1, ..., x9 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 37;
Delta := [1, 10, 11, 26, 27, 36];
g := 10;
P<x0,x1,x2,x3,x4,x5,x6,x7,x8,x9> := ProjectiveSpace(Rationals(), 9);
X := Curve(P, [
  -x3*x7 + x6*x7 + x7^2 + x2*x8 + x3*x8 - x5*x8 - 2*x6*x8 - x8^2 - x2*x9 + x5*x9 + x6*x9 - x7*x9 + x9^2,
  x3*x7 - x6*x7 - x7^2 - x2*x8 - x4*x8 + 2*x5*x8 + x7*x8 + x8^2 + x4*x9 - x5*x9 + x6*x9 - x7*x9 - x8*x9 + x9^2,
  -x2*x7 + x3*x7 - x4*x7 + x5*x7 + x2*x8 - x3*x8 + x4*x8 - x5*x8 + x7*x8 - x8^2 + x0*x9 - x1*x9 - x4*x9 + x5*x9 - x6*x9 + x7*x9 + x8*x9 + x9^2,
  x4*x7 - x5*x7 + x6*x7 - 2*x7^2 - x2*x8 - x4*x8 + 2*x5*x8 + x7*x8 + x8^2 + x1*x9 - x4*x9 - x5*x9 + x6*x9 - 2*x9^2,
  x4*x6 - x6*x7 - x2*x8 - x4*x8 + x5*x8 - x6*x8 + x7*x8 + 2*x8^2 - x4*x9 + x6*x9 + x7*x9 + 2*x8*x9 - x9^2,
  -x3*x6 + x6^2 + x3*x7 - x7^2 - x3*x8 + x4*x8 + x6*x8 - x7*x8 - x8^2 + x0*x9 + x3*x9 - 2*x4*x9 - x6*x9 - x7*x9 + 2*x8*x9 - x9^2,
  -x3*x7 + x4*x7 - x5*x7 + 2*x6*x7 - x7^2 + x1*x8 + x3*x8 - 2*x4*x8 - x6*x8 + x7*x8 - x8^2 - x0*x9 + x3*x9 + x4*x9 - x6*x9 - x8*x9,
  x3*x6 - x4*x6 - x6^2 - x4*x7 + x7^2 - x1*x8 + x2*x8 + 2*x4*x8 + 2*x7*x8 - 2*x8^2 - x3*x9 + x4*x9 - x7*x9 + x9^2,
  x5*x6 - x3*x8 - x5*x8 + x7*x8 + x8^2 - x5*x9 - 2*x6*x9 + 3*x8*x9 + 2*x9^2,
  x6^2 - x1*x7 + x4*x7 + x5*x7 - x6*x7 + x0*x8 - x3*x8 - x4*x8 - x6*x8 + x7*x8 + x1*x9 - x2*x9 - x3*x9 + x7*x9 + x8*x9 + 2*x9^2,
  -x2*x6 + 2*x6^2 - x6*x7 + x0*x8 + x2*x8 - x4*x8 - x6*x8 - x7*x8 - x8^2 + x2*x9 - x6*x9 + x7*x9 - 2*x8*x9 - x9^2,
  x5*x6 - x6^2 + x3*x7 - x4*x7 + x5*x7 - x6*x7 + x7^2 - x3*x8 + x4*x8 - x5*x8 - x7*x8 - x1*x9 + x4*x9 - x5*x9 + 2*x6*x9 - x7*x9 + 3*x8*x9 + x9^2,
  -x3*x4 + x4^2 + x2*x5 - x4*x5 - x5^2 + x4*x6 - x6^2 - x4*x7 + 2*x6*x7 - x0*x8 + x1*x8 - x2*x8 + 2*x3*x8 - x4*x8 + x5*x8 + x7*x8 - x8^2 - x2*x9 + x6*x9 - x7*x9 - x9^2,
  x3*x4 - x4^2 + x4*x5 - x1*x6 + x1*x7 - x2*x7 - x5*x7 + x6*x7 - x7^2 - x3*x8 + 2*x6*x8 + x7*x8 + x8^2 + x3*x9 - x4*x9 + x6*x9 + x7*x9 - 2*x8*x9 + x9^2,
  x1*x6 - x4*x6 - x5*x6 - x0*x7 - x2*x7 + x3*x7 + x4*x7 + x6*x7 + x5*x8 + x0*x9 - 2*x1*x9 + 2*x5*x9 - x6*x9 + 2*x7*x9 - x8*x9 + x9^2,
  -x2*x5 + x4*x5 + x5^2 + x2*x6 - x3*x6 - x5*x6 + x0*x7 + x3*x7 - x4*x7 - x5*x7 - x6*x7 - 2*x7^2 - x0*x8 + x3*x8 + x7*x8 + x2*x9 + x3*x9 - x4*x9 - x6*x9 + 2*x7*x9 - x9^2,
  -x3*x4 + x4^2 + x3*x5 - x4*x5 + x1*x6 - x3*x6 - x5*x6 + x6^2 - x1*x7 + x2*x7 - x5*x7 + x7^2 - x0*x8 + x3*x8 + x4*x8 - x6*x8 + x7*x8 + x0*x9 - x2*x9 - 2*x3*x9 + x5*x9 + x6*x9,
  x2*x3 - x3^2 + x3*x4 - x4^2 - x0*x5 + x4*x5 + x0*x6 - x1*x6 - x6^2 + x1*x7 - x2*x7 + x3*x7 + x5*x7 - x6*x7 - x7^2 + x1*x8 - x5*x8 - x8^2 - x0*x9 - x2*x9 + x3*x9 + x5*x9 + x6*x9 - x7*x9 - x8*x9 + 2*x9^2,
  -x1*x3 + x0*x4 - x4^2 + x3*x5 + x1*x6 - x4*x6 - x5*x6 - x0*x7 + x1*x7 + 2*x3*x7 - x4*x7 - x5*x7 - x6*x7 - x0*x8 + x3*x8 + 2*x4*x8 - x8^2 + x4*x9 - x7*x9 - x8*x9,
  x2*x3 - x3^2 + x3*x4 - x0*x5 + x1*x5 - x2*x5 + x4*x5 - x3*x6 - x4*x6 + x5*x6 + x2*x7 - 2*x5*x7 + x6*x7 + x7^2 - x2*x8 + x3*x8 - x4*x8 - x5*x8 + x6*x8 - x7*x8 - x0*x9 - x1*x9 + x3*x9 + 2*x4*x9 + x6*x9 - x7*x9 + x8*x9 + x9^2,
  -x1*x5 + x2*x5 + x0*x6 - x4*x6 - x6^2 - x0*x7 + x1*x7 - x2*x7 + x5*x7 + x6*x7 + x7^2 - x0*x8 + x1*x8 + x6*x8 + x8^2 + x1*x9 - x2*x9 - x4*x9 - x5*x9 - x6*x9 - 2*x8*x9 + 2*x9^2,
  x4*x5 - x3*x6 - x5*x6 + x6^2 + x3*x7 - x5*x7 - x7^2 - x4*x8 - x5*x8 + x6*x8 + x7*x8 + x8^2 - x1*x9 + 2*x3*x9 - x4*x9 + 2*x5*x9 + 2*x8*x9 - 2*x9^2,
  x2*x3 - x2*x4 - x0*x5 + x2*x5 + x4*x5 - x5^2 + x0*x6 - x2*x6 - x3*x6 + x4*x6 - x0*x7 + x1*x7 - x3*x7 - x5*x7 + x6*x7 + x7^2 + x5*x8 + 2*x7*x8 - x3*x9 - x4*x9 - x6*x9 + x7*x9 - x9^2,
  -x2*x4 + x4^2 + x1*x5 - x3*x5 - x5^2 + x2*x6 - x3*x6 + x4*x6 + x5*x6 - x1*x7 + x2*x7 - x4*x7 + x7^2 - x1*x8 + x5*x8 - x6*x8 + x0*x9 + x1*x9 - 2*x2*x9 - x4*x9 + x7*x9 + x8*x9 + x9^2,
  x1*x4 - x4^2 - x0*x5 + x3*x5 - x6^2 - x1*x7 - x3*x7 + x4*x7 + x5*x7 + 2*x6*x7 + x7^2 + x0*x8 + x2*x8 - x4*x8 - x5*x8 - x7*x8 - 2*x8^2 - x1*x9 + x2*x9 - x5*x9 - x6*x9 + x7*x9 - x8*x9 + x9^2,
  x1^2 - x0*x2 - x1*x3 + x2*x3 - x3^2 + x0*x4 - x1*x4 + x2*x4 + x3*x4 - x4^2 - x1*x5 + x3*x5 + x0*x6 - x6^2 - x0*x7 + x2*x7 + x3*x7 - x5*x7 - x6*x7 + x7^2 - x1*x8 - x2*x8 + x6*x8 + 3*x8^2 - x1*x9 + x5*x9 + x6*x9 + x7*x9 - x8*x9 - x9^2,
  -x1*x2 + x0*x3 + x1*x3 - x3^2 - x0*x4 + x2*x4 - x3*x4 + x4^2 + x1*x5 + x2*x5 - x3*x5 - x5^2 - x0*x6 + x3*x6 - x6^2 - x5*x7 + x6*x7 + x7^2 - x1*x8 + x2*x8 + x3*x8 - x4*x8 - x6*x8 + x7*x8 + x8^2 + x3*x9 - x4*x9 - 2*x5*x9 + 2*x6*x9 + 2*x9^2,
  x1*x2 - x2^2 - x0*x3 + x0*x4 - x2*x4 + x3*x4 - x4^2 + x2*x5 - x5^2 + x0*x6 - x1*x6 + x2*x6 - x4*x6 + x6^2 - x0*x7 + 2*x3*x7 - x5*x7 - x6*x7 - x1*x8 - x3*x8 + 2*x4*x8 + x5*x8 + x6*x8 + x0*x9 - 2*x1*x9 + x2*x9 + 2*x4*x9 + x5*x9 - x6*x9 - 2*x7*x9 - x8*x9 - x9^2
]);
