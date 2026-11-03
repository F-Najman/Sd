// The three rational divisor classes used in prove_lower_bound_7.m to generate the group C are torsion,
// checked directly over Q. With D1 = C2 - C1, D2 = C3 - C1 and E = C(3) - (C1 + C2 + C3) we check that 38 D1,
// 38 D2 and 7 E are principal; then C(3) - 3 C3 = E + (D1 - D2) - D2 is torsion too. This replaces the
// identification of the points as cusps (and Manin-Drinfeld) in the proof.
SetQuitOnError(true); SetMemoryLimit(40 * 2^30);
None := 0;
load "lmfdb_43.132.9.a.2.m";
K := Rationals();
P8 := ProjectiveSpace(K, 8); S := CoordinateRing(P8);
X := Curve(P8, [Evaluate(q, [S.i : i in [1..9]]) : q in model_0]);
P2<A,B,C> := ProjectiveSpace(K, 2);
Cplane := Curve(P2, Evaluate(model_1[1], [A,B,C] cat [K!0 : i in [4..9]]));
pr := map<X -> Cplane | [S.7, S.8, S.9]>;
cs := [FunctionFieldDivisor(Pullback(pr, Places(P)[1])) : P in [Cplane![0,0,1], Cplane![0,1,0], Cplane![1,0,0]]];
P20<U,V,W> := ProjectiveSpace(K, 2);
L := [Evaluate(f, [S.i : i in [1..9]]) : f in [map_0_coord_0, map_0_coord_1, map_0_coord_2]];
C0 := Curve(P20, Evaluate(map_0_codomain[1], [U,V,W] cat [K!0 : i in [4..9]]));
c3 := FunctionFieldDivisor(Pullback(map<X -> C0 | L>, Place(C0![0,1,0])));
assert [Degree(c) : c in cs] eq [1, 1, 1] and Degree(c3) eq 3;
assert c3 - 3*cs[3] eq (c3 - cs[1] - cs[2] - cs[3]) + ((cs[2] - cs[1]) - (cs[3] - cs[1])) - (cs[3] - cs[1]);
for t in [<38, cs[2] - cs[1]>, <38, cs[3] - cs[1]>, <7, c3 - cs[1] - cs[2] - cs[3]>] do
    assert Dimension(t[1] * t[2]) ge 1;       // degree 0 and a nonzero section: principal
    printf "TORSION class of order dividing %o\n", t[1];
end for;
print "ALL_THREE_CLASSES_TORSION"; quit;
