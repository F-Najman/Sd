SetQuitOnError(true);SetColumns(0);out:=[**];s1:=0;s2:=0;gd:=0;
function Code(x)return[<Numerator(a),Denominator(a)>:a in Eltseq(x)];end function;
for n in[1,2,4]do
 K<z>:=CyclotomicField(n);G:=DirichletGroup(89,K);chi:=G.1^ExactQuotient(#G,n);S:=CuspidalSubspace(ModularSymbols(chi,2,1));d:=Dimension(S);T:=HeckeOperator(S,3);a:=Trace(Trace(T));b:=Trace(Trace(T^2-6*chi(3)*IdentityMatrix(K,d)));s1+:=a;s2+:=b;gd+:=d*Degree(K);Append(~out,<n,d,[Code(x):x in Eltseq(T)],Code(chi(3)),a,b>);
end for;assert gd eq 27;
PrintFile("work/degree22/frobenius89_at3_data.m",Sprintf("Q89Frob3Data:=%o;Q89PointCountsAt3:=%o;",out,[4-s1,10-s2]):Overwrite:=true);print "S22_QUOTIENT89_POINTCOUNTS_AT3",[4-s1,10-s2];quit;
