// Fresh positive certificate for Delta=<-1,2> at level 33.
// Modular identification: relations_33.json, geometry_33.log,
// and the rational-duality proof RATIONAL_MODELS.md.
load "model_33.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
assert IsNonsingular(C) and Degree(C) eq 8 and ArithmeticGenus(C) eq 5;
P := C![1,1,0,1,0];
Q := C![1,0,0,0,0];
assert P ne Q;
D := 4*Divisor(Place(P))+Divisor(Place(Q));
V,to_function := RiemannRochSpace(D);
assert Dimension(V) ge 2;
found := false;
for v in Basis(V) do
    f := to_function(v);
    if f eq 0 then continue; end if;
    poles := Denominator(Divisor(f));
    if Degree(poles) eq 5 then
        assert poles eq D;
        found := true;
        print "function", f;
        break;
    end if;
end for;
assert found;
print "SUCCESS quintic_33: rational function with exact pole divisor 4P+Q.";
quit;
