// Expand the black-box TorsionMultiple(B,100)=532 computation into the
// individual good-prime point counts whose gcd gives the bound.

Jmod := JH(43,[2]);
factors := Decomposition(Jmod);
Amod := [A : A in factors | Dimension(A) eq 1][1];
Bmod, quotient_map := Jmod/Amod;

primes := [p : p in PrimesUpTo(100) | p gt 2 and p ne 43];
counts := [];
running_gcds := [];
g := 0;
for p in primes do
    fp := FrobeniusPolynomial(Bmod,p);
    n := Integers()!Evaluate(fp,1);
    Append(~counts,n);
    g := GCD(g,n);
    Append(~running_gcds,g);
    printf "PRIME=%o|POINTS=%o|RUNNING_GCD=%o\n",p,n,g;
end for;

assert g eq 532;
assert g eq TorsionMultiple(Bmod,100);
printf "CHECK|TORSION_POINT_COUNT_GCD=%o\n",g;
exit;
