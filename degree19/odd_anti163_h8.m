SetQuitOnError(true);SetColumns(0);SetMemoryLimit(32*10^9);tt:=Cputime();Records:=[**];
p:=163;ord:=81;
for sign in[1,-1]do
 S:=CuspidalSubspace(ModularSymbolsH(p,[1],2,sign));g:=Dimension(S);
 function T(n)return Transpose(DualHeckeOperator(S,n));end function;
 D2:=(T(2)^2-T(4))/2;assert D2^ord eq 1;H:=D2^3;assert H^27 eq 1;B:=BasisMatrix(RowSpace(H-1));r:=Nrows(B);printf "S19_ANTI163_H8_START sign=%o genus=%o anti_dimension=%o elapsed=%o\n",sign,g,r,Cputime(tt);
 D3:=(T(3)^2-T(9))/3;A:=T(3)-1-3*D3;AA:=Solution(B,B*A);assert AA*B eq B*A;det:=Determinant(AA);assert IsIntegral(det);odd:=IsOdd(Integers()!det);
 Append(~Records,<sign,g,r,det,[<Numerator(z),Denominator(z)>:z in Eltseq(AA)]>);printf "S19_ANTI163_H8_RESULT sign=%o odd=%o determinant=%o elapsed=%o\n",sign,odd,det,Cputime(tt);
end for;
PrintFile("work/degree19/odd_anti163_h8_data.m",Sprintf("OddAnti163Data:=%o;",Records):Overwrite:=true);print "S19_ANTI163_H8_TEST_COMPLETE";quit;
