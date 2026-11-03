// Reproducible certificate that X = 43.132.9.a.2 has no Q-rational g^1_6.
//
// The earlier certificate had a saturation gap.  It is closed here using
// the quotient B = Jac(X)/43A.  Magma constructs a modular abelian variety
// Bmod that is Q-isogenous to B and certifies a rational-torsion multiple
// 532 for Bmod.  Point counts, hence this torsion bound, are invariant
// within the Q-isogeny class.  Kato's theorem gives rank B(Q)=0, while a
// rational cuspidal subgroup of order at least 532 maps injectively to B.
// Hence Jac(X)(Q) = 43A(Q) + C_cusp, exactly.

None := 0;
load "lmfdb_43.132.9.a.2.m";
AttachSpec("../../third_party/CurveArith/CurveArith.spec");

// ---------- The unique degree-6 class in characteristic 3 ----------
k := GF(3);
C3 := Curve(Reduction(Curve(ProjectiveSpace(Pol), model_0), 3));
assert Genus(C3) eq 9;
assert CAGonality(C3) eq 6;
FF := AlgorithmicFunctionField(FunctionField(C3));
J3, _, class_map := ClassGroup(FF);
target := J3![1,1,1977,0];

degree := 6;
rational_places := Places(FF,1);
n := Ceiling(#rational_places/(#k+1));
assert n eq 1;
places := [Places(FF,i):i in [1..degree-n]] cat [[]:i in [1..n]];
counts := [#P:P in places];
base := degree*Divisor(rational_places[1]);
classes := {@ @};
successes := 0;
for partition in RestrictedPartitions(degree-n,{1..degree-n}) do
    multiplicities := [
        Multiplicity(Multiset(partition),i):i in [1..degree]
    ];
    multiplicities[1] +:= n;
    products := CartesianProduct([
        Multisets({1..counts[i]},multiplicities[i]):i in [1..degree]
    ]);
    for candidate in products do
        D := &+[
            multiplicity*Divisor(places[place_degree][place_index])
            : place_index -> multiplicity in multiset,
              place_degree -> multiset in candidate
        ];
        if Dimension(D) ge 2 then
            successes +:= 1;
            Include(~classes,class_map(D-base));
        end if;
    end for;
end for;
assert successes eq 4;
assert #classes eq 1;
assert classes[1] eq target;
assert Order(target) eq 1596;
pic_invariants := Invariants(J3);
J3_order := &*[n : n in pic_invariants | n ne 0];
printf "CHECK|F3_GONALITY=6|UNIQUE_G1_6_CLASS=%o\n",Eltseq(target);
printf "CHECK|F3_PICARD_INVARIANTS=%o|JACOBIAN_ORDER=%o\n",
    pic_invariants,J3_order;

// ---------- Elliptic and rational cuspidal reduction subgroup ----------
P8 := Ambient(C3);
S := CoordinateRing(P8);
X := C3;
L0 := Evaluate(map_0_coord_0,[S.i:i in [1..9]]);
L1 := Evaluate(map_0_coord_1,[S.i:i in [1..9]]);
L2 := Evaluate(map_0_coord_2,[S.i:i in [1..9]]);
Xfix := L0;
Dfix := L1-L2;
Aanti := L1+L2;
A4 := k!1/16;
A2 := Xfix^2-k!1/2*Xfix*Dfix+k!1/8*Dfix^2;
Wquot := 2*A4*Aanti^2+A2;
E3 := EllipticCurve([k|0,k!1/4,0,0,k!1/256]);
assert #Points(E3) eq 6;
XtoE3 := map<X->E3|[
    k!1/4*Xfix*Dfix,k!1/4*Wquot,-Dfix^2
]>;

elliptic_generators := [];
fiber_O := FunctionFieldDivisor(Pullback(XtoE3,Place(E3!0)));
assert Degree(fiber_O) eq 6;
for P in Points(E3) do
    fiber := FunctionFieldDivisor(Pullback(XtoE3,Place(P)));
    assert Degree(fiber) eq 6;
    Append(~elliptic_generators,class_map(fiber-fiber_O));
end for;

P2<A,B,C> := ProjectiveSpace(k,2);
Cplane := Curve(P2,Evaluate(
    model_1[1],[A,B,C] cat [k!0:i in [4..9]]
));
projection := map<X->Cplane|[S.7,S.8,S.9]>;
cusps := [];
for P in [Cplane![0,0,1],Cplane![0,1,0],Cplane![1,0,0]] do
    Append(~cusps,FunctionFieldDivisor(
        Pullback(projection,Places(P)[1])
    ));
end for;
// The Pic^6 origin used in the exhaustive search is the reduction of
// the third Q-rational cusp, so there is no unaccounted affine translate.
assert class_map(cusps[3]-Divisor(rational_places[1])) eq J3!0;
cusp_generators := [
    class_map(cusps[2]-cusps[1]),
    class_map(cusps[3]-cusps[1])
];
P20<U,V,W> := ProjectiveSpace(k,2);
C0 := Curve(P20,Evaluate(
    map_0_codomain[1],[U,V,W] cat [k!0:i in [4..9]]
));
XtoC0 := map<X->C0|[L0,L1,L2]>;
degree3_cusp := FunctionFieldDivisor(
    Pullback(XtoC0,Place(C0![0,1,0]))
);
Append(~cusp_generators,class_map(degree3_cusp-3*cusps[3]));

Cusp3 := sub<J3|cusp_generators>;
H3 := sub<J3|elliptic_generators cat cusp_generators>;
assert #Cusp3 eq 532;
assert not target in H3;
printf "CHECK|CUSPIDAL_REDUCTION_ORDER=532\n";
printf "CHECK|ELLIPTIC_REDUCTION_ORDER=6\n";
printf "CHECK|ELLIPTIC_PLUS_CUSPIDAL_ORDER=%o\n",#H3;
printf "CHECK|TARGET_OUTSIDE_ELLIPTIC_PLUS_CUSPIDAL=true\n";

// ---------- Close the saturation gap over Q ----------
//
// The modular Jacobian is J_H(43) for H=<2> in (Z/43Z)^*.  Magma's JH
// object is Q-isogenous, not canonically isomorphic, to Jac(X).  This is
// enough here: its unique dimension-1 isogeny factor is 43a and its
// complementary quotient is Q-isogenous to B=Jac(X)/A.
Jmod := JH(43,[2]);
assert Dimension(Jmod) eq 9;
// This point-count comparison is a strong independent compatibility
// check between the reduced LMFDB function field and the modular-symbols
// Jacobian.  It does not replace the standard good-reduction theorem.
expected_J3_order := Integers()!Evaluate(FrobeniusPolynomial(Jmod,3),1);
assert J3_order eq expected_J3_order;
printf "CHECK|F3_JACOBIAN_ORDER_MATCHES_MODULAR_SYMBOLS=%o\n",
    expected_J3_order;
factors := Decomposition(Jmod);
assert [Dimension(A):A in factors] eq [1,2,2,4];
Amod := [A:A in factors|Dimension(A) eq 1][1];
assert Conductor(Amod) eq 43;
Bmod, quotient_map := Jmod/Amod;
assert Dimension(Bmod) eq 8;
// Compute the L-ratios directly on these four factors.  The earlier
// version took the first four factors of the larger J_1(43)
// decomposition; that happened to give the same zero/nonzero pattern,
// but did not itself verify that the selected factors belonged to J_H.
// By Kato, the three nonzero complementary factors have rank zero.
assert [LRatio(factors[i],1):i in [1..4]] eq [
    Rationals()!0, Rationals()!2/7,
    Rationals()!3/16, Rationals()!1/361
];
upper_B := TorsionMultiple(Bmod,100);
assert upper_B eq 532;

// The elliptic factor is E: y^2+y=x^3+x^2 and has E(Q)=Z, so no torsion.
EQ := EllipticCurve([Rationals()|0,1,1,0,0]);
MW, MWtoE := MordellWeilGroup(EQ);
assert Invariants(MW) eq [0];
Etors, Etors_to_E := TorsionSubgroup(EQ);
assert #Etors eq 1;
has_cm, cm_disc := HasComplexMultiplication(EQ);
assert not has_cm;
isogenous_curves, max_cyclic_degree := IsogenousCurves(EQ);
assert #isogenous_curves eq 1;
assert max_cyclic_degree eq 1;

// The three rational cuspidal divisor classes above are Q-rational and
// torsion (Manin--Drinfeld).  Their reduction has order 532, so their
// Q-subgroup has order at least 532.  Let A=f^*E in the actual Jac(X) and
// B=Jac(X)/A.  The pullback is an embedding: otherwise f would factor
// through a nontrivial Q-rational isogeny E' -> E of degree dividing 6.
// The Q-isogeny class of 43a1 contains no other curve, and a nontrivial
// self-isogeny has square degree because End_Q(E)=Z; no such degree
// divides 6.  Thus A(Q) is torsion-free.
//
// The cuspidal subgroup meets A(Q) trivially and hence injects into the
// actual B(Q).  Since B is Q-isogenous to Bmod, it has the same good-prime
// point counts as Bmod, so TorsionMultiple(Bmod,100)=532 also bounds
// #B(Q)_tors.  Kato gives rank B(Q)=0.  The upper and lower bounds force
// #B(Q)=532 and the cuspidal subgroup maps onto it.  Therefore
//
//     Jac(X)(Q) = Amod(Q) + Cusp(Q),
//
// whose reduction is contained in H3.  Since target is not in H3, the
// unique F_3 degree-6 class cannot lift to Q.
printf "CHECK|COMPLEMENT_Q_POINT_UPPER_BOUND=%o\n",upper_B;
printf "CHECK|COMPLEMENTARY_LRATIOS_NONZERO=true\n";
printf "CHECK|ELLIPTIC_FACTOR_TORSION_FREE=true\n";
printf "CHECK|ELLIPTIC_ISOGENY_CLASS_SIZE=1\n";
printf "CHECK|ELLIPTIC_PULLBACK_PRIMITIVE=true\n";
printf "CONCLUSION|NO_Q_RATIONAL_G1_6=true\n";
printf "CONCLUSION|Q_GONALITY_LOWER_BOUND=7\n";
exit;
