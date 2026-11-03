// Export homogeneous prime ideals of ALL closed cusps from the exact j-map.
// No arithmetic completeness assertion is inferred from a point search.
load "canonical_input.m";
load "j_function.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
F := FunctionField(C);
RC := CoordinateRing(Ambient(C));
j := F!((RC!j_numerator)/(RC!j_denominator));
poles := Denominator(Divisor(j));
assert Degree(poles) eq expected_j_degree;
cusps := Support(poles);
PrintFile("closed_cusp_ideals.m","closed_cusp_equations := [* *];":Overwrite:=true);
degrees := [];
for P in cusps do
    I := Ideal(P);
    assert Degree(Scheme(Ambient(C),I)) eq Degree(P);
    // Serialize explicitly, avoiding printer-dependent variable names.
    expressions := [];
    for f in Basis(I) do
        terms := [];
        for m in Monomials(f) do
            term := "(" cat Sprint(MonomialCoefficient(f,m)) cat ")";
            exponents := Exponents(m);
            for i in [1..#exponents] do
                if exponents[i] ne 0 then
                    term cat:= Sprintf("*R.%o^%o",i,exponents[i]);
                end if;
            end for;
            Append(~terms,term);
        end for;
        Append(~expressions,Join(terms,"+"));
    end for;
    text := "[R|" cat Join(expressions,",") cat "]";
    PrintFile("closed_cusp_ideals.m","Append(~closed_cusp_equations," cat text cat ");");
    Append(~degrees,Degree(P));
    printf "exported closed cusp %o degree=%o\n",#degrees,Degree(P);
end for;
PrintFile("closed_cusp_ideals.m",Sprintf("closed_cusp_degrees := %o;",degrees));
print "SUCCESS all closed cusp ideals exported";
quit;
