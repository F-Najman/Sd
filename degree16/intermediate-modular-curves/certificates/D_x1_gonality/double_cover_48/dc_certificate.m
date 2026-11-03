// Double-cover lower bound: gon(X over F_p) > dmax, for X = X1(N) -> Y = X/<a> of degree 2.
// (See README.md in this folder for the lemma.) Caller: loads the data file from dc_data.py and
// assigns p (odd, not dividing N) and dmax.
//
// Write k(X) = k(Y)(w) with w^2 = delta, and div_Y(delta) = B + 2G (B = branch divisor).
// A nonconstant f of degree d <= dmax on X either factors through Y, so d >= 2 gon(Y), or has the
// form f = (h + w)/u with u, h in L_Y(E - G), u != 0, E >= 0 effective of degree d - deg(B)/2.

SetQuitOnError(true);
AttachSpec("../../../third_party/CurveArith/CurveArith.spec");
if not assigned Shard then Shard := 0; Shards := 1; end if;         // E's are split round-robin
if not assigned SelfCheck then SelfCheck := 0; end if;              // every k-th candidate: slow degree too
if not assigned SkipGonY then SkipGonY := false; end if;            // only for shards > 0 (shard 0 checks it)
assert IsOdd(p) and N mod p ne 0;
Fp := GF(p);
P := ProjectiveSpace(Fp, gY - 1);
S := CoordinateRing(P);
Poly := func< terms | &+[S | t[2] * &*[S | S.(i + 1) : i in t[1]] : t in terms] >;
Y := Curve(P, [Poly(r) : r in Rel]);
FFY := FunctionField(Y);
FY, toFY := AlgorithmicFunctionField(FFY);
assert Genus(FY) eq gY;
Kfrac := FieldOfFractions(S);
yfun := func< F | toFY(FFY ! (Kfrac ! (F / S.1^TotalDegree(F)))) >;   // form in y -> function F/y_0^k
delta := yfun(Poly(Nm)) / yfun(Poly(Dn));
assert delta ne 0;

// Branch divisor B (odd part of div delta) and G.
Dd := Divisor(delta);
supp, mult := Support(Dd);
B := &+[Parent(Dd) | Divisor(supp[i]) : i in [1..#supp] | IsOdd(mult[i])];
G := (Dd - B) div 2;
assert Degree(B) eq (2*gX - 2) - 2*(2*gY - 2);            // Riemann-Hurwitz
c := Degree(B) div 2;

// k(X) = k(Y)(w). Only shard 0 (or a self-check) needs k(X) itself: the degrees are computed on Y.
if not assigned NeedFX then NeedFX := Shard eq 0 or SelfCheck gt 0; end if;
if NeedFX then
    PT<T> := PolynomialRing(FY);
    FX<w> := FunctionField(T^2 - delta);
    assert Genus(FX) eq gX;                  // k(Y)(sqrt(delta)) is the function field of X1(N) mod p
else
    FX := FY; w := FY ! 0;                    // placeholders; used only by the self-check (SelfCheck > 0)
end if;
printf "SETUP N=%o a=%o p=%o gX=%o gY=%o deg(B)=%o dmax=%o\n", N, a, p, gX, gY, Degree(B), dmax;

// Factoring case.
if Shard eq 0 or not SkipGonY then
    gonY := CAGonality(FY);
    printf "gon(Y over F_%o) = %o\n", p, gonY;
    assert 2 * gonY gt dmax;
end if;

// Non-factoring case. It suffices to take E of degree exactly emax: if f arises from E, it also
// arises from E + P for any place P (L_Y(E - G) only grows), so pad E up to degree emax.
emax := dmax - c;
assert emax ge 0;
function EffectiveDivisors(e)            // all effective divisors of degree exactly e
    if e eq 0 then return [DivisorGroup(FY)!0]; end if;
    pl := &cat[Places(FY, j) : j in [1..e]];
    out := [];
    procedure Rec(i0, rest, D, ~out)
        if rest eq 0 then Append(~out, D); return; end if;
        for i in [i0..#pl] do
            if Degree(pl[i]) le rest then Rec(i, rest - Degree(pl[i]), D + Divisor(pl[i]), ~out); end if;
        end for;
    end procedure;
    Rec(1, e, DivisorGroup(FY)!0, ~out);
    return out;
end function;

degX := func< f | Degree(Denominator(Divisor(f))) >;     // degree of f on X (slow; self-check only)

// Degree of f = (h + w)/u on X, computed on Y. f is a root of T^2 - t T + n with t = 2h/u and
// n = (h^2 - delta)/u^2, functions on Y. Over a place P of Y, f has poles above P exactly when t or n
// has a pole at P, and the total pole order above P is max(0, -v_P(t), -v_P(n)) (the Newton polygon
// of T^2 - t T + n, case by case). So deg f = deg of the smallest A on Y with t, n in L_Y(A).
function PolesAbove(vt, vn) return Max([0, -vt, -vn]); end function;
function DegreeOnY(h, u, S)
    t := 2 * h / u; n := (h^2 - delta) / u^2;
    return &+[Integers() | Degree(P) * PolesAbove(Valuation(t, P), Valuation(n, P)) : P in S];
end function;

// Cheap lower bound: n = f * sigma(f) and t = f + sigma(f) are functions on Y, and by the formula
// above deg_X f >= deg_Y n and deg_X f >= deg_Y t. Computing the degree of one function on Y needs no
// places at all, so most candidates are discarded without locating the zeros of u.
count_E := 0; count_f := 0; count_filtered := 0; mindeg := Infinity(); witness := false;
// Sharding: E goes to shard (EKey(E) mod Shards). EKey depends only on E, not on the order in which Magma
// lists places, so the shards are disjoint and together cover every E, whatever that order is in each process.
fkey := yfun(S.2);                                   // the function y_1/y_0 on Y
function PlaceKey(P)
    f := Valuation(fkey, P) ge 0 select fkey else 1 / fkey;
    m := MinimalPolynomial(Evaluate(f, P), GF(p));
    return &+[Integers() | (Integers() ! c) * p^(k - 1) : k -> c in Eltseq(m)];
end function;
function EKey(E)
    supp, mult := Support(E);
    return &+[Integers() | mult[i] * PlaceKey(supp[i]) : i in [1..#supp]];
end function;
Ecount := -1;
for e in [emax] do
    for E in EffectiveDivisors(e) do
        Ecount +:= 1;
        if EKey(E) mod Shards ne Shard then continue; end if;
        count_E +:= 1;
        if count_E gt 1 then printf "PROGRESS E=%o done=%o candidates=%o seconds=%o\n", Ecount, count_E - 1, count_f, Cputime(); end if;
        V, phi := RiemannRochSpace(E - G);
        if Dimension(V) eq 0 then continue; end if;
        for vu in V do
            if vu eq 0 or Eltseq(vu)[Depth(vu)] ne 1 then continue; end if;   // u up to scalar
            u := phi(vu);
            S := false;                                   // places for the exact degree, when needed
            // h only matters modulo the span of u (h -> h + c u changes f by the constant c).
            C := Complement(V, sub<V | vu>);
            for vh in C do
                count_f +:= 1;
                h := phi(vh);
                lb := Degree((h^2 - delta) / u^2);
                if lb le dmax then lb := Max(lb, Degree(2 * h / u)); end if;
                if lb gt dmax then
                    count_filtered +:= 1; dg := lb;       // deg f >= lb > dmax
                else
                    if S cmpeq false then                 // poles of t, n lie over supp(E + H) and the zeros of u
                        S := Seqset(Support(E - G)) join Seqset(Support(Divisor(u) + E - G));
                    end if;
                    dg := DegreeOnY(h, u, S);
                end if;
                if SelfCheck gt 0 and count_f mod SelfCheck eq 0 then
                    dX := degX((FX ! h + w) / FX ! u); assert dg eq dX or (dg gt dmax and dX ge dg);
                end if;
                if dg lt mindeg then mindeg := dg; end if;
                if dg le dmax then witness := <E, vu, vh, dg>; end if;
            end for;
        end for;
    end for;
end for;
printf "SEARCH shard=%o/%o effective_E_total=%o effective_E_this_shard=%o candidate_functions=%o min_degree_bound=%o discarded_by_norm_bound=%o\n", Shard, Shards, Ecount + 1, count_E, count_f, mindeg, count_filtered;
if witness cmpne false then
    printf "FOUND a non-factoring function of degree %o <= dmax (E = %o)\n", witness[4], witness[1];
else
    printf "CERTIFIED gon(X1(%o) over F_%o) > %o\n", N, p, dmax;
end if;
quit;
