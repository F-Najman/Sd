// Phase 1 of CurveArith's gonality test (Derickx-Terao), unchanged: the places of degree at most
// d - n1 and the expansions of the holomorphic differentials there, computed by CurveArith's own
// functions with CurveArith's own precisions. Only the output is new: the expansions are written to
// a file for the Phase 2 search.
//
// The caller (run_phase1.py writes a small driver) declares A<x,y> := PolynomialRing(Rationals(), 2),
// loads a plane model "X := ...;" over Q (Sutherland-van Hoeij), and assigns p, d, Out, Shard,
// Shards. The places are split round-robin between shards; every shard computes the same place
// lists, so the indices agree.
SetQuitOnError(true); SetColumns(0);
if assigned MemGB then SetMemoryLimit(MemGB * 2^30); end if;    // hard cap per process (bytes)
AttachSpec("../../../third_party/CurveArith/CurveArith.spec");
import "../../../third_party/CurveArith/src/gonality.m" : PrecomputePowerseriesExpansions;
t0 := Realtime();
// The plane model reduced mod p; F_p(x)[y]/(X).
R<t> := FunctionField(GF(p)); S<Y> := PolynomialRing(R);
den := LCM([Denominator(c) : c in Coefficients(X)]);
Xp := Evaluate(ChangeRing(den * X, GF(p)), [t, Y]);
assert IsIrreducible(Xp);
FF := FunctionField(Xp);

// From here on, exactly CurveArith's CAHasFunctionOfDegreeAtMost(FF, d : Al := "LinAlg") up to the
// search (third_party/CurveArith/src/gonality.m, lines 189-249).
FF := RationalExtensionRepresentation(FF);
assert DimensionOfExactConstantField(FF) eq 1;
g := Genus(FF);
q := #ConstantField(FF);
P1 := Places(FF, 1);
n := Ceiling(#P1 / (q + 1));
assert d lt g and n le d;
n1 := Min(n, d - 1);
places := [Places(FF, i) : i in [1..(d - n1)]];
precisions := [i eq 1 select d else (d - n1) div i : i in [1..d - n1]];
printf "PHASE1_PLACES g=%o q=%o rational=%o n=%o counts=%o seconds=%o\n", g, q, #P1, n, [#x : x in places], Realtime(t0);

// This shard's places. A place is assigned to shard ShardOf(key), where key encodes the irreducible
// polynomial g(t) in F_p[t] below the place (0 for places at infinity). The key does not depend on the order
// in which Magma lists the places, so the shards are disjoint and together contain every place of degree
// at most d - n1, whatever that order is in each process.
function Key(P)
    if not IsFinite(P) then return 0; end if;
    g := Minimum(Ideal(P));
    return &+[Integers() | (Integers() ! c) * p^(k - 1) : k -> c in Eltseq(g)];
end function;
// Fibonacci hashing spreads the keys evenly over the shards (the keys themselves are biased modulo small numbers).
ShardOf := func< k | ((k * 2654435761) mod 2^32) * Shards div 2^32 >;
mine := [[j : j in [1..#places[i]] | ShardOf(Key(places[i][j])) eq Shard] : i in [1..#places]];
expansions := PrecomputePowerseriesExpansions(FF, [[places[i][j] : j in mine[i]] : i in [1..#places]], precisions);
printf "PHASE1_EXPANSIONS shard=%o/%o places=%o seconds=%o\n", Shard, Shards, [#m : m in mine], Realtime(t0);

// Independent spot checks: Riemann-Roch dimensions of a few divisors supported on this shard's places,
// computed with Magma's Dimension (not with CurveArith); Phase 2 verifies them against the rank formula.
SetSeed(20261005 + Shard);
own := [<i, jj> : jj in [1..#mine[i]], i in [1..#places]];
checks := [];
for trial in [1..4] do
    if #own eq 0 then break; end if;
    ids := Sort(Setseq({Random(1, #own) : k in [1..Min(3, #own)]}));
    ms := [Random(1, Min(2, precisions[own[k][1]])) : k in ids];
    D := &+[ms[r] * Divisor(places[own[k][1]][mine[own[k][1]][own[k][2]]]) : r -> k in ids];
    Append(~checks, Sprintf("CHECK %o %o ", #ids, Dimension(D)) cat Join([Sprintf("%o %o %o", own[k][1], own[k][2], ms[r]) : r -> k in ids], " "));
end for;

// Output: one block per place, the matrix Transpose(HorizontalJoin(expansions)) of size (m*deg) x g, entries
// as integers 0..p-1, indexed by (degree, index among this shard's places of that degree).
basis := BasisOfHolomorphicDifferentials(FF);
lines := [Sprintf("PHASE1 %o %o %o %o %o %o %o", p, g, d, #P1, n, d - n1, Shards),
          "COUNTS " cat Join([IntegerToString(#x) : x in places], " "),
          "BASIS " cat Sprint(Hash(Sprint([Eltseq(RationalFunction(w / basis[1])) : w in basis])))];
for i in [1..#places] do
    for jj -> j in mine[i] do
        B := Transpose(HorizontalJoin(expansions[i][jj]));
        Append(~lines, Sprintf("PLACE %o %o %o %o", i, jj, precisions[i], Key(places[i][j])));
        for r in Rows(B) do Append(~lines, Join([IntegerToString(Integers() ! c) : c in Eltseq(r)], " ")); end for;
    end for;
end for;
lines cat:= checks;
Append(~lines, "END");
Write(Out, Join(lines, "\n") : Overwrite := true);
printf "PHASE1_DONE shard=%o/%o seconds=%o\n", Shard, Shards, Realtime(t0);
quit;
