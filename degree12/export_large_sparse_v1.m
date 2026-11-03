SetQuitOnError(true);SetColumns(0);SetMemoryLimit(160*10^9);SetSeed(20261029);SequenceOut:="unused_export_only";
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree12/large_orders/strange_primes_export.magma";
p:=StringToInteger(P);n:=StringToInteger(OrderToTest);tt:=Cputime();q:=aux_prime(p);Fq:=GF(q);G:=DirichletGroup(p,Fq);chi:=G.1^ExactQuotient(#G,n);assert Order(chi)eq n and IsEven(chi);
M:=ModularSymbols(chi,2,1);assert Rank(BoundaryMap(M))eq 2;k:=Dimension(M)-2;V,VtoM,MtoV:=VectorSpace(M);e:=MtoV(M!<1,[Cusps()|0,Infinity()]>);T:=sparse_hecke_lean(M,2);e1:=eisenstein_killer(e,T,2,chi(2));assert not IsZero(e1);u:=Random(V);nd:=Degree(V);
PrintFile(SparseOut,Sprintf("%o %o %o %o",q,nd,k,NNZEntries(T)):Overwrite:=true);
PrintFile(SparseOut,&cat[IntegerToString(Integers()!a)cat " ":a in Eltseq(e1)]);
PrintFile(SparseOut,&cat[IntegerToString(Integers()!a)cat " ":a in Eltseq(u)]);
for i in[1..nd]do
 supp:=Support(T,i);PrintFile(SparseOut,IntegerToString(#supp)cat " "cat &cat[IntegerToString(j-1)cat " "cat IntegerToString(Integers()!T[i,j])cat " ":j in supp]);
end for;
vv:=e1;prefix:=[];uc:=Matrix(Fq,nd,1,Eltseq(u));for i in[1..64]do Append(~prefix,Integers()!(vv*uc)[1]);vv:=vv*T;end for;
PrintFile(SparseOut,"64 "cat &cat[IntegerToString(a)cat " ":a in prefix]);
printf "S12_SPARSE_EXPORT_COMPLETE p=%o order=%o q=%o dimension=%o nnz=%o native_prefix=64 elapsed=%o\n",p,n,q,k,NNZEntries(T),Cputime(tt);quit;
