// Independent local check for the surface A+C in Pic^5(C).
// Inputs are exact canonical q-expansion models and the forgetting map.
// No conclusion over Q is asserted by this exploratory check alone.
load "family_input.m";
p := StringToInteger(p);
k := GF(p);
M := CuspidalSubspace(ModularForms(N,2));
Qbasis := Matrix(Rationals(),[[Coefficient(qExpansion(f,precision),i):i in [1..precision-1]]:f in Basis(M)]);
U := Matrix(Rationals(),[Eltseq(Solution(Qbasis,v)):v in Rows(target_basis)]);
assert U*Qbasis eq target_basis;
W := U*AtkinLehnerOperator(M,N)*U^-1;
assert W^2 eq IdentityMatrix(Rationals(),target_genus);
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),source_genus-1),source_equations),k);
Y := ChangeRing(Curve(ProjectiveSpace(Rationals(),target_genus-1),target_equations),k);
for Z in [C,Y] do
    assert IsIrreducible(Z) and IsReduced(Z);
    assert ArithmeticGenus(Z) eq Genus(AlgorithmicFunctionField(FunctionField(Z)));
end for;
RC := CoordinateRing(Ambient(C));
RY := CoordinateRing(Ambient(Y));
Lp := ChangeRing(L,k);
Wp := ChangeRing(W,k);
phi := map<C->Y|[&+[Lp[i,j]*RC.j:j in [1..source_genus]]:i in [1..target_genus]]>;
assert Degree(phi) eq 2;
forms := [&+[Wp[i,j]*RY.j:j in [1..target_genus]]:i in [1..target_genus]];
w := iso<Y->Y|forms,forms>;
invariants := Kernel(Wp-IdentityMatrix(k,target_genus));
assert Dimension(invariants) eq 1;
a := Basis(invariants)[1]*Lp;
denominator := &+[a[j]*RC.j:j in [1..source_genus]];
FC := FunctionField(C);
FY := FunctionField(Y);
direction := [];
for i in [1..source_genus] do
    h := FC!(RC.i/denominator);
    // For a quadratic extension, Tr(h)=Norm(h+1)-Norm(h)-1.
    // Pushforward of a rational function is its norm, not its trace.
    s := Pushforward(phi,h+1)-Pushforward(phi,h)-1;
    t := s+Pullback(w,s);
    constants := [c:c in k|t eq FY!c];
    assert #constants eq 1;
    Append(~direction,constants[1]);
end for;
assert &+[a[i]*direction[i]:i in [1..source_genus]] eq k!4;
printf "elliptic_tangent_direction=%o\n",direction;
pts := Points(C);
for P in pts do
    // Canonical coordinates give the Abel-map tangent line at P.
    assert Rank(Matrix(k,[direction,Eltseq(P)])) eq 2;
end for;
printf "SUCCESS immersion at all %o rational reduction points\n",#pts;
quit;
