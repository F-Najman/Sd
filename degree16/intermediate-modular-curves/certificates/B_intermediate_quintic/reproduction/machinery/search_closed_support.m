// Search rational divisors supported on closed points, not just Q-points.
// Hyperplane sections supply actual closed points over Q of several degrees.
// Finite failure remains inconclusive. Only exact pole-degree tests count.
load "canonical_input.m";
assert expected_genus eq 5;
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and ArithmeticGenus(C) eq 5;
forms := [R.i:i in [1..5]] cat [R.i+s*R.j:i,j in [1..5],s in [-1,1]|i lt j];
pool := {};
for h in forms do
    D := Divisor(C,Scheme(C,[h]));
    assert Degree(D) eq 8;
    for P in Support(D) do
        if Degree(P) le 5 then Include(~pool,P); end if;
    end for;
end for;
places := [[P:P in pool|Degree(P) eq d]:d in [1..5]];
print "CLOSED_SUPPORT_COUNTS",[#s:s in places];
K := CanonicalDivisor(C);
for target in [3,5] do
    for partition in Partitions(target) do
        choices := CartesianProduct([Multisets({1..#places[d]},
            Multiplicity(Multiset(partition),d)):d in [1..5]]);
        for choice in choices do
            E := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
            assert Degree(E) eq target;
            D := target eq 3 select K-E else E;
            assert Degree(D) eq 5;
            V,to_function := RiemannRochSpace(D);
            if Dimension(V) lt 2 then continue; end if;
            sections := [to_function(v):v in Basis(V)];
            for j in [2..#sections] do
                f := sections[j]/sections[1];
                if Degree(Denominator(Divisor(f))) eq 5 then
                    print "SUCCESS EXACT DEGREE FIVE from closed support";
                    print "support_divisor",E;
                    print "support_decomposition",Decomposition(E);
                    print "canonical_residual",target eq 3;
                    print "function",f;
                    quit;
                end if;
            end for;
        end for;
    end for;
end for;
print "SEARCH FINISHED: no closed-support witness, not an exclusion.";
quit;
