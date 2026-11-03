// Class-group sieve for degree-five pencils whose classes lift from rational
// point differences. This is a positive-search aid, not a torsion-completeness
// claim. Signed divisors are essential: effective cusp-only searches miss them.
load "canonical_input.m";
load "small_points.m";
p := StringToInteger(p);
k := GF(p);
g := expected_genus;
CQ := Curve(ProjectiveSpace(Rationals(),g-1),equations);
qpoints := [CQ!v:v in small_points];
C := ChangeRing(CQ,k);
assert IsIrreducible(C) and IsReduced(C) and ArithmeticGenus(C) eq g;
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq g and Degree(C) eq 2*g-2;
points := [];
for P in qpoints do
    v := Eltseq(P);
    denominator := LCM([Denominator(c):c in v]);
    iv := [Integers()!(denominator*c):c in v];
    common := GCD(iv);
    Append(~points,C![k!(c div common):c in iv]);
end for;
G,rep,cl := ClassGroup(C);
base := Divisor(Place(points[1]));
generators := [cl(Divisor(Place(P))-base):P in points];
S := sub<G|generators>;
printf "rational_support_points=%o subgroup_order=%o ambient_invariants=%o\n",#points,#S,Invariants(G);
free := FreeAbelianGroup(#points);
lift := hom<free->G|generators>;
places := [Places(C,d):d in [1..5]];
classes := [[cl(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
seen := {G|};
special := 0;
survivors := [];
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        if c in seen then continue; end if;
        Include(~seen,c);
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        if Dimension(D) lt 2 then continue; end if;
        special +:= 1;
        if c notin S then continue; end if;
        v := Eltseq(c@@lift);
        assert lift(free!v) eq c;
        // Sum v_i(P_i-P_1)+5P_1 has degree five over Q and reduction c.
        v[1] +:= 5-&+v;
        assert &+v eq 5;
        Append(~survivors,v);
    end for;
end for;
PrintFile("signed_support_candidates.m",Sprintf("support_points := %o;",[Eltseq(P):P in qpoints]):Overwrite:=true);
PrintFile("signed_support_candidates.m",Sprintf("support_divisors := %o;",survivors));
printf "special_classes=%o rational_support_survivors=%o\n",special,#survivors;
print "SUCCESS rational-support class sieve; no completeness claim";
quit;
