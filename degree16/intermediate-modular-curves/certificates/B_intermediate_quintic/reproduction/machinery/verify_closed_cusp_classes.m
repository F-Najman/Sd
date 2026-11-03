// Exhaustive rational class check after a separate torsion-completeness proof.
load "canonical_input.m";
load "closed_cusp_ideals.m";
load "signed_cusp_candidates.m";
expected_classes := StringToInteger(expected_classes);
assert #signed_cusp_candidates eq expected_classes;
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
support := [Divisor(C,Scheme(C,eqs)):eqs in closed_cusp_equations];
assert [Degree(D):D in support] eq closed_cusp_degrees;
for i->v in signed_cusp_candidates do
    D := &+[v[j]*support[j]:j in [1..#support]];
    assert Degree(D) eq 5;
    V,to_function := RiemannRochSpace(D);
    printf "class=%o h0=%o\n",i,Dimension(V);
    if Dimension(V) lt 2 then continue; end if;
    assert Dimension(V) eq 2;
    basis := Basis(V);
    f := to_function(basis[2])/to_function(basis[1]);
    degree := Degree(Denominator(Divisor(f)));
    assert degree ge 1 and degree lt 5;
    printf "moving_degree=%o\n",degree;
end for;
printf "SUCCESS all %o rational classes have no degree-five pencil\n",#signed_cusp_candidates;
quit;
