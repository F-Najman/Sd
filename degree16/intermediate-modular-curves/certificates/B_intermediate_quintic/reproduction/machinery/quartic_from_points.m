// Verify supplied points and find inequivalent quartic divisor pencils.
load "canonical_input.m";
load "small_points.m";
C := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
points := [C!v:v in small_points];
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
    printf "quartic pencil %o multiplicities=%o\n",#pencils,witnesses[#witnesses];
end for;
PrintFile("small_quartic_witnesses.m",Sprintf("quartic_points := %o;",[Eltseq(P):P in points]):Overwrite:=true);
PrintFile("small_quartic_witnesses.m",Sprintf("quartic_multiplicities := %o;",witnesses));
printf "SUCCESS small-support quartic pencils=%o\n",#pencils;
quit;
