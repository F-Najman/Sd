SetQuitOnError(true);SetColumns(0);None:=0;
load "work/degree16/intermediate-modular-curves/certificates/C_43.132.9.a.2/lmfdb_43.132.9.a.2.m";
K:=GF(2);P8:=ProjectiveSpace(K,8);S:=CoordinateRing(P8);X:=Curve(P8,[Evaluate(q,[S.i:i in[1..9]]):q in model_0]);assert IsAbsolutelyIrreducible(X)and Genus(X)eq 9 and ArithmeticGenus(X)eq 9 and Degree(X)eq 16;
pts:=[X![0,0,0,0,0,0,0,0,1],X![0,0,0,0,0,0,0,1,0],X![0,0,0,0,0,1,1,0,0]];assert &and[IsNonsingular(P):P in pts];
cs:=[FunctionFieldDivisor(Divisor(Places(P)[1])):P in pts];assert [Degree(c):c in cs]eq[1,1,1];
D1:=19*(cs[2]-cs[1]);D2:=19*(cs[3]-cs[1]);
for D in[D1,D2,D1+D2]do
 printf "S16_TORSION43_REDUCTION dim=%o doubled_dim=%o\n",Dimension(D),Dimension(2*D);assert Dimension(D)eq 0 and Dimension(2*D)eq 1;
end for;print "S16_TORSION43_REDUCTION_INJECTIVE_COMPLETE";quit;
