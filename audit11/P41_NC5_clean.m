SetColumns(0);SetQuitOnError(true);SetMemoryLimit(12*10^9);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");Attach("/home/fnajman/degree9_torsion/nonic-torsion/common/fast_hecke.m");tt:=Cputime();X:=MDX1(41,GF(2));
pl:=NoncuspidalPlaces(X,5);assert #pl eq 2;
A:=[HeckeOperatorFast(X,3,P)-Divisor(P)-3*Divisor(DiamondOperator(X,3,P)):P in pl];
assert DiamondOperator(X,PrimitiveRoot(41),pl[1])eq pl[2];
for ij in [[1,1],[1,2]]do
 B:=A[ij[1]]+A[ij[2]];assert Degree(B)eq 0;flag:=IsPrincipal(B);assert not flag;
 printf "DECIC41_MIXED_NC5 pair=%o principal=%o elapsed=%o\n",ij,flag,Cputime(tt);
end for;
print "DECIC41_NC5_COMPLETE all_cases_covered_by_diamond_symmetry=true";quit;
