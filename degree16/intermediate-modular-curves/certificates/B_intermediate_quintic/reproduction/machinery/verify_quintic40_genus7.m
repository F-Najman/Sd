// A fixed witness, not a search. Coordinates refer to the fresh q-basis.
load "canonical_input.m";
assert expected_genus eq 7;
C := Curve(ProjectiveSpace(Rationals(),6),equations);
points := [C!v:v in [[3,4,2,-1,1,2,1],[0,0,0,0,1,0,0],
                     [1,0,0,1,3,0,1],[3,4,2,3,1,2,1]]];
D := &+[Divisor(Place(points[i])):i in [1..3]]+2*Divisor(Place(points[4]));
assert Degree(D) eq 5;
V,to_function := RiemannRochSpace(D);
assert Dimension(V) ge 2;
found := false;
for v in Basis(V) do
    f := to_function(v);
    if f ne 0 and Degree(Denominator(Divisor(f))) eq 5 then
        found := true;
        print "CERTIFIED function",f;
        break;
    end if;
end for;
assert found;
print "SUCCESS fixed genus-seven degree-five witness";
quit;
