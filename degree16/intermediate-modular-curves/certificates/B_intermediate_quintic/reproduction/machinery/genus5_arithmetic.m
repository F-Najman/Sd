// Exploratory exact arithmetic on a freshly verified model.
// No classification conclusion is inferred merely from these group orders.
load "genus5_input.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and ArithmeticGenus(C) eq 5;
points := PointSearch(C,30);
orders := [];
for p in [3,5,7,11,13] do
    Cp := ChangeRing(C,GF(p));
    if not IsNonsingular(Cp) then
        printf "p=%o displayed model singular; skipped\n",p;
        continue;
    end if;
    assert IsIrreducible(Cp) and IsReduced(Cp);
    F := AlgorithmicFunctionField(FunctionField(Cp));
    assert Genus(F) eq 5 and ArithmeticGenus(Cp) eq 5;
    G,representative,cl := ClassGroup(Cp);
    iv := Invariants(G);
    order := &*[a:a in iv|a ne 0];
    Append(~orders,order);
    reductions := [];
    for P in points do
        v := Eltseq(P);
        den := LCM([Denominator(a):a in v]);
        ints := [Integers()!(den*a):a in v];
        common := GCD(ints);
        Q := Cp![GF(p)!(a div common):a in ints];
        Append(~reductions,Divisor(Place(Q)));
    end for;
    H := sub<G|[cl(D-reductions[1]):D in reductions]>;
    printf "p=%o Jorder=%o rational_point_subgroup=%o group=%o\n",p,order,#H,iv;
end for;
printf "rational_torsion_order_bound=%o\n",GCD(orders);
print "SUCCESS arithmetic metadata only";
quit;
