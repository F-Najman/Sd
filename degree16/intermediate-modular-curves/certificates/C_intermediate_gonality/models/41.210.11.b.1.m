// X_Delta(N) for N = 41, Delta = <-1,3> = {±1,±3,±9,±14}
// LMFDB label 41.210.11.b.1; index 210, genus 11, 10 cusps.
//
// Canonical model: 36 quadrics in P^10 over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit 6022429) as
//   vanishing_quadratic_forms(GammaH(41, [27]), minimize_strategy="LLL")
// sage-group: GammaH(41, [27])
// Coordinates x0, ..., x10 are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH(41, [27]): x0 vanishes to order 1 at infinity and x1, ..., x10 to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := 41;
Delta := [1, 3, 9, 14, 27, 32, 38, 40];
g := 11;
P<x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10> := ProjectiveSpace(Rationals(), 10);
X := Curve(P, [
  -x6*x7 + x6*x8 + x0*x10 + x3*x10 - x4*x10 - x5*x10 - 2*x7*x10 + x10^2,
  x6*x8 - x1*x10 - x3*x10 + x4*x10 + x5*x10 + x7*x10 - 2*x8*x10 + x9*x10 - x10^2,
  x6*x7 - x6*x8 - x6*x9 - x0*x10 + x3*x10 + x5*x10 + 2*x6*x10 + x7*x10 + x10^2,
  -x6^2 + x6*x7 + x3*x8 - x4*x8 - x8^2 - x3*x9 + x4*x9 - x6*x9 + x8*x9 - x2*x10 + x5*x10 + x7*x10 - x8*x10,
  -x6^2 + x4*x7 - x5*x7 - x4*x8 + x6*x8 + x4*x9 - x6*x9 + x9^2 + x0*x10 - x1*x10 + x6*x10 - x7*x10 - x8*x10 - x9*x10,
  x6*x7 + x6*x8 - x3*x9 + x7*x9 - x8*x9 + x0*x10 - x1*x10 + x2*x10 + x6*x10 - x7*x10 - x8*x10 - x9*x10,
  -x1*x5 + x2*x5 - x3*x5 + x4*x5 + x0*x6 - x5*x6 - x6*x7 - x5*x9 + x1*x10 - x2*x10 + x3*x10 - x4*x10 + x9*x10,
  -x5^2 + x4*x6 - x5*x6 + x6*x8 + x0*x9 - x4*x9 - x5*x9 + x6*x9 - x7*x9 - x8*x9 + x0*x10 + x1*x10 - x2*x10 - x5*x10 - x6*x10 - x7*x10 + x9*x10,
  -x4*x6 + x5*x6 - x6^2 + x4*x7 + x1*x8 - x2*x8 - x3*x8 - x5*x8 + 2*x8^2 + x7*x9 - x8*x9 - x1*x10 + x2*x10 - x6*x10 - x8*x10 - x10^2,
  x4*x5 - x5^2 - x3*x6 + x5*x6 - x6^2 + x5*x7 - x5*x8 + x1*x9 - x2*x9 - x6*x9 + x8*x9 - x4*x10 - 2*x6*x10 + x7*x10 - x8*x10,
  x3*x5 - x3*x6 + x6^2 - x0*x7 + x5*x7 + x7^2 + x0*x8 - x5*x8 - x8^2 + x2*x10 - x3*x10 - x4*x10 + x5*x10 + x8*x10 - 2*x9*x10,
  x3*x5 - x0*x7 - x4*x7 + x5*x7 + x6*x7 + x7^2 + x2*x8 + x4*x8 - x6*x8 + x7*x8 - x7*x9 + x2*x10 - x4*x10 + x5*x10 - 2*x9*x10 + x10^2,
  x3*x5 - x3*x6 + x5*x6 - x0*x7 + x7^2 + x0*x8 + x2*x8 - x6*x8 - x7*x8 + x8^2 - x0*x9 + x3*x9 + x5*x9 + x2*x10 - x4*x10 - x6*x10 - x9*x10 + x10^2,
  x1*x5 - x2*x5 - x5^2 - x0*x6 + x0*x7 - x4*x7 - x7^2 - x0*x8 + x4*x8 + x5*x8 + x6*x8 + x8^2 + x0*x9 + x1*x9 - x2*x9 - x4*x9 - x5*x9 - x7*x9 - x1*x10 + x2*x10 - x8*x10 + x10^2,
  -x5^2 - x3*x6 + x4*x6 - x5*x6 + x3*x7 - x5*x7 - x7^2 + x0*x8 - x4*x8 + x5*x8 - x8^2 - x5*x9 + x1*x10 - x2*x10 + x3*x10 - x4*x10 + x5*x10 + x9*x10 + x10^2,
  2*x6^2 - x5*x7 - x6*x7 + x5*x8 - x1*x9 + x2*x9 + x3*x9 + x6*x9 - x7*x9 - x4*x10 + 2*x5*x10 - x7*x10 + x8*x10,
  -x4*x5 + x5^2 - x4*x6 - x6^2 + x1*x7 - x5*x7 - x6*x7 - x2*x8 - x3*x8 + x4*x8 + x7*x8 + x8^2 - x5*x9 + x2*x10 + x3*x10 - x5*x10 - x7*x10 + x8*x10 - x10^2,
  x3*x5 - x4*x5 - x2*x6 - x5*x6 - x6^2 + x6*x7 + x1*x8 - x2*x8 - x5*x8 - x6*x8 + x8^2 + x0*x9 - x3*x9 - 2*x5*x9 + x6*x9 - x8*x9 + 2*x5*x10 + x6*x10 - x10^2,
  -x5*x6 + x6^2 - x4*x7 + x6*x7 + x2*x8 - x6*x8 - x5*x9 - x7*x9 + x0*x10 + x1*x10 - x3*x10 - x4*x10 + x5*x10 + x6*x10 - x9*x10 - x10^2,
  -x3*x6 + 2*x6^2 + x4*x7 + x0*x8 - x2*x8 - x3*x8 - x5*x8 - x6*x8 - x7*x8 + x6*x9 + x7*x9 - x1*x10 + x2*x10 - x3*x10 + x5*x10 - x6*x10 - x8*x10 - 2*x10^2,
  x3*x6 - x4*x6 - x1*x7 + x2*x7 + x1*x8 - x2*x8 - x6*x8 - x7*x8 + x8^2 - x7*x9 + x8*x9 + x6*x10 + x7*x10 - x8*x10,
  x1*x5 - x2*x5 + x3*x5 - x4*x5 - x0*x6 + x4*x6 - x5*x6 + x5*x7 - x1*x8 + x5*x8 + x6*x8 - x8^2 + x0*x9 + x1*x9 - x2*x9 - x3*x9 - x5*x9 - x1*x10 + x2*x10 + x3*x10 - x7*x10,
  -x6^2 - x3*x7 + x5*x7 + x2*x8 - x5*x8 + x7*x8 + x1*x9 - x2*x9 + x3*x9 - x4*x9 - x5*x9 - x6*x9 - x7*x9 + x2*x10 - x3*x10 + x4*x10 + x6*x10 + x9*x10 - 2*x10^2,
  -x3*x5 + x2*x6 + x3*x6 - x5*x6 - x6^2 - x4*x7 + x6*x7 + x2*x8 + x3*x8 + x5*x8 - x7*x8 + x8^2 - x5*x9 - x6*x9 - x7*x9 - x0*x10 + x3*x10 + x4*x10 + x5*x10 + x7*x10 + x9*x10,
  x4*x6 - x5*x6 + x6^2 - x4*x7 + x5*x7 - x1*x8 + x2*x8 + x3*x8 + x4*x8 - x7*x8 - x2*x9 + x5*x9 - x8*x9 + x9^2 - x0*x10 + x3*x10 + x4*x10 - x5*x10 + x6*x10 + x7*x10 + x9*x10 + x10^2,
  -x3^2 + x3*x4 - x5^2 + x0*x6 + x3*x7 + x5*x7 - x2*x8 - 2*x5*x8 - x6*x8 - x8^2 + x0*x9 - x3*x9 + x1*x10 - x2*x10 - x3*x10 - x6*x10 + x7*x10 + x8*x10 - x9*x10,
  -x2*x4 + x1*x5 + x3*x5 - x4*x5 - x3*x6 - x4*x6 + x6^2 + x5*x7 + x1*x8 - x2*x8 - x3*x8 - x4*x8 + x7*x8 - x5*x9 + x7*x9 - x8*x9 - x9^2 + x2*x10 - 2*x3*x10 + x4*x10 + x8*x10 - x10^2,
  -x2*x3 + x0*x5 + x2*x5 - x5^2 + x5*x6 - x1*x7 + x2*x7 - x6*x7 - x3*x8 + x6*x8 - x8^2 - x0*x9 + x1*x9 - x2*x9 + x3*x9 + x7*x9 + x8*x9 - x1*x10 + x4*x10 - x5*x10 - x6*x10 - x7*x10 + x9*x10,
  x3*x4 - x4^2 + x4*x5 - x1*x6 - x3*x6 - x4*x7 + x5*x7 - x6*x7 + x1*x8 - x2*x8 + x3*x8 - x4*x8 + x6*x8 - x3*x9 - x5*x9 + x7*x9 - x9^2 + x0*x10 - x4*x10 + x5*x10 - x7*x10 + x9*x10 - x10^2,
  x1*x5 - x3*x5 - x5^2 - x0*x6 - x1*x6 + x2*x6 + x3*x6 + x5*x6 + x6^2 + 2*x5*x8 - x5*x9 - x0*x10 - x1*x10 + x4*x10 + x5*x10 + x6*x10 + x7*x10 - x8*x10 + x9*x10,
  -x3*x4 + x2*x5 + x4*x5 - x5^2 - x4*x6 + x6^2 - x5*x7 - x6*x7 + x4*x8 + 2*x5*x8 - x0*x9 + x7*x9 + x8*x9 - x1*x10 + x6*x10 - x7*x10 - x8*x10 + x9*x10,
  x3^2 + x1*x4 - x2*x4 - x3*x4 - x0*x5 + x3*x5 - x4*x5 + x5^2 - x5*x6 + x6^2 + x0*x7 - x5*x7 - x7^2 - x0*x8 + x5*x8 - x6*x8 + x3*x9 + x4*x9 - x7*x9 + x8*x9 + x9^2 + x0*x10 - x2*x10 - x3*x10 + x5*x10 - x9*x10,
  x1*x3 - x2*x3 - x0*x4 + x0*x5 + x3*x5 - x1*x6 + x2*x6 + x4*x6 + x6^2 - x0*x7 - x1*x7 + x2*x7 + x7^2 + x2*x8 + x3*x8 + x4*x8 - x6*x8 - x0*x9 + x3*x9 + x5*x9 - x7*x9 + x8*x9 + x0*x10 + x2*x10 - 2*x7*x10 + x8*x10 - x9*x10,
  x1*x2 - x0*x3 + x3^2 - x2*x4 - x2*x5 + x4*x5 - x1*x6 + x5*x6 + x0*x7 - x0*x8 + x1*x8 - x4*x8 - x5*x8 - x2*x9 - x3*x9 + x4*x9 + x7*x9 - x1*x10 + 2*x5*x10 + x6*x10 + x7*x10 - x8*x10 - x9*x10,
  -x1*x2 + x2^2 + x0*x3 - x0*x4 - x3*x5 + x4*x5 - x5*x6 - x0*x7 - x3*x7 + x6*x7 + x7^2 + x3*x8 + x4*x8 + x5*x8 - x2*x9 + x6*x9 - x7*x9 + x9^2 + x0*x10 - x3*x10 + x4*x10 - x7*x10,
  x1^2 - x0*x2 - x1*x2 + x0*x3 + x2*x3 - x1*x4 + x2*x4 - x3*x4 + x4^2 - x1*x5 + x2*x5 - x4*x5 + x5^2 + x3*x6 - x6^2 - x6*x7 - x7^2 + x1*x8 + x2*x8 - x4*x8 - x6*x8 + x8^2 + x0*x9 + x2*x9 - x3*x9 - x5*x9 - x8*x9 - x9^2 + x2*x10 - x4*x10 + x6*x10 - x9*x10 + x10^2
]);
