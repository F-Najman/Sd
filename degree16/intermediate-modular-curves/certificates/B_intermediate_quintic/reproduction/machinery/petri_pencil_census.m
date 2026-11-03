// Exhaustive finite-field W^1_5 census and Petri tangent dimensions.
// Exploratory metadata only: rational lifting is a separate proof obligation.
load "canonical_input.m";
p := StringToInteger(p);
k := GF(p);
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations),k);
assert Dimension(C) eq 1 and Degree(C) eq 2*expected_genus-2;
assert IsIrreducible(C) and IsReduced(C);
assert ArithmeticGenus(C) eq expected_genus;
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq expected_genus;
places := [Places(F,d):d in [1..5]];
assert #places[1] gt 0;
printf "good reduction p=%o g=%o place_counts=%o\n",p,expected_genus,[#s:s in places];
G,rep,cl := ClassGroup(F);
base := Divisor(places[1][1]);
classes := [[cl(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
seen := {G|};
K := CanonicalDivisor(F);
VK,to_K := RiemannRochSpace(K);
profile := AssociativeArray();
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        if c in seen then continue; end if;
        Include(~seen,c);
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        VD,to_D := RiemannRochSpace(D);
        h := Dimension(VD);
        if h lt 2 then continue; end if;
        Vres,to_res := RiemannRochSpace(K-D);
        rows := [Eltseq((to_D(a)*to_res(b))@@to_K):a in Basis(VD),b in Basis(Vres)];
        tangent := expected_genus-Rank(Matrix(k,#rows,expected_genus,&cat rows));
        moving := -1;
        if h eq 2 then
            basis := Basis(VD);
            f := to_D(basis[2])/to_D(basis[1]);
            moving := Degree(Denominator(Divisor(f)));
        end if;
        key := <h,moving,tangent>;
        if not IsDefined(profile,key) then profile[key] := 0; end if;
        profile[key] +:= 1;
    end for;
end for;
printf "W5_classes=%o\n",#seen;
for key in Sort(Setseq(Keys(profile))) do
    printf "PENCIL h0=%o moving_degree=%o petri_tangent_dimension=%o count=%o\n",
           key[1],key[2],key[3],profile[key];
end for;
print "SUCCESS exhaustive Petri-pencil metadata; no lifting assertion";
quit;
