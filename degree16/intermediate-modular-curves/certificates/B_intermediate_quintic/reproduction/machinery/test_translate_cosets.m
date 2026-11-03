// Exhaustive finite-field obstruction to abelian translates in W_5.
// Interpreting this as a Q-finiteness proof requires the separately audited
// factor profile and reduction argument. Nonempty cosets are inconclusive.
load "canonical_input.m";
p := StringToInteger(p);
ell := StringToInteger(ell);
// ell may be composite: we then test cyclic subgroups of that exact order.
// The application must justify that every possible elliptic direction has
// such a cyclic subgroup; group order alone does not imply this.
assert IsPrime(p) and ell gt 1 and GCD(p,ell) eq 1;
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations),GF(p));
assert IsIrreducible(C) and IsReduced(C);
assert ArithmeticGenus(C) eq expected_genus;
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq expected_genus;
places := [Places(F,d):d in [1..5]];
assert #places[1] gt 0;
G,representative,class_map := ClassGroup(F);
base := Divisor(places[1][1]);
classes := [[class_map(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
W := {G|};
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},
        Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        Include(~W,c);
    end for;
end for;
inv := Invariants(G);
T := sub<G|[(inv[i] div GCD(inv[i],ell))*G.i:i in [1..#inv]|inv[i] ne 0]>;
assert &and[ell*(G!t) eq G!0:t in Generators(T)];
subgroups := Setseq({sub<G|G!t>:t in T|Order(t) eq ell});
printf "p=%o ell=%o genus=%o place_counts=%o W5=%o group=%o tested_subgroups=%o\n",
    p,ell,expected_genus,[#s:s in places],#W,inv,#subgroups;
total := 0;
for H in subgroups do
    seen := {G|};
    count := 0;
    for c in W do
        if c in seen then continue; end if;
        coset := {c+G!h:h in H};
        seen join:= coset;
        if coset subset W then count +:= 1; end if;
    end for;
    printf "SUBGROUP generators=%o complete_cosets=%o\n",[G!h:h in Generators(H)],count;
    total +:= count;
end for;
printf "COMPLETE_COSETS_TOTAL=%o\n",total;
print "SUCCESS exhaustive translate-coset test";
quit;
