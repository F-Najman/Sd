// Positive quartic witnesses on a previously identified smooth Q-model.
// The output records divisors on rational points, not just numerical gonality.
load "canonical_input.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
points := PointSearch(C,20);
assert #points gt 0;
printf "rational points found=%o\n",#points;
divisors := [Divisor(Place(P)):P in points];
pencils := [];
witnesses := [];
for choice in Multisets({1..#points},4) do
    D := &+[e*divisors[i]:i->e in choice];
    V,to_function := RiemannRochSpace(D);
    if Dimension(V) ne 2 then continue; end if;
    basis := Basis(V);
    f := to_function(basis[2])/to_function(basis[1]);
    if Degree(Denominator(Divisor(f))) ne 4 then continue; end if;
    if &or[Dimension(D-E) eq 1:E in pencils] then continue; end if;
    Append(~pencils,D);
    Append(~witnesses,[Multiplicity(choice,i):i in [1..#points]]);
    printf "new quartic pencil %o support multiplicities=%o\n",#pencils,witnesses[#witnesses];
end for;
output := "quartic_witnesses.m";
PrintFile(output,Sprintf("quartic_points := %o;",[Eltseq(P):P in points]):Overwrite:=true);
PrintFile(output,Sprintf("quartic_multiplicities := %o;",witnesses));
printf "SUCCESS exact quartic pencils=%o\n",#pencils;
quit;
