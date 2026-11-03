SetQuitOnError(true);SetColumns(0);p:=97;h:=Integers()!((GF(p)!PrimitiveRoot(p))^6);S:=CuspidalSubspace(ModularSymbolsH(p,[h],2,1));g:=Dimension(S);T2:=Transpose(DualHeckeOperator(S,2));D2:=(T2^2-Transpose(DualHeckeOperator(S,4)))/2;
// Recover the generator diamond5 and its order3 square on the index6 quotient.
T5:=Transpose(DualHeckeOperator(S,5));D5:=(T5^2-Transpose(DualHeckeOperator(S,25)))/5;H:=D5^2;assert H^3 eq 1;
U:=RowSpace(H-1);B:=BasisMatrix(U);r:=Dimension(U);print "S16_ANTI97",g,r;
T:=Transpose(DualHeckeOperator(S,3));D:=(T^2-Transpose(DualHeckeOperator(S,9)))/3;A:=T-1-3*D;AA:=Solution(B,B*A);assert AA*B eq B*A;det:=Determinant(AA);assert IsIntegral(det)and IsOdd(Integers()!det);
PrintFile("work/degree16/anti97_data.m",Sprintf("Anti97Matrix:=Matrix(Rationals(),%o,%o,%o);Anti97Determinant:=%o;",r,r,Eltseq(AA),det):Overwrite:=true);
printf "S16_ANTI97_ODD_DEGREE_CERTIFIED genus=%o anti_dimension=%o determinant=%o\n",g,r,det;quit;
