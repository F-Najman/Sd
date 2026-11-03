// Exact modular-symbol degree calculation, not ModularDegree(CrvEll), whose
// numerical implementation involves assumptions about the Manin constant.
N := StringToInteger(N);
assert N in {37,57};
J := JZero(N);
factors := Decomposition(J);
assert &+[Dimension(A):A in factors] eq Dimension(J);
degrees := [];
for A in factors do
    if Dimension(A) ne 1 then continue; end if;
    E := EllipticCurve(A);
    lo,hi := RankBounds(E);
    assert lo eq hi;
    if hi eq 0 then continue; end if;
    assert lo eq 1 and Conductor(E) eq N and RootNumber(E) eq -1;
    M := ModularSymbols(E);
    d := ModularDegree(M);
    Append(~degrees,d);
    printf "positive_factor=%o exact_optimal_modular_degree=%o\n",aInvariants(E),d;
end for;
assert #degrees eq 1;
t := N eq 37 select 6 else 2;
assert t*degrees[1] gt 7;
printf "CERTIFIED minimum_positive_elliptic_degree=%o\n",t*degrees[1];
print "SUCCESS small-density elliptic obstruction";
quit;
