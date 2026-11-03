// Search degree-five effective divisors with non-rational closed support.
// The model must have passed the Hilbert identification gate. No failed
// search is a characteristic-zero nonexistence certificate.
load "canonical_input.m";
g := expected_genus;
C := Curve(ProjectiveSpace(Rationals(),g-1),equations);
forms := [R.i:i in [1..g]] cat [R.i+s*R.j:i,j in [1..g],s in [-1,1]|i lt j];
pool := {};
for j->h in forms do
    D := Divisor(C,Scheme(C,[h]));
    assert Degree(D) eq 2*g-2;
    for P in Support(D) do
        if Degree(P) le 5 then Include(~pool,P); end if;
    end for;
    printf "hyperplane=%o/%o closed_places=%o\n",j,#forms,#pool;
end for;
places := [[P:P in pool|Degree(P) eq d]:d in [1..5]];
print "CLOSED_SUPPORT_COUNTS",[#s:s in places];
tested := 0;
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        assert Degree(D) eq 5;
        V,to_function := RiemannRochSpace(D);
        tested +:= 1;
        if Dimension(V) lt 2 then continue; end if;
        sections := [to_function(v):v in Basis(V)];
        for j in [2..#sections] do
            f := sections[j]/sections[1];
            if Degree(Denominator(Divisor(f))) eq 5 then
                print "SUCCESS EXACT DEGREE FIVE mixed divisor";
                print "support_decomposition",Decomposition(D);
                print "function",f;
                quit;
            end if;
        end for;
    end for;
    printf "partition=%o tested=%o\n",partition,tested;
end for;
print "SEARCH FINISHED: no mixed-divisor witness, not an exclusion.";
quit;
