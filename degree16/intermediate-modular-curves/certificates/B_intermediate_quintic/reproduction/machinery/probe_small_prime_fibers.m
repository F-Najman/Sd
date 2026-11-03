// Exploratory only: enumerate quotient fibers, including their multiplicities.
// Deliberately independent of any hard-coded elliptic group order.
load "family_input.m";
load "../../quotient_rational_fibers.m";
p := StringToInteger(p);
M := CuspidalSubspace(ModularForms(N,2));
B := Matrix(Rationals(),[[Coefficient(qExpansion(f,precision),i):
    i in [1..precision-1]]:f in Basis(M)]);
U := Matrix(Rationals(),[Eltseq(Solution(B,v)):v in Rows(target_basis)]);
assert U*B eq target_basis;
W := U*AtkinLehnerOperator(M,N)*U^-1;
assert W^2 eq IdentityMatrix(Rationals(),target_genus);
assert Rank(W+IdentityMatrix(Rationals(),target_genus)) eq 1;
Y := ChangeRing(Curve(ProjectiveSpace(Rationals(),target_genus-1),target_equations),GF(p));
fibers := QuotientRationalFibers(Y,ChangeRing(W,GF(p)),p);
printf "prime=%o quotient fibers=%o\n",p,#fibers;
for D in fibers do
    print [<Degree(t[1]),t[2]>:t in Decomposition(D)];
end for;
print "SUCCESS fiber diagnostic, not a classification certificate";
quit;
