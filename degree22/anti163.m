SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();Records:=[**];total:=0;
function Code(x)return[<Numerator(a),Denominator(a)>:a in Eltseq(x)];end function;
for n in [3]do
 K<z>:=CyclotomicField(n);G:=DirichletGroup(163,K);chi:=G.1^ExactQuotient(#G,n);assert Order(chi)eq n and IsEven(chi);
 S:=CuspidalSubspace(ModularSymbols(chi,2,0));d:=Dimension(S);total+:=EulerPhi(n)*d;found:=false;
 for q in[3,5,7,11,13,17,19]do
  A:=HeckeOperator(S,q)-(chi(q)+q)*IdentityMatrix(K,d);dd:=Determinant(A);nn:=Norm(dd);assert IsIntegral(nn);
  printf "S22_ANTI163_TRIAL order=%o q=%o odd=%o elapsed=%o\n",n,q,IsOdd(Integers()!nn),Cputime(tt);
  if IsOdd(Integers()!nn)then
   Append(~Records,<n,q,[Integers()!a:a in Eltseq(DefiningPolynomial(K))],d,[Code(a):a in Eltseq(A)],Code(dd),nn>);found:=true;break;
  end if;
 end for;
 assert found;
end for;
PrintFile("work/degree22/anti163_data.m",Sprintf("Anti163Data:=%o;Anti163Dimension:=%o;",Records,total):Overwrite:=true);print "S22_ANTI163_ALL_ODD_CERTIFIED",total;quit;
