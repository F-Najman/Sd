// Verify explicit Q quartic pencils cover every possible quintic pencil
// in a good reduction, with smooth one-dimensional Petri tangent spaces.
// The formal lifting lemma is an additional mathematical part of the proof.
load "canonical_input.m";
load "quartic_witnesses.m";
p := StringToInteger(p);
assert IsPrime(p);
g := expected_genus;
CQ := Curve(ProjectiveSpace(Rationals(),g-1),equations);
qpoints := [CQ!v:v in quartic_points];
assert #quartic_multiplicities gt 0;
for multiplicities in quartic_multiplicities do
    D := &+[multiplicities[i]*Divisor(Place(qpoints[i])):i in [1..#qpoints]];
    assert Degree(D) eq 4;
    V,to_function := RiemannRochSpace(D);
    assert Dimension(V) eq 2;
    basis := Basis(V);
    f := to_function(basis[2])/to_function(basis[1]);
    assert Degree(Denominator(Divisor(f))) eq 4;
end for;
print "exact Q quartic pencils verified";
k := GF(p);
C := ChangeRing(CQ,k);
assert Dimension(C) eq 1 and Degree(C) eq 2*g-2;
assert ArithmeticGenus(C) eq g and IsIrreducible(C) and IsReduced(C);
assert Genus(AlgorithmicFunctionField(FunctionField(C))) eq g;
reduced_points := [];
for P in qpoints do
    coords := Eltseq(P);
    denominator := LCM([Denominator(c):c in coords]);
    integer_coords := [Integers()!(denominator*c):c in coords];
    common := GCD(integer_coords);
    Append(~reduced_points,C![k!(c div common):c in integer_coords]);
end for;
places := [Places(C,d):d in [1..5]];
assert #places[1] gt 0;
base := Divisor(places[1][1]);
G,rep,cl := ClassGroup(C);
quartic_classes := {G|};
for multiplicities in quartic_multiplicities do
    D := &+[multiplicities[i]*Divisor(Place(reduced_points[i])):i in [1..#qpoints]];
    V,to_function := RiemannRochSpace(D);
    assert Dimension(V) eq 2;
    basis := Basis(V);
    f := to_function(basis[2])/to_function(basis[1]);
    assert Degree(Denominator(Divisor(f))) eq 4;
    Include(~quartic_classes,cl(D-4*base));
end for;
known := {a+cl(Divisor(P)-base):a in quartic_classes,P in places[1]};
K := CanonicalDivisor(C);
VK,to_K := RiemannRochSpace(K);
classes := [[cl(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
seen := {G|};
special := {G|};
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        if c in seen then continue; end if;
        Include(~seen,c);
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        VD,to_D := RiemannRochSpace(D);
        if Dimension(VD) lt 2 then continue; end if;
        assert Dimension(VD) eq 2;
        Include(~special,c);
        assert c in known;
        Vres,to_res := RiemannRochSpace(K-D);
        rows := [Eltseq((to_D(a)*to_res(b))@@to_K):a in Basis(VD),b in Basis(Vres)];
        assert g-Rank(Matrix(k,#rows,g,&cat rows)) eq 1;
    end for;
end for;
assert special eq known;
printf "quartic_reduction_classes=%o rational_reduction_points=%o quintic_pencil_classes=%o\n",
       #quartic_classes,#places[1],#special;
print "SUCCESS complete Petri lifting checks: only known basepointed pencils";
quit;
