// EXPLORATORY ONLY: JH's character-component lattice has not been identified
// with the integral homology of the actual curve. These are bounds for that
// analytic lattice, NOT accepted torsion bounds for the curve Jacobian.
// See INTEGRAL_HOMOLOGY_AUDIT.md before using any output.
// For odd good p, Frobenius fixes rational torsion, so
// 1-T_p+p< p > kills it. Recover p< p > as T_p^2-T_(p^2).
// Matrices are transported to the lattice returned by this constructor.
delta := [1,7,9,15,17,23,25,31,33,39,41,47,49,55,57,63];
J := JH(64,delta);
assert Dimension(J) eq 5;
B := BasisMatrix(IntegralHomology(J));
assert Nrows(B) eq 10 and Ncols(B) eq 10;
I := IdentityMatrix(Rationals(),10);
relations := ZeroMatrix(Integers(),0,10);
for p in [3,5,7,11,13] do
    T := HeckeOperator(J,p);
    U := HeckeOperator(J,p^2);
    assert not OnlyUpToIsogeny(T) and not OnlyUpToIsogeny(U);
    A := B*(I-Matrix(T)+Matrix(T)^2-Matrix(U))*B^-1;
    assert &and[Denominator(c) eq 1:c in Eltseq(A)];
    A := ChangeRing(A,Integers());
    // Homology vectors act on the right. The common torus kernel is dual
    // to Z^10 modulo the sum of the COLUMN lattices of these matrices.
    relations := VerticalJoin(relations,Transpose(A));
    D := SmithForm(relations);
    invariants := [Abs(D[i,i]):i in [1..10]];
    assert &and[a ne 0:a in invariants];
    bound := 2^&+[Valuation(a,2):a in invariants];
    printf "p=%o smith=%o rational_2_primary_order_bound=%o\n",p,invariants,bound;
end for;
print "EXPLORATORY Hecke annihilator calculation; curve torsion NOT certified";
quit;
