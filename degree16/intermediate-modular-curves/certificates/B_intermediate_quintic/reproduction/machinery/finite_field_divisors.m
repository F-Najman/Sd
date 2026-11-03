// Exhaustive effective-divisor census, not a characteristic-zero conclusion.
// Input: a verified rational canonical model; command-line p:=good_prime.
load "canonical_input.m";
p := StringToInteger(p);
assert IsPrime(p);
CQ := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
C := ChangeRing(CQ,GF(p));
assert Dimension(C) eq 1 and IsIrreducible(C) and IsReduced(C);
assert ArithmeticGenus(C) eq expected_genus;
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq expected_genus;
// Equality of arithmetic genus and normalization genus gives smoothness
// here; a degree-one place gives full constant field and geometric integrality.
places := [Places(F,d):d in [1..5]];
assert #places[1] gt 0;
printf "p=%o genus=%o place_counts=%o\n",p,Genus(F),[#s:s in places];
G,representative,class_map := ClassGroup(F);
base := Divisor(places[1][1]);
classes := [[class_map(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
// Each partition specifies the degrees of closed points in an effective
// divisor. Multisets allow repetitions and avoid counting a divisor twice.
counts := AssociativeArray();
representatives := AssociativeArray();
total := 0;
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        assert Degree(D) eq 5;
        if IsDefined(counts,c) then
            counts[c] +:= 1;
        else
            counts[c] := 1;
            representatives[c] := D;
        end if;
        total +:= 1;
    end for;
end for;
special := 0;
moving_degrees := AssociativeArray();
for c in Keys(counts) do
    h := Dimension(representatives[c]);
    // Independent check: a rational divisor class with h sections has
    // precisely #P^(h-1)(F_p) rational effective representatives.
    assert counts[c] eq (p^h-1) div (p-1);
    if h gt 1 then
        special +:= 1;
        if h eq 2 then
            V,to_function := RiemannRochSpace(representatives[c]);
            basis := Basis(V);
            f := to_function(basis[2])/to_function(basis[1]);
            degree := Degree(Denominator(Divisor(f)));
            assert 1 le degree and degree le 5;
            if not IsDefined(moving_degrees,degree) then moving_degrees[degree] := 0; end if;
            moving_degrees[degree] +:= 1;
        end if;
    end if;
end for;
printf "CLASS_CENSUS group=%o effective_divisors=%o W5_classes=%o W5_special=%o\n",
       Invariants(G),total,#Keys(counts),special;
print "PENCIL_MOVING_DEGREES",[<d,moving_degrees[d]>:d in Sort(Setseq(Keys(moving_degrees)))];
print "SUCCESS exhaustive finite-field degree-five divisor census";
print "No assertion about characteristic-zero degree-five functions is made.";
quit;
