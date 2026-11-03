// Reproducible certificate that X = 43.132.9.a.2 has a Q-rational g^1_7.
//
// Let C1,C2,C3 be the rational cusps lying above [0:0:1], [0:1:0],
// [1:0:0] on the stored plane model.  Let F_P be the pullback of P under
// the degree-6 quotient X -> E, where
//
//   E: y^2 = x^3 + x^2/4 + 1/256,
//   O = 0_E,  G = (0,-1/16).
//
// This script verifies exactly that
//
//   D = 3*C3 + 7*C2 - 3*C1 + F_G - F_O
//
// has degree 7 and h^0(D)=2.  A ratio of two basis elements of L(D) is
// therefore a nonconstant function of degree at most 7.  Together with
// prove_lower_bound_7.m this proves that its degree is exactly 7.

None := 0;
load "lmfdb_43.132.9.a.2.m";

Q := Rationals();
P8 := ProjectiveSpace(Q,8);
S := CoordinateRing(P8);
X := Curve(P8,[
    Evaluate(q,[S.i:i in [1..9]]):q in model_0
]);

// Recover the three rational cusps in one algorithmic function field.
P2<Acoord,Bcoord,Ccoord> := ProjectiveSpace(Q,2);
Cplane := Curve(P2,Evaluate(
    model_1[1],[Acoord,Bcoord,Ccoord] cat [Q!0:i in [4..9]]
));
projection := map<X->Cplane|[S.7,S.8,S.9]>;
cusp_points := [
    Cplane![0,0,1],
    Cplane![0,1,0],
    Cplane![1,0,0]
];
cusps := [];
for i->P in cusp_points do
    T := Realtime();
    C := FunctionFieldDivisor(Pullback(projection,Places(P)[1]));
    assert Degree(C) eq 1;
    Append(~cusps,C);
    printf "RATIONAL_CUSP=%o|SECONDS=%.3o\n",i,Realtime(T);
end for;
C1,C2,C3 := Explode(cusps);

// Construct the degree-6 elliptic quotient from the stored map to X_0(43).
L0 := Evaluate(map_0_coord_0,[S.i:i in [1..9]]);
L1 := Evaluate(map_0_coord_1,[S.i:i in [1..9]]);
L2 := Evaluate(map_0_coord_2,[S.i:i in [1..9]]);
Xfix := L0;
Dfix := L1-L2;
Aanti := L1+L2;
A2 := Xfix^2-Q!1/2*Xfix*Dfix+Q!1/8*Dfix^2;
Wquot := Q!1/8*Aanti^2+A2;
E := EllipticCurve([Q|0,Q!1/4,0,0,Q!1/256]);
XtoE := map<X->E|[
    Q!1/4*Xfix*Dfix,Q!1/4*Wquot,-Dfix^2
]>;
O := E!0;
G := E![0,-Q!1/16,1];
T := Realtime();
FG := FunctionFieldDivisor(Pullback(XtoE,Place(G)));
FO := FunctionFieldDivisor(Pullback(XtoE,Place(O)));
assert Degree(FG) eq 6 and Degree(FO) eq 6;
printf "ELLIPTIC_FIBERS_SECONDS=%.3o\n",Realtime(T);

D := 3*C3+7*C2-3*C1+FG-FO;
assert Degree(D) eq 7;
T := Realtime();
h0 := Dimension(D);
assert h0 eq 2;
printf "CHECK|DIVISOR_DEGREE=7|H0=%o|RR_SECONDS=%.3o\n",
    h0,Realtime(T);

basis := Basis(D);
assert #basis eq 2;
f := basis[2]/basis[1];
// Calling Degree(f) triggers an unnecessary and very expensive
// factorization.  Since b1 and b2 are independent sections of the
// degree-7 line bundle O(D), their ratio defines the associated pencil
// after its common base divisor is removed, and therefore has degree at
// most 7.  Equivalently, E1=D+div(b1) is effective of degree 7 and
// div(b2/b1)+E1=D+div(b2) is effective.  Notice that D itself is not
// effective, so it would be incorrect to say that the poles are bounded
// directly by D.  The separately proved lower bound excludes degrees <=6.
printf "CHECK|BASIS_SIZE=2|RATIO_NONCONSTANT_BY_LINEAR_INDEPENDENCE=true\n";
printf "CONCLUSION|Q_GONALITY_UPPER_BOUND=7\n";
printf "CONCLUSION|WITH_LOWER_BOUND_Q_GONALITY=7\n";
exit;
