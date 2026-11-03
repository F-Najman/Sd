SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();
K<z>:=CyclotomicField(83);G:=DirichletGroup(167,K);chi:=G.1^ExactQuotient(#G,83);assert Order(chi)eq 83 and IsEven(chi);
S:=CuspidalSubspace(ModularSymbols(chi,2,0));d:=Dimension(S);print "S20_ANTI167_DIMENSION",d;assert d eq 26;
function Code(x)return[<Numerator(a),Denominator(a)>:a in Eltseq(x)];end function;
for q in[3,5,7,11]do
 A:=HeckeOperator(S,q)-(chi(q)+q)*IdentityMatrix(K,d);dd:=Determinant(A);nn:=Norm(dd);assert IsIntegral(nn);
 printf "S20_ANTI167_TRIAL prime=%o norm_odd=%o elapsed=%o\n",q,IsOdd(Integers()!nn),Cputime(tt);
 if IsOdd(Integers()!nn)then
  PrintFile("work/degree20/anti167_data.m",Sprintf("Anti167Data:=%o;",<q,[Integers()!a:a in Eltseq(DefiningPolynomial(K))],d,[Code(a):a in Eltseq(A)],Code(dd),nn>):Overwrite:=true);
  print "S20_ANTI167_ODD_DEGREE_CERTIFIED";break;
 end if;
end for;quit;
