// Exploratory cubic-class sieve against the Hecke exponent-four bound.
load "canonical_input.m";
assert expected_genus eq 5;
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),4),equations),GF(3));
assert IsIrreducible(C) and IsReduced(C) and ArithmeticGenus(C) eq 5;
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq 5;
places := [Places(F,d):d in [1..3]];
G,rep,cl := ClassGroup(F);
P := Divisor(places[1][1]);
K := CanonicalDivisor(F);
all := 0;
survivors := 0;
moving := [];
for partition in Partitions(3) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..3]]);
    for choice in choices do
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        assert Degree(D) eq 3 and Dimension(D) eq 1;
        all +:= 1;
        c := cl(D-3*P);
        if 4*c ne G!0 then continue; end if;
        survivors +:= 1;
        V,to_function := RiemannRochSpace(K-D);
        assert Dimension(V) eq 2;
        b := Basis(V);
        f := to_function(b[2])/to_function(b[1]);
        d := Degree(Denominator(Divisor(f)));
        Append(~moving,d);
    end for;
end for;
printf "cubic_divisors=%o exponent_four_survivors=%o moving_degrees=%o\n",all,survivors,moving;
print "SUCCESS cubic-class sieve metadata";
quit;
