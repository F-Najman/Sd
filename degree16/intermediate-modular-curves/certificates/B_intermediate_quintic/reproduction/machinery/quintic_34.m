// New exact-degree-five certificate on the verified rational canonical model.
load "model_34.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and Degree(C) eq 8 and ArithmeticGenus(C) eq 5;
P := C![1,0,1,0,1];
Q := C![3,0,2,-1,2];
assert P ne Q;
D := 4*Divisor(Place(P))+Divisor(Place(Q));
V,to_function := RiemannRochSpace(D);
found := false;
for v in Basis(V) do
    f := to_function(v);
    if f eq 0 then continue; end if;
    poles := Denominator(Divisor(f));
    if Degree(poles) eq 5 then
        assert poles eq D;
        found := true;
        print "function",f;
        break;
    end if;
end for;
assert found;
print "SUCCESS quintic_34: rational function with exact pole divisor 4P+Q.";
quit;
