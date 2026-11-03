// A local base-point certificate avoids factoring a global function divisor.
load "canonical_input.m";
load "signed_support_candidates.m";
i := StringToInteger(candidate);
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
points := [C!v:v in support_points];
assert #Seqset(points) eq #points;
places := [Place(P):P in points];
v := support_divisors[i];
D := &+[v[j]*Divisor(places[j]):j in [1..#places]];
assert Degree(D) eq 5;
V,to_function := RiemannRochSpace(D);
printf "candidate=%o h0=%o\n",i,Dimension(V);
if Dimension(V) lt 2 then
    printf "SUCCESS no degree-five pencil in class %o: h0 below two\n",i;
    quit;
end if;
assert Dimension(V) eq 2;
sections := [to_function(b):b in Basis(V)];
for j in [1..#places] do
    orders := [Valuation(f,places[j])+v[j]:f in sections];
    assert Min(orders) ge 0;
    printf "point=%o section_orders=%o\n",j,orders;
    if Min(orders) ge 1 then
        printf "SUCCESS no degree-five pencil in class %o: rational base point %o\n",i,j;
        quit;
    end if;
end for;
print "INCONCLUSIVE: no base point among supplied rational points";
quit;
