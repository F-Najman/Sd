SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();out:=[**];tot:=[Rationals()|0:f in[1..21]];gd:=0;
function Code(z)return[<Numerator(a),Denominator(a)>:a in Eltseq(z)];end function;
for n in[1,3,7,9,21,63]do
 K<z>:=CyclotomicField(n);G:=DirichletGroup(127,K);chi:=G.1^ExactQuotient(#G,n);assert IsEven(chi)and Order(chi)eq n;
 S:=CuspidalSubspace(ModularSymbols(chi,2,1));d:=Dimension(S);gd+:=d*Degree(K);T:=HeckeOperator(S,2);H0:=2*IdentityMatrix(K,d);H1:=T;cs:=[Trace(Trace(H1))];
 for f in[2..21]do H2:=T*H1-2*chi(2)*H0;Append(~cs,Trace(Trace(H2)));H0:=H1;H1:=H2;end for;
 for f in[1..21]do tot[f]+:=cs[f];end for;
 Append(~out,<n,[Integers()!a:a in Eltseq(DefiningPolynomial(K))],d,[Code(a):a in Eltseq(T)],Code(chi(2)),cs>);
 print "S21_FROB127_CHARACTER",n,d,Degree(K),Cputime(tt);
end for;assert gd eq 610;
PrintFile("work/degree21/frobenius127_data.m",Sprintf("Frob127Data:=%o;Frob127Trace:=%o;Frob127PointCounts:=%o;",out,tot,[2^f+1-tot[f]:f in[1..21]]):Overwrite:=true);
print "S21_FROB127_ALL_DEGREES_COMPLETE",Cputime(tt);quit;
