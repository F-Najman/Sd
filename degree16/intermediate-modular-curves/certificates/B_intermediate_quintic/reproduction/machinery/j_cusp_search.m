// Recover the complete cusp support as poles of the newly certified j-map.
load "canonical_input.m";
load "j_function.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
F := FunctionField(C);
RC := CoordinateRing(Ambient(C));
j := F!((RC!j_numerator)/(RC!j_denominator));
poles := Denominator(Divisor(j));
assert Degree(poles) eq expected_j_degree;
cusps := Support(poles);
printf "J_POLE_DEGREE=%o CLOSED_CUSP_DEGREES=%o\n",Degree(poles),Sort([Degree(P):P in cusps]);
if expected_genus in {5,7} then
    // K-E has degree five when deg(E)=2g-7.
    K := CanonicalDivisor(C);
    residual_degree := 2*expected_genus-7;
    places := [[P:P in cusps|Degree(P) eq d]:d in [1..residual_degree]];
    for partition in Partitions(residual_degree) do
        choices := CartesianProduct([Multisets({1..#places[d]},
            Multiplicity(Multiset(partition),d)):d in [1..residual_degree]]);
        for choice in choices do
            E := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
            D := K-E;
            V,to_function := RiemannRochSpace(D);
            if Dimension(V) lt 2 then continue; end if;
            basis := Basis(V);
            f := to_function(basis[2])/to_function(basis[1]);
            if Degree(Denominator(Divisor(f))) eq 5 then
                print "SUCCESS EXACT DEGREE FIVE complete-cusp residual";
                print "residual support",Decomposition(E);
                print "function",f;
                quit;
            end if;
        end for;
        printf "completed residual cusp-supported partition %o\n",partition;
    end for;
end if;
places := [[P:P in cusps|Degree(P) eq d]:d in [1..5]];
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        V,to_function := RiemannRochSpace(D);
        if Dimension(V) lt 2 then continue; end if;
        basis := Basis(V);
        for b in basis[2..#basis] do
            f := to_function(b)/to_function(basis[1]);
            if Degree(Denominator(Divisor(f))) eq 5 then
                print "SUCCESS EXACT DEGREE FIVE complete-cusp effective";
                print "pole support candidate",Decomposition(D);
                print "function",f;
                quit;
            end if;
        end for;
    end for;
    printf "completed cusp-supported partition %o\n",partition;
end for;
print "SUCCESS complete cusp support; bounded searches found no quintic witness";
quit;
