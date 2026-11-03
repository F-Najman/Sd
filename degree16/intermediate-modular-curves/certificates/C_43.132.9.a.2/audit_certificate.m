// Adversarial checks for the claimed gonality proof of 43.132.9.a.2.
//
// This file deliberately checks interfaces that the original short
// certificate only described in comments: cusp identification, good
// reduction, the elliptic quotient, and the modular-factor calculations.

None := 0;
load "lmfdb_43.132.9.a.2.m";

Q := Rationals();
P8Q := ProjectiveSpace(Q,8);
SQ := CoordinateRing(P8Q);
XQ := Curve(P8Q,[Evaluate(q,[SQ.i:i in [1..9]]):q in model_0]);
assert Genus(XQ) eq 9;
// Direct IsNonsingular on this 21-quadric canonical presentation takes
// several minutes and is not needed for any subsequent exact calculation:
// the algorithmic function field used below automatically works with the
// smooth projective curve having this function field.
printf "CHECK|Q_FUNCTION_FIELD_GENUS=9\n";

// The stored degree-3 map X -> X_0(43).
L0Q := Evaluate(map_0_coord_0,[SQ.i:i in [1..9]]);
L1Q := Evaluate(map_0_coord_1,[SQ.i:i in [1..9]]);
L2Q := Evaluate(map_0_coord_2,[SQ.i:i in [1..9]]);
P2Q<UQ,VQ,WQ> := ProjectiveSpace(Q,2);
X0Q := Curve(P2Q,Evaluate(
    map_0_codomain[1],[UQ,VQ,WQ] cat [Q!0:i in [4..9]]
));
assert Genus(X0Q) eq 3;
XtoX0Q := map<XQ->X0Q|[L0Q,L1Q,L2Q]>;

// The two rational cusps on X_0(43), certified as poles of the stored
// LMFDB j-map.  The numerator is nonzero and denominator zero at each.
load "references/x043_jmap_polynomials.m";
X0_cusp_split := X0Q![0,0,1];
X0_cusp_degree3 := X0Q![0,1,0];
for P in [X0_cusp_split,X0_cusp_degree3] do
    coords := Eltseq(P) cat [Q!0:i in [4..9]];
    assert Evaluate(j_denominator,coords) eq 0;
    assert Evaluate(j_numerator,coords) ne 0;
end for;

// Recover the three rational branches on the singular plane model of X.
P2plane<AQ,BQ,CQ> := ProjectiveSpace(Q,2);
CplaneQ := Curve(P2plane,Evaluate(
    model_1[1],[AQ,BQ,CQ] cat [Q!0:i in [4..9]]
));
projectionQ := map<XQ->CplaneQ|[SQ.7,SQ.8,SQ.9]>;
cusp_plane_points_Q := [
    CplaneQ![0,0,1], CplaneQ![0,1,0], CplaneQ![1,0,0]
];
assert [#Places(P):P in cusp_plane_points_Q] eq [1,1,1];
cuspsQ := [
    FunctionFieldDivisor(Pullback(projectionQ,Places(P)[1]))
    : P in cusp_plane_points_Q
];
assert [Degree(D):D in cuspsQ] eq [1,1,1];

split_fiber_Q := FunctionFieldDivisor(
    Pullback(XtoX0Q,Place(X0_cusp_split))
);
degree3_cusp_Q := FunctionFieldDivisor(
    Pullback(XtoX0Q,Place(X0_cusp_degree3))
);
assert split_fiber_Q eq &+cuspsQ;
assert Degree(degree3_cusp_Q) eq 3;
printf "CHECK|Q_CUSPS_IDENTIFIED_VIA_J_POLES=true\n";
printf "CHECK|Q_X0_CUSP_FIBERS=1+1+1_AND_3\n";

// Explicit degree-6 quotient X -> E = 43a1.
XfixQ := L0Q;
DfixQ := L1Q-L2Q;
AantiQ := L1Q+L2Q;
A2Q := XfixQ^2-Q!1/2*XfixQ*DfixQ+Q!1/8*DfixQ^2;
WquotQ := Q!1/8*AantiQ^2+A2Q;
EQ := EllipticCurve([Q|0,Q!1/4,0,0,Q!1/256]);
XtoEQ := map<XQ->EQ|[
    Q!1/4*XfixQ*DfixQ,Q!1/4*WquotQ,-DfixQ^2
]>;
OQ := EQ!0;
GQ := EQ![0,-Q!1/16,1];
fiber_O_Q := FunctionFieldDivisor(Pullback(XtoEQ,Place(OQ)));
fiber_G_Q := FunctionFieldDivisor(Pullback(XtoEQ,Place(GQ)));
assert Degree(fiber_O_Q) eq 6;
assert Degree(fiber_G_Q) eq 6;
printf "CHECK|Q_ELLIPTIC_MAP_DEGREE=6\n";

// Good reduction and the same cusp splitting modulo 3.
k := GF(3);
P8k := ProjectiveSpace(k,8);
Sk := CoordinateRing(P8k);
X3 := Curve(P8k,[Evaluate(q,[Sk.i:i in [1..9]]):q in model_0]);
assert Genus(X3) eq 9;
printf "CHECK|F3_FUNCTION_FIELD_GENUS=9\n";

L03 := Evaluate(map_0_coord_0,[Sk.i:i in [1..9]]);
L13 := Evaluate(map_0_coord_1,[Sk.i:i in [1..9]]);
L23 := Evaluate(map_0_coord_2,[Sk.i:i in [1..9]]);
P23<U3,V3,W3> := ProjectiveSpace(k,2);
X03 := Curve(P23,Evaluate(
    map_0_codomain[1],[U3,V3,W3] cat [k!0:i in [4..9]]
));
XtoX03 := map<X3->X03|[L03,L13,L23]>;
P2plane3<A3,B3,C3coord> := ProjectiveSpace(k,2);
Cplane3 := Curve(P2plane3,Evaluate(
    model_1[1],[A3,B3,C3coord] cat [k!0:i in [4..9]]
));
projection3 := map<X3->Cplane3|[Sk.7,Sk.8,Sk.9]>;
cusp_plane_points_3 := [
    Cplane3![0,0,1], Cplane3![0,1,0], Cplane3![1,0,0]
];
assert [#Places(P):P in cusp_plane_points_3] eq [1,1,1];
cusps3 := [
    FunctionFieldDivisor(Pullback(projection3,Places(P)[1]))
    : P in cusp_plane_points_3
];
split_fiber_3 := FunctionFieldDivisor(
    Pullback(XtoX03,Place(X03![0,0,1]))
);
degree3_cusp_3 := FunctionFieldDivisor(
    Pullback(XtoX03,Place(X03![0,1,0]))
);
assert split_fiber_3 eq &+cusps3;
assert Degree(degree3_cusp_3) eq 3;
printf "CHECK|GOOD_REDUCTION_AT_3_AND_CUSP_SPECIALIZATION=true\n";

// Use the factors of J_H directly; do not rely on their order inside the
// much larger decomposition of J_1(43).
Jmod := JH(43,[2]);
assert Dimension(Jmod) eq 9;
factors := Decomposition(Jmod);
assert [Dimension(A):A in factors] eq [1,2,2,4];
assert [LRatio(A,1):A in factors] eq [
    Rationals()!0, Rationals()!2/7,
    Rationals()!3/16, Rationals()!1/361
];
Amod := factors[1];
Bmod, quotient_map := Jmod/Amod;
assert Dimension(Bmod) eq 8;
assert TorsionMultiple(Bmod,100) eq 532;
printf "CHECK|JH_FACTOR_DIMENSIONS=1,2,2,4\n";
printf "CHECK|COMPLEMENT_LRATIOS=2/7,3/16,1/361\n";
printf "CHECK|COMPLEMENT_TORSION_MULTIPLE=532\n";

exit;
