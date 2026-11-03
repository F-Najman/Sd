// Search degree-five pencils as canonical residuals of rational degree-three
// divisors. A genus-five curve has deg K=8, so K-E has degree five.
load "genus5_input.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and ArithmeticGenus(C) eq 5;
points := PointSearch(C,30);
divisors := [Divisor(Place(P)):P in points];
K := CanonicalDivisor(C);
for choice in Multisets({1..#points},3) do
    E := &+[e*divisors[i]:i->e in choice];
    D := K-E;
    V,to_function := RiemannRochSpace(D);
    if Dimension(V) lt 2 then continue; end if;
    sections := [to_function(v):v in Basis(V)];
    for i in [2..#sections] do
        f := sections[i]/sections[1];
        if Degree(Denominator(Divisor(f))) eq 5 then
            print "SUCCESS EXACT DEGREE FIVE via canonical residual";
            print "points",points;
            print "degree_three_multiset",choice;
            print "function",f;
            quit;
        end if;
    end for;
end for;
print "SEARCH FINISHED: no residual witness; not an exclusion.";
quit;
