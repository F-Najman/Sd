// Shared exact operations. Run all entry-point scripts from this directory.
// No search bound is used: degree-five divisors are enumerated exhaustively.
SetColumns(160);
SetSeed(1);
load "coordinates.m";
load "place_cache.m";

function GoodModel(N, p, genus)
    C := ChangeRing(ModularCurveQuotient(N, []), GF(p));
    F := AlgorithmicFunctionField(FunctionField(C));
    assert N mod p ne 0;
    assert IsIrreducible(C) and IsReduced(C);
    assert ArithmeticGenus(C) eq genus and Genus(F) eq genus;
    assert #Places(F, 1) gt 0;
    // The integral special fiber has no normalization defect and has
    // full constant field F_p. It is smooth and geometrically integral.
    return C, F;
end function;

function PositiveFactors(N)
    factors := Factorization(JZero(N));
    // A Magma list, not a sequence: different modular factors can have
    // different parents. IsZeroAt at the central critical value is exact.
    positive := [* t : t in factors | IsZeroAt(LSeries(t[1]), 1) *];
    return factors, positive;
end function;

function PointCount(A, p)
    return Integers()!Evaluate(FrobeniusPolynomial(A, p), 1);
end function;

function TorsionKilledBy(G, n)
    invariants := Invariants(G);
    return sub<G | [
        (invariants[i] div GCD(invariants[i], n))*G.i
        : i in [1..#invariants] | invariants[i] ne 0
    ]>;
end function;

function PrimarySubgroup(G, ell)
    invariants := Invariants(G);
    return sub<G | [
        (invariants[i] div ell^Valuation(invariants[i], ell))*G.i
        : i in [1..#invariants] | invariants[i] ne 0
    ]>;
end function;

function DegreeFiveClasses(F, class_map, base : Sections := false)
    places := [Places(F, d) : d in [1..5]];
    printf "place_counts=%o\n", [#ps : ps in places];

    // Compute each place class once. Later use additivity of the class map.
    place_classes := [];
    for d in [1..5] do
        classes := [];
        for i -> P in places[d] do
            Append(~classes, class_map(Divisor(P)-d*base));
            if i mod 500 eq 0 then
                printf "degree=%o place_classes=%o/%o\n", d, i, #places[d];
            end if;
        end for;
        Append(~place_classes, classes);
    end for;

    W := {};
    W1 := {};
    representatives := AssociativeArray();
    total := 0;
    for partition in Partitions(5) do
        // For each degree d, choose the required multiset of degree-d
        // places. This visits each effective degree-five divisor once.
        choices := CartesianProduct([
            Multisets({1..#places[d]}, Multiplicity(Multiset(partition), d))
            : d in [1..5]
        ]);
        for choice in choices do
            D := &+[e*Divisor(places[d][i]) : i -> e in s, d -> s in choice];
            c := &+[e*place_classes[d][i] : i -> e in s, d -> s in choice];
            assert Degree(D) eq 5;
            Include(~W, c);
            representatives[c] := D;
            if Sections and Dimension(D) ge 2 then Include(~W1, c); end if;
            total +:= 1;
        end for;
        printf "partition=%o divisors=%o classes=%o\n", partition, total, #W;
    end for;
    return W, representatives, total, W1;
end function;

function WholeCosets(W, subgroup, G)
    elements := [G!s : s in subgroup];
    seen := {};
    cosets := [];
    for c in W do
        if c in seen then continue; end if;
        coset := {c+h : h in elements};
        seen join:= coset;
        if coset subset W then Append(~cosets, coset); end if;
    end for;
    return cosets;
end function;

function IntersectionTangent(F, representatives, coset)
    K := CanonicalDivisor(F);
    VK, to_function := RiemannRochSpace(K);
    rows := [];
    for c in coset do
        D := representatives[c];
        if Dimension(D) ne 1 then continue; end if;
        V, inclusion := RiemannRochSpace(K-D);
        rows cat:= [Eltseq(inclusion(v)@@to_function) : v in Basis(V)];
    end for;
    // Use one fixed canonical Riemann--Roch basis for the whole coset.
    // For h^0(D)>=2, the tangent space of W_5^0 is the full ambient space.
    g := Genus(F);
    return g-Rank(Matrix(ConstantField(F), #rows, g, &cat rows));
end function;

function CoordinateInvolution(C, M)
    R := CoordinateRing(Ambient(C));
    n := Nrows(M);
    forms := [&+[M[i,j]*R.j : j in [1..n]] : i in [1..n]];
    return iso<C -> C | forms, forms>;
end function;

function ReducePoint(P, p)
    v := Eltseq(P);
    denominator := LCM([Denominator(a) : a in v]);
    integers := [Integers()!(denominator*a) : a in v];
    common := GCD(integers);
    return [GF(p)!(a div common) : a in integers];
end function;
