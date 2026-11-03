SetQuitOnError(true);SetColumns(0);SetMemoryLimit(32*10^9);tt:=Cputime();
// Sign zero, rational Gamma_1 modular symbols. The integral cuspidal lattice
// is the kernel of H_1(X,C;Z)->Z[C]^0, hence the actual H_1(X;Z).
M:=ModularSymbolsH(163,[1],2,0);S:=CuspidalSubspace(M);d:=Dimension(S);assert d eq 2054;L:=Lattice(S);assert Rank(L)eq d;
printf "S19_DIRECT163_INTEGRAL_HOMOLOGY rank=%o elapsed=%o\n",d,Cputime(tt);
function T(n)return ChangeRing(IntegralHeckeOperator(S,n),Integers());end function;
T2:=T(2);D2:=ChangeRing((ChangeRing(T2,Rationals())^2-ChangeRing(T(4),Rationals()))/2,Integers());assert D2^81 eq IdentityMatrix(Integers(),d);
I:=IdentityMatrix(GF(2),d);DD:=ChangeRing(D2,GF(2));K:=VectorSpace(GF(2),d);
PrintFile("work/degree19/direct_two163_data.m",Sprintf("DirectTwo163Dimension:=%o;DirectTwo163Diamond:=Matrix(Integers(),%o,%o,%o);",d,d,d,Eltseq(D2)):Overwrite:=true);
for q in[3,5]do
 Tq:=T(q);Dq:=ChangeRing((ChangeRing(Tq,Rationals())^2-ChangeRing(T(q^2),Rationals()))/q,Integers());A:=Tq-IdentityMatrix(Integers(),d)-q*Dq;assert A*D2 eq D2*A;
 K:=K meet Nullspace(ChangeRing(A,GF(2)));rk:=Rank(BasisMatrix(K)*(DD-I));a2rk:=Rank(BasisMatrix(K)*(ChangeRing(T2,GF(2))-I));a2prk:=Rank(BasisMatrix(K)*(ChangeRing(T2,GF(2))-DD));
 PrintFile("work/degree19/direct_two163_data.m",Sprintf("DirectTwo163A%o:=Matrix(Integers(),%o,%o,%o);",q,d,d,Eltseq(A)));
 printf "S19_DIRECT163_TWO_KERNEL q=%o dimension=%o diamond_difference_rank=%o A2_rank=%o A2prime_rank=%o elapsed=%o\n",q,Dimension(K),rk,a2rk,a2prk,Cputime(tt);
 if rk eq 0 then print "S19_DIRECT163_DIAMOND_TRIVIAL_ON_RATIONAL_TWO_TORSION_CERTIFIED";break;end if;
end for;
print "S19_DIRECT163_TWO_TEST_COMPLETE";quit;
