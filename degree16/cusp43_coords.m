SetQuitOnError(true);SetColumns(0);None:=0;
load "work/degree16/intermediate-modular-curves/certificates/C_43.132.9.a.2/lmfdb_43.132.9.a.2.m";
Q:=Rationals();P8:=ProjectiveSpace(Q,8);S:=CoordinateRing(P8);X:=Curve(P8,[Evaluate(q,[S.i:i in[1..9]]):q in model_0]);
for ij in[[7,8],[7,9],[8,9]]do
 Z:=Scheme(X,[S.i:i in ij]);print Dimension(Z);ps:=Points(Z);print ps;
end for;quit;
