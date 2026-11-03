// Verify the full special-fiber Hilbert polynomials, not just their genera.
load "family_input.m";
p := StringToInteger(p);
assert IsPrime(p) and N mod p ne 0 and p ne 2;
for pair in [* <source_equations,source_genus>,<target_equations,target_genus> *] do
    equations := pair[1];
    g := pair[2];
    C := ChangeRing(Curve(ProjectiveSpace(Rationals(),g-1),equations),GF(p));
    assert Dimension(C) eq 1 and Degree(C) eq 2*g-2;
    assert ArithmeticGenus(C) eq g;
    assert IsReduced(C) and IsIrreducible(C);
    assert Genus(AlgorithmicFunctionField(FunctionField(C))) eq g;
    assert #Places(C,1) gt 0;
    printf "good canonical reduction: genus=%o degree=%o prime=%o\n",g,Degree(C),p;
end for;
print "SUCCESS good family models with unchanged Hilbert polynomials";
quit;
