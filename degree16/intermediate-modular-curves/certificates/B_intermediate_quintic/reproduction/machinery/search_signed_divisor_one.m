// One independently checkable rational divisor class; suitable for parallelism.
load "canonical_input.m";
load "signed_support_candidates.m";
i := StringToInteger(candidate);
assert i ge 1 and i le #support_divisors;
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
points := [C!v:v in support_points];
places := [Divisor(Place(P)):P in points];
v := support_divisors[i];
D := &+[v[j]*places[j]:j in [1..#places]];
assert Degree(D) eq 5;
V,to_function := RiemannRochSpace(D);
printf "signed candidate=%o h0=%o\n",i,Dimension(V);
if Dimension(V) ge 2 then
    basis := Basis(V);
    assert Dimension(V) eq 2; // Otherwise do not certify a unique moving degree.
    f := to_function(basis[2])/to_function(basis[1]);
    d := Degree(Denominator(Divisor(f)));
    printf "moving degree=%o\n",d;
    if d eq 5 then
        print "SUCCESS EXACT DEGREE FIVE signed support";
        print "points",points;
        print "multiplicities",v;
        print "function",f;
    end if;
end if;
printf "SUCCESS exact rational class check candidate=%o\n",i;
quit;
