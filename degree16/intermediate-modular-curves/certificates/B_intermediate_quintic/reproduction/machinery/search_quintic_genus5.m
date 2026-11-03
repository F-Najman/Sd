// A bounded characteristic-zero search. Success is an exact certificate;
// failure is NOT a proof of nonexistence. Run only on a verified rational model.
load "genus5_input.m";
C := Curve(ProjectiveSpace(Rationals(),5-1),equations);
assert IsNonsingular(C) and ArithmeticGenus(C) eq 5;
points := PointSearch(C,30);
printf "rational_points=%o\n",#points;
divisors := [Divisor(Place(P)):P in points];
tested := 0;
for choice in Multisets({1..#points},5) do
    D := &+[e*divisors[i]:i->e in choice];
    V,to_function := RiemannRochSpace(D);
    tested +:= 1;
    if Dimension(V) lt 2 then continue; end if;
    // Test each basis function: a degree-five witness is sufficient.
    // The finite search is not claimed to find every possible pencil.
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
printf "SEARCH FINISHED: %o divisors tested; no witness in this bounded search.\n",tested;
quit;
