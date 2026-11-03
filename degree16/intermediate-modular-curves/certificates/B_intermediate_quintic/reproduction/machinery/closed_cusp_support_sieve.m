// Exploratory class sieve using every closed cusp, including quadratic ones.
// Output consists only of candidate rational degree-five divisors. A negative
// result is not a certificate without a separate rational-torsion upper bound
// and exact rational Riemann--Roch checks on every surviving class.
load "canonical_input.m";
load "closed_cusp_ideals.m";
p := StringToInteger(p);
k := GF(p);
g := expected_genus;
CQ := Curve(ProjectiveSpace(Rationals(),g-1),equations);
C := ChangeRing(CQ,k);
assert IsIrreducible(C) and IsReduced(C) and ArithmeticGenus(C) eq g;
assert Genus(AlgorithmicFunctionField(FunctionField(C))) eq g;
Rk := CoordinateRing(Ambient(C));
support := [];
for i in [1..#closed_cusp_equations] do
    integral := [];
    for f in closed_cusp_equations[i] do
        denominator := LCM([Denominator(c):c in Coefficients(f)]);
        Append(~integral,Rk!(denominator*f));
    end for;
    Z := Scheme(C,integral);
    // The flat projective closure is contained in Z. Equal special and
    // generic lengths certify equality, provided the special scheme is finite.
    assert Dimension(Z) eq 0 and Degree(Z) eq closed_cusp_degrees[i];
    D := Divisor(C,Z);
    assert Degree(D) eq closed_cusp_degrees[i];
    Append(~support,D);
end for;
base_index := Index(closed_cusp_degrees,1);
assert base_index gt 0;
base := support[base_index];
G,rep,cl := ClassGroup(C);
generators := [cl(support[i]-closed_cusp_degrees[i]*base):i in [1..#support]];
S := sub<G|generators>;
printf "closed_cusp_support=%o subgroup_order=%o ambient_invariants=%o\n",#support,#S,Invariants(G);
free := FreeAbelianGroup(#support);
lift := hom<free->G|generators>;
places := [Places(C,d):d in [1..5]];
classes := [[cl(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
seen := {G|};
special := 0;
survivors := [];
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        if c in seen then continue; end if;
        Include(~seen,c);
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        if Dimension(D) lt 2 then continue; end if;
        special +:= 1;
        if c notin S then continue; end if;
        v := Eltseq(c@@lift);
        assert lift(free!v) eq c;
        v[base_index] +:= 5-&+[v[i]*closed_cusp_degrees[i]:i in [1..#v]];
        assert &+[v[i]*closed_cusp_degrees[i]:i in [1..#v]] eq 5;
        Append(~survivors,v);
    end for;
end for;
PrintFile("signed_cusp_candidates.m",Sprintf("signed_cusp_candidates := %o;",survivors):Overwrite:=true);
printf "special_classes=%o closed_cusp_survivors=%o\n",special,#survivors;
print "SUCCESS closed-cusp sieve; candidate generation only";
quit;
