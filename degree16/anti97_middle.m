SetQuitOnError(true);SetColumns(0);p:=97;h:=Integers()!((GF(p)!PrimitiveRoot(p))^48);S:=CuspidalSubspace(ModularSymbolsH(p,[h],2,1));g:=Dimension(S);T2:=Transpose(DualHeckeOperator(S,2));D2:=(T2^2-Transpose(DualHeckeOperator(S,4)))/2;
// Recover the generator diamond5 and its order3 square on the index6 quotient.
T5:=Transpose(DualHeckeOperator(S,5));D5:=(T5^2-Transpose(DualHeckeOperator(S,25)))/5;H:=D5^12;assert H^4 eq 1;
U:=Nullspace(H+1);B:=BasisMatrix(U);r:=Dimension(U);print "S16_ANTI97",g,r;
AS:=[];for q in[3,5,7,11]do
 T:=Transpose(DualHeckeOperator(S,q));D:=(T^2-Transpose(DualHeckeOperator(S,q^2)))/q;A:=T-1-q*D;AA:=Solution(B,B*A);assert AA*B eq B*A;assert IsIntegral(Determinant(AA));print "S16_ANTI97_DET",q,Integers()!Determinant(AA)mod 2;Append(~AS,AA);
end for;
for k in[1..0]do C:=&+[AS[j]:j in[1..4]|IsOdd(k div 2^(j-1))];print "S16_ANTI97_COMBINATION",k,Integers()!Determinant(C)mod 2;end for;quit;
