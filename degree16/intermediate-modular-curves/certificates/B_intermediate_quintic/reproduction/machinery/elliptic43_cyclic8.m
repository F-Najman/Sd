// Isogeny-invariant cyclic-eight reduction needed by the translate test.
E := EllipticCurve([Rationals()|0,1,1,0,0]);
assert Conductor(E) eq 43;
lo,hi := RankBounds(E);
assert lo eq 1 and hi eq 1;
// No rational 2-isogeny. A minimal isogeny from E to another Q-isogenous
// elliptic curve has cyclic kernel, hence has odd degree. Such an isogeny
// identifies the 2-primary groups of good reductions.
assert IsIrreducible(DivisionPolynomial(E,2));
E7 := ChangeRing(E,GF(7));
assert #Points(E7) eq 8;
assert #Roots(ChangeRing(DivisionPolynomial(E,2),GF(7))) eq 1;
// Exactly one nonzero rational 2-torsion point: the order-eight group is
// cyclic. Thus every Q-elliptic curve in this isogeny class has cyclic
// order-eight reduction at 7 as well.
print "SUCCESS: every Q-isogenous elliptic direction has cyclic order eight at seven";
quit;
