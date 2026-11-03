// Exact positive-only search on closed-cusp divisor classes selected mod p.
load "canonical_input.m";
load "closed_cusp_ideals.m";
load "signed_cusp_candidates.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
support := [Divisor(C,Scheme(C,eqs)):eqs in closed_cusp_equations];
assert [Degree(D):D in support] eq closed_cusp_degrees;
for i->v in signed_cusp_candidates do
    D := &+[v[j]*support[j]:j in [1..#support]];
    assert Degree(D) eq 5;
    V,to_function := RiemannRochSpace(D);
    printf "signed closed-cusp candidate=%o h0=%o\n",i,Dimension(V);
    if Dimension(V) lt 2 then continue; end if;
    basis := Basis(V);
    for b in basis[2..#basis] do
        f := to_function(b)/to_function(basis[1]);
        d := Degree(Denominator(Divisor(f)));
        printf "moving degree=%o\n",d;
        if d eq 5 then
            print "SUCCESS EXACT DEGREE FIVE signed closed cusps";
            print "multiplicities",v;
            print "function",f;
            quit;
        end if;
    end for;
end for;
print "SEARCH FINISHED: candidate classes exhausted, not an exclusion";
quit;
