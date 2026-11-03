// Certificate: a rational cuspidal divisor D on X_Delta(N) with h^0(D) >= 2, hence gon_Q <= deg D.
//
// Caller assigns: level, Delta (the elements of Delta), g, orbit_degrees, a, label.
// D = sum_i a[i] * C_i, where C_1, C_2, ... are the Galois orbits of cusps in the order used
// by Zywina's Modular package (their degrees are asserted to equal orbit_degrees).
//
// Weight-2 modular forms f correspond to differentials f dq/q with at most simple poles at cusps.
// Such a differential lies in H^0(K - D) exactly when f vanishes to order >= a[i] + 1 at the cusps
// in C_i. Conditions at one cusp of each orbit suffice, because the basis is rational.
// Riemann-Roch:  h^0(D) = deg D + 1 - g + h^0(K - D).

AttachSpec("../../../../third_party/Modular/Modular.spec");
SetQuitOnError(true);

U := [u : u in [1..level-1] | GCD(u, level) eq 1];
H := [[d, 0, 0, 1] : d in Delta] cat [[1, 1, 0, 1]] cat [[1, 0, 0, u] : u in U];  // H_Delta
X := CreateModularCurveRec(level, H);
X := FindModularForms(2, X : lll := [false, false], saturation := [false, false]);
assert X`genus eq g;
assert [#O : O in X`cusp_orbits] eq orbit_degrees;
assert #a eq #orbit_degrees and Min(a) ge -1;

// Name each orbit by a representative cusp a/c = A*infinity (A in SL_2(Z)) and its width.
function CuspName(i)
    A := X`cusps[X`cusp_orbits[i][1]];
    return Sprintf("%o/%o (width %o)", A[1,1], A[2,1], X`widths[X`cusp_orbits[i][1]]);
end function;
names := [CuspName(i) : i in [1..#a]];
if assigned expected_cusps then assert names eq expected_cusps; end if;

prec := [1 : c in [1..X`vinf]];
for i in [1..#a] do for c in X`cusp_orbits[i] do prec[c] := Max(1, a[i] + 1) + 1; end for; end for;
X := IncreaseModularFormPrecision(X, prec);

function H0KminusD(m)  // m[i] = number of vanishing conditions at orbit i
    rows := [];
    for i in [1..#m] do
        c := X`cusp_orbits[i][1];
        for k in [0..m[i] - 1] do
            coeffs := [Eltseq(Coefficient(X`F[j][c], k)) : j in [1..#X`F]];
            rows cat:= [[Rationals()!coeffs[j][e] : j in [1..#X`F]] : e in [1..#coeffs[1]]];
        end for;
    end for;
    return #rows eq 0 select #X`F else #X`F - Rank(Matrix(Rationals(), rows));
end function;

assert H0KminusD([1 : i in a]) eq g;  // sanity check: holomorphic differentials
d := &+[a[i] * orbit_degrees[i] : i in [1..#a]];
h0D := d + 1 - g + H0KminusD([ai + 1 : ai in a]);
assert h0D ge 2;
terms := [Sprintf("%o*[orbit of %o, degree %o]", a[i], names[i], orbit_degrees[i]) : i in [1..#a] | a[i] ne 0];
printf "CERTIFIED %o: deg D = %o, h0(D) = %o, so gon_Q <= %o, where\n  D = %o\n", label, d, h0D, d, Join(terms, "\n    + ");
printf "ORBITS %o\n", names;
quit;
