// Positive-only search on signed degree-five divisors selected by reduction.
load "canonical_input.m";
load "signed_support_candidates.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
points := [C!v:v in support_points];
places := [Divisor(Place(P)):P in points];
for i->multiplicities in support_divisors do
    D := &+[multiplicities[j]*places[j]:j in [1..#places]];
    assert Degree(D) eq 5;
    V,to_function := RiemannRochSpace(D);
    printf "signed candidate=%o h0=%o\n",i,Dimension(V);
    if Dimension(V) lt 2 then continue; end if;
    basis := Basis(V);
    for b in basis[2..#basis] do
        f := to_function(b)/to_function(basis[1]);
        d := Degree(Denominator(Divisor(f)));
        printf "moving degree=%o\n",d;
        if d eq 5 then
            print "SUCCESS EXACT DEGREE FIVE signed support";
            print "points",points;
            print "multiplicities",multiplicities;
            print "function",f;
            quit;
        end if;
    end for;
end for;
print "SEARCH FINISHED: signed support exhausted, not an exclusion";
quit;
