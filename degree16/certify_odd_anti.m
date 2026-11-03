SetQuitOnError(true);SetColumns(0);tt:=Cputime();Records:=[**];
for dat in[<89,44,2,1,11,260>,<97,6,5,2,3,28>]do
 p,ind,a,pow,ord,expected:=Explode(dat);h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);dets:=[];
 for sign in[1,-1]do
 S:=CuspidalSubspace(ModularSymbolsH(p,[h],2,sign));g:=Dimension(S);
 function T(n) return Transpose(DualHeckeOperator(S,n));end function;
 Da:=(T(a)^2-T(a^2))/a;H:=Da^pow;assert H^ord eq 1;U:=RowSpace(H-1);B:=BasisMatrix(U);r:=Dimension(U);assert r eq expected;
 D3:=(T(3)^2-T(9))/3;A:=T(3)-1-3*D3;AA:=Solution(B,B*A);assert AA*B eq B*A;det:=Determinant(AA);assert IsIntegral(det)and IsOdd(Integers()!det);Append(~dets,det);
 Append(~Records,<p,ind,sign,g,r,det,[<Numerator(z),Denominator(z)>:z in Eltseq(AA)]>);
 printf "S16_ODD_ANTI p=%o index=%o sign=%o genus=%o anti_dimension=%o determinant=%o elapsed=%o\n",p,ind,sign,g,r,det,Cputime(tt);
 end for;assert IsOdd(Integers()!(&*dets));
end for;
PrintFile("work/degree16/odd_anti_data.m",Sprintf("OddAntiData:=%o;",Records):Overwrite:=true);print "S16_ODD_ANTI_ISOGENIES_COMPLETE";quit;
