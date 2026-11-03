// Compute the elliptic tangent by intersecting tangents to W4 at fibers.
// This avoids a potentially expensive trace calculation in function fields.
// The known elliptic family supplies a line in every tangent considered.
load "family_input.m";
p := StringToInteger(p);
k := GF(p);
M := CuspidalSubspace(ModularForms(N,2));
Qbasis := Matrix(Rationals(),[[Coefficient(qExpansion(f,precision),i):i in [1..precision-1]]:f in Basis(M)]);
U := Matrix(Rationals(),[Eltseq(Solution(Qbasis,v)):v in Rows(target_basis)]);
assert U*Qbasis eq target_basis;
W := U*AtkinLehnerOperator(M,N)*U^-1;
assert W^2 eq IdentityMatrix(Rationals(),target_genus);
assert Rank(W+IdentityMatrix(Rationals(),target_genus)) eq 1;
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
K := CanonicalDivisor(C);
VK,to_function := RiemannRochSpace(K);
assert Dimension(VK) eq source_genus;
rows := [];
for Q in Points(Y) do
    D := Pullback(phi,Divisor(Place(Q))+Divisor(Place(w(Q))));
    assert Degree(D) eq 4;
    if Dimension(D) eq 1 then
        V,inclusion := RiemannRochSpace(K-D);
        rows cat:= [Eltseq(inclusion(v)@@to_function):v in Basis(V)];
    end if;
end for;
annihilator := Matrix(k,#rows,source_genus,&cat rows);
assert Rank(annihilator) eq source_genus-1;
print "elliptic tangent line identified from degree-four fibers";
places := Places(C,1);
for P in places do
    V,inclusion := RiemannRochSpace(K-Divisor(P));
    point_rows := [Eltseq(inclusion(v)@@to_function):v in Basis(V)];
    assert Rank(Matrix(k,point_rows)) eq source_genus-1;
    // Distinct annihilator hyperplanes mean distinct tangent lines.
    assert Rank(Matrix(k,rows cat point_rows)) eq source_genus;
end for;
printf "SUCCESS immersion at all %o rational reduction points\n",#places;
quit;
