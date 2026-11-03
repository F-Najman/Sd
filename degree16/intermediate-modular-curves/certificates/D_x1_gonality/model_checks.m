// For each level and prime of Theorem D (and the tests): the plane model F of X1(N) (Sutherland-van Hoeij),
// scaled to a primitive integral polynomial, has deg_y(F mod p) = deg_y F, F mod p is irreducible over
// F_p(x) with exact constant field F_p, and its function field has genus g(X1(N)). By the paper (Section 2.2)
// the function field of F mod p is then that of X1(N) over F_p. Run from this folder: magma -b model_checks.m
SetQuitOnError(true); SetMemoryLimit(32 * 2^30);
// Some model files reassign x and y, so the ring is declared afresh before each model is loaded.
procedure Check(X, N, p, gX)
    Z := PolynomialRing(Integers(), 2);
    den := LCM([Denominator(c) : c in Coefficients(X)]);
    F := Z ! (den * X); F := F div GCD([c : c in Coefficients(F)]);         // primitive
    R<t> := FunctionField(GF(p)); S<Y> := PolynomialRing(R);
    Fp := Evaluate(ChangeRing(F, GF(p)), [t, Y]);
    assert Degree(Fp) eq Degree(F, 2);
    assert IsIrreducible(Fp);
    K := FunctionField(Fp);
    assert DimensionOfExactConstantField(K) eq 1;
    assert Genus(K) eq gX;
    printf "MODEL_OK N=%o p=%o genus=%o\n", N, p, gX;
end procedure;
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_26.txt"; Check(X, 26, 3, 10);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_26.txt"; Check(X, 26, 5, 10);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_26.txt"; Check(X, 26, 7, 10);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_29.txt"; Check(X, 29, 2, 22);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_29.txt"; Check(X, 29, 3, 22);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_29.txt"; Check(X, 29, 5, 22);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_41.txt"; Check(X, 41, 2, 51);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_42.txt"; Check(X, 42, 5, 25);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_43.txt"; Check(X, 43, 2, 57);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_44.txt"; Check(X, 44, 3, 36);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_45.txt"; Check(X, 45, 2, 41);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_46.txt"; Check(X, 46, 3, 45);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_47.txt"; Check(X, 47, 2, 70);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_48.txt"; Check(X, 48, 5, 37);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_49.txt"; Check(X, 49, 2, 69);
A<x, y> := PolynomialRing(Rationals(), 2); load "models/X1_50.txt"; Check(X, 50, 3, 48);
print "ALL_MODELS_OK"; quit;
