SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);tt:=Cputime();Records:=[**];
function Code(x)return[Integers()!a:a in Eltseq(x,GF(2))];end function;
// Delta has odd order81, so its character idempotents are integral at2.
// Work with sign ZERO. At level163 there is no elliptic order2 stabilizer;
// the remaining elliptic order3 stabilizers have invertible order at2.
for n in[3,9,27,81]do
 f:=Order(Integers(n)!2);F:=GF(2^f);G:=DirichletGroup(163,F);assert #G eq n or #G mod n eq 0;chi:=G.1^ExactQuotient(#G,n);assert Order(chi)eq n and IsEven(chi);
 M:=ModularSymbols(chi,2,0);S:=CuspidalSubspace(M);d:=Dimension(S);assert Rank(BoundaryMap(M))eq 2;
 D2:=chi(2);assert Order(D2)eq n;I:=IdentityMatrix(F,d);K:=VectorSpace(F,d);T2:=HeckeOperator(S,2);
 As:=[**];for q in[3,5,7]do
  Tq:=HeckeOperator(S,q);A:=Tq-(1+chi(q))*I;Append(~As,<q,[[Code(a):a in Eltseq(v)]:v in Rows(A)]>);K:=K meet Nullspace(A);
  rk:=Rank(BasisMatrix(K)*(T2-D2*I));rk2:=Rank(BasisMatrix(K)*(T2-I));
  printf "S19_CHARACTER_TWO163 order=%o coefficient_degree=%o dimension=%o q=%o kernel_dimension=%o A2prime_rank=%o A2_rank=%o elapsed=%o\n",n,f,d,q,Dimension(K),rk,rk2,Cputime(tt);
 end for;
 Append(~Records,<n,f,[Integers()!a:a in Eltseq(DefiningPolynomial(F,GF(2)))],d,Code(D2),[[Code(a):a in Eltseq(v)]:v in Rows(T2)],As>);
end for;
PrintFile("work/degree19/two163_characters_data.m",Sprintf("Two163CharacterData:=%o;",Records):Overwrite:=true);print "S19_CHARACTER_TWO163_TEST_COMPLETE";quit;
