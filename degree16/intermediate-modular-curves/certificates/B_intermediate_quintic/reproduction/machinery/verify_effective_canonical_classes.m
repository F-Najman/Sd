// Riemann--Roch via canonical hyperplanes and exact fat-point ideals.
// No function-field presentation or global function divisor is required.
load "canonical_input.m";
load "short_signed_support.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
RC := CoordinateRing(Ambient(C));
g := expected_genus;
points := [C!v:v in support_points];
spaces := AssociativeArray();
for i->P in points do
    v := Eltseq(P);
    pivot := Minimum([j:j in [1..g]|v[j] ne 0]);
    point_ideal := ideal<RC|[RC.j-v[j]/v[pivot]*RC.pivot:j in [1..g]|j ne pivot]>;
    for m in [1..Maximum([D[i]:D in support_divisors])] do
        Z := Scheme(C,Basis(point_ideal^m));
        Saturate(~Z);
        assert Dimension(Z) eq 0 and Degree(Z) eq m;
        linear := [f:f in GroebnerBasis(Ideal(Z))|TotalDegree(f) eq 1];
        spaces[<i,m>] := sub<VectorSpace(Rationals(),g)|
            [Vector(Rationals(),[MonomialCoefficient(f,RC.j):j in [1..g]]):f in linear]>;
    end for;
end for;
function H0(multiplicities,spaces,g)
    W := VectorSpace(Rationals(),g);
    for i in [1..#multiplicities] do
        if multiplicities[i] gt 0 then
            W := W meet spaces[<i,multiplicities[i]>];
        end if;
    end for;
    // W is precisely H0(K-D) on the certified canonical model.
    return &+multiplicities+1-g+Dimension(W);
end function;
assert #support_divisors eq 12;
for i->v in support_divisors do
    assert &+v eq 5 and Min(v) ge 0;
    h0 := H0(v,spaces,g);
    printf "class=%o h0=%o\n",i,h0;
    if h0 lt 2 then continue; end if;
    assert h0 eq 2;
    fixed := false;
    for j in [1..#v] do
        if v[j] eq 0 then continue; end if;
        w := v;
        w[j] -:= 1;
        if H0(w,spaces,g) eq h0 then
            fixed := true;
            printf "rational base point=%o\n",j;
            break;
        end if;
    end for;
    assert fixed;
end for;
print "SUCCESS all 12 classes excluded by exact canonical fat-point conditions";
quit;
