// Isolated check of rational quotient fibers, before large source class groups.
load "family_input.m";
load "../../quotient_rational_fibers.m";
p := StringToInteger(p);
M := CuspidalSubspace(ModularForms(N,2));
Qbasis := Matrix(Rationals(),[[Coefficient(qExpansion(f,precision),i):i in [1..precision-1]]:f in Basis(M)]);
U := Matrix(Rationals(),[Eltseq(Solution(Qbasis,v)):v in Rows(target_basis)]);
assert U*Qbasis eq target_basis;
W := U*AtkinLehnerOperator(M,N)*U^-1;
Y := ChangeRing(Curve(ProjectiveSpace(Rationals(),target_genus-1),target_equations),GF(p));
fibers := QuotientRationalFibers(Y,ChangeRing(W,GF(p)),p);
printf "rational quotient fibers=%o rational source points=%o\n",#fibers,#Points(Y);
assert #fibers eq 12;
print "SUCCESS complete elliptic quotient fibers at level 65, prime 7";
quit;
