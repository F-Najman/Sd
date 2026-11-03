SetQuitOnError(true);SetColumns(0);
R<x>:=PolynomialRing(Rationals());pol:=x^7+5*x^6+2*x^5-20*x^4-19*x^3+15*x^2+10*x+1;
S:=ModularSymbols(193,2,-1);I:=IntegralHeckeOperator(S,1);T2:=IntegralHeckeOperator(S,2);W:=ChangeRing(AtkinLehnerOperator(S,193),Integers());
print "S16_INTEGRAL_CHECK",T2 eq ChangeRing(HeckeOperator(S,2),Integers());assert W*T2 eq T2*W;assert W^2 eq I;
A:=ChangeRing(Evaluate(pol,T2)*(IntegralHeckeOperator(S,3)-4*I),GF(2));WW:=ChangeRing(W,GF(2));tt:=[A*ChangeRing(IntegralHeckeOperator(S,n),GF(2)):n in[1,2]];
for mode in[0,1,2]do
 rows:=mode eq 0 select Matrix([Eltseq(tt[1]),Eltseq(tt[2])])else mode eq 1 select Matrix([Eltseq(tt[1]),Eltseq(tt[1]*WW)])else Matrix([Eltseq(tt[1]*WW),Eltseq(tt[2]*WW)]);
 print "S16_XZERO193_CUSP_FI",mode,Rank(rows);assert Rank(rows)eq 2;
end for;print "S16_XZERO193_CUSP_FI_COMPLETE";quit;
