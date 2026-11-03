SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");Attach("/home/fnajman/degree9_torsion/nonic-torsion/common/fast_hecke.m");
X:=MDX1(41,GF(2));ss:=NoncuspidalPlaces(X,5);assert #ss eq 2;nc:=[P:P in Cusps(X)|Degree(P)eq 10];assert #nc eq 2;
B:=[HeckeOperatorFast(X,3,P)-Divisor(P)-3*Divisor(DiamondOperator(X,3,P)):P in ss];
for ij in [[3,0],[2,1]]do F:=ij[1]*B[1]+ij[2]*B[2];flag:=IsPrincipal(F);printf "S15_NATIVE41_SS_TRIPLE multiplicities=%o principal=%o elapsed=%o\n",ij,flag,Cputime(tt);assert not flag;end for;
// T_3(C)=<3>C+3C on the nonrational cusp type, and <3> swaps them.
assert Order(GF(41)!3)eq 8;assert Min([k:k in[1..40]|2^k mod 41 in[1,40]])eq 10;
for j in[1,2]do F:=2*(Divisor(nc[1])-Divisor(nc[2]))+B[j];flag:=IsPrincipal(F);printf "S15_NATIVE41_CUSP_SS index=%o principal=%o elapsed=%o\n",j,flag,Cputime(tt);assert not flag;end for;
print "S15_NATIVE41_EXCEPTIONAL_COMPLETE";quit;
