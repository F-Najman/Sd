// All possible positive Mordell-Weil directions for the specified curve.
delta := [1,2,4,8,11,16,21,22,27,32,35,39,41,42];
J := JH(43,delta);
assert Dimension(J) eq 9;
factors := Factorization(J);
assert &+[Dimension(t[1])*#t[2]:t in factors] eq 9;
potential := [* t:t in factors|IsZeroAt(LSeries(t[1]),1) *];
assert #potential eq 1;
assert Dimension(potential[1][1]) eq 1 and #potential[1][2] eq 1;
E := EllipticCurve([Rationals()|0,1,1,0,0]);
assert IsIsogenous(E,EllipticCurve(potential[1][1]));
assert Conductor(E) eq 43;
lo,hi := RankBounds(E);
assert lo eq 1 and hi eq 1;
assert #Points(ChangeRing(E,GF(2))) eq 5;
print "SUCCESS: unique elliptic Mordell-Weil direction with reduction order five at two";
quit;
