// Positive-witness search only, on an independently verified canonical model.
// A finite failure does not establish nonexistence, even when J(Q) is finite.
load "canonical_input.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
assert IsNonsingular(C) and ArithmeticGenus(C) eq expected_genus;
points := PointSearch(C,20);
printf "rational_points=%o\n",#points;
divisors := [Divisor(Place(P)):P in points];
tested := 0;
for choice in Multisets({1..#points},5) do
    D := &+[e*divisors[i]:i->e in choice];
    V,to_function := RiemannRochSpace(D);
    tested +:= 1;
    if Dimension(V) lt 2 then continue; end if;
    for v in Basis(V) do
        f := to_function(v);
        if f ne 0 and Degree(Denominator(Divisor(f))) eq 5 then
            print "SUCCESS EXACT DEGREE FIVE";
            print "points",points;
            print "divisor multiset",choice;
            print "function",f;
            quit;
        end if;
    end for;
end for;
printf "SEARCH FINISHED: %o divisors tested; no bounded witness, not an exclusion.\n",tested;
quit;
