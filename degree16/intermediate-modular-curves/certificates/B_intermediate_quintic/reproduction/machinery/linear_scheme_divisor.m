// Convert a zero-dimensional linear section using local place valuations.
// Avoids the generic ideal-divisor intrinsic's expensive ambiguous-patch search.
// The final degree equality certifies that the supplied places exhaust support.
function LinearSchemeDivisor(C,forms,places,coordinates)
    Z := Scheme(C,forms);
    assert Dimension(Z) le 0;
    degree := Degree(Z);
    D := 0*Divisor(places[1]);
    if degree eq 0 then return D; end if;
    F := FunctionField(C);
    RC := CoordinateRing(Ambient(C));
    for i->P in places do
        v := coordinates[i];
        if not &and[Evaluate(f,v) eq 0:f in forms] then continue; end if;
        pivot := Minimum([j:j in [1..#v]|v[j] ne 0]);
        functions := [F!(f/RC.pivot):f in forms];
        valuations := [Valuation(f,P):f in functions|f ne 0];
        assert #valuations gt 0;
        multiplicity := Minimum(valuations);
        assert multiplicity ge 1;
        D +:= multiplicity*Divisor(P);
    end for;
    assert Degree(D) eq degree;
    return D;
end function;
