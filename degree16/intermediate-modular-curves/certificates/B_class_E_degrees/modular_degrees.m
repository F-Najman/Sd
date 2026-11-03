// Theorem B, class E (paper Table classE): elliptic curves of conductor N with odd analytic rank and their
// optimal modular degrees, from Cremona's database. Run: magma -b modular_degrees.m
D := CremonaDatabase();
for N in [37, 43, 53, 57, 58, 61, 65, 67, 73, 91, 121] do
    res := [];
    for i in [1..NumberOfIsogenyClasses(D, N)] do
        E := EllipticCurve(D, N, i, 1);
        r := AnalyticRank(E);
        if IsOdd(r) then Append(~res, <CremonaReference(E), r, ModularDegree(E)>); end if;
    end for;
    printf "N=%o odd-rank curves %o\n", N, res;
end for;
quit;
