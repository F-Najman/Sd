SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);tt:=Cputime();Records:=[**];full:=1;dim:=0;
function Code(x)return[<Numerator(a),Denominator(a)>:a in Eltseq(x)];end function;
for n in[9,27,81]do
 K<z>:=CyclotomicField(n);G:=DirichletGroup(163,K);chi:=G.1^ExactQuotient(#G,n);assert Order(chi)eq n and IsEven(chi)and chi(2)^n eq 1 and chi(2)^(n div 3)ne 1;S:=CuspidalSubspace(ModularSymbols(chi,2,0));d:=Dimension(S);assert d eq(n eq 81 select 26 else 24);
 A:=HeckeOperator(S,3)-(chi(3)+3)*IdentityMatrix(K,d);det:=Determinant(A);nd:=Norm(det);assert IsIntegral(nd)and IsOdd(Integers()!nd);full*:=Integers()!nd;dim+:=Degree(K)*d;
 Append(~Records,<n,Degree(K),[Integers()!a:a in Eltseq(DefiningPolynomial(K))],d,[Code(a):a in Eltseq(A)],Code(det),nd>);
 printf "S19_ANTI163_NORM order=%o homology_dimension=%o coefficient_degree=%o norm=%o odd=true elapsed=%o\n",n,d,Degree(K),nd,Cputime(tt);
end for;
assert dim eq 1980 and IsOdd(full);PrintFile("work/degree19/odd_anti163_character_norms_data.m",Sprintf("OddAnti163CharacterNormData:=%o;OddAnti163TotalNorm:=%o;",Records,full):Overwrite:=true);print "S19_ANTI163_ODD_DEGREE_PROVED sign_zero=true anti_homology_dimension=1980";quit;
