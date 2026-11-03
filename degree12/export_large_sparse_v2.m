SetQuitOnError(true);SetColumns(0);SetMemoryLimit(160*10^9);SetSeed(20261029);SequenceOut:="unused_export_only";
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree12/large_orders/strange_primes_export.magma";
import "/opt/magma-2.30-1/package/Geometry/ModSym/operators.m": Get_Tquot,Heilbronn,get_fixed_eps_values;
import "/opt/magma-2.30-1/package/Geometry/ModSym/core.m": UnwindManinSymbol;
// Store the existing quotient map in dense/sparse blocks without forming
// a dense matrix of its sparse rows. No quotient relations are changed.
procedure CompactQuotient(~M,raw)
 if Type(raw)ne SeqEnum then return;end if;
 F:=BaseField(M);d:=Degree(Universe(raw));V:=VectorSpace(F,d);dense:=[i:i in[1..#raw]|Weight(raw[i])ge 0.3*d];sparse:=[i:i in[1..#raw]|Weight(raw[i])lt 0.3*d];idx:=[0:i in[1..#raw]];
 A:=ZeroMatrix(F,#dense,d);for i in[1..#dense]do idx[dense[i]]:=i;A[i]:=V!raw[dense[i]];end for;
 C:=SparseMatrix(F,#sparse,d);for i in[1..#sparse]do idx[sparse[i]]:=-i;v:=raw[sparse[i]];for j in Support(v)do C[i,j]:=F!v[j];end for;end for;
 eps:=ValueList(DirichletCharacter(M));qq:=M`quot;qq`Scoef:=ChangeUniverse(qq`Scoef,F);mixed:=<idx,A,C,V,eps>;qq`Tquot:=mixed;qq`Tquot_mixed:=mixed;M`quot:=qq;
end procedure;
// Evaluate the usual Heilbronn action directly into a sparse matrix.
function DirectSparseHecke(M,n)
 Get_Tquot(M,~qq,~qt,~Action2,~Action);
 hl:=Heilbronn(M,n,false);pp:=M`mlist`p1list;F:=BaseField(M);d:=Dimension(M);ans:=SparseMatrix(F,d,d);dat:=<pp,qt,qq`Squot,qq`Scoef,get_fixed_eps_values(M)>;
 for i in[1..d]do
  uv,w:=UnwindManinSymbol(qq`Sgens[qq`Tgens[i]],M`mlist);v:=Action2(dat,uv,hl[2]);
  for j in Support(v)do ans[i,j]:=F!v[j];end for;
 end for;
 return ans;
end function;
p:=StringToInteger(P);n:=StringToInteger(OrderToTest);tt:=Cputime();q:=aux_prime(p);Fq:=GF(q);G:=DirichletGroup(p,Fq);chi:=G.1^ExactQuotient(#G,n);assert Order(chi)eq n and IsEven(chi);
print "S12_SPARSE_EXPORT_IMPLEMENTATION direct_compact_v2";M:=ModularSymbols(chi,2,1);raw:=M`quot`Tquot;
ReferenceT:=ZeroMatrix(Fq,0,0);if assigned CheckMatrix then ReferenceT:=HeckeOperator(M,2);M`hecke_operator:=[];end if;
CompactQuotient(~M,raw);delete raw;assert Rank(BoundaryMap(M))eq 2;k:=Dimension(M)-2;V,VtoM,MtoV:=VectorSpace(M);e:=MtoV(M!<1,[Cusps()|0,Infinity()]>);T:=DirectSparseHecke(M,2);if assigned CheckMatrix then assert Matrix(T)eq ReferenceT;print "S12_DIRECT_SPARSE_FULL_MATRIX_MATCH";end if;e1:=eisenstein_killer(e,T,2,chi(2));assert not IsZero(e1);u:=Random(V);nd:=Degree(V);
PrintFile(SparseOut,Sprintf("%o %o %o %o",q,nd,k,NNZEntries(T)):Overwrite:=true);
PrintFile(SparseOut,&cat[IntegerToString(Integers()!a)cat " ":a in Eltseq(e1)]);
PrintFile(SparseOut,&cat[IntegerToString(Integers()!a)cat " ":a in Eltseq(u)]);
for i in[1..nd]do
 supp:=Support(T,i);PrintFile(SparseOut,IntegerToString(#supp)cat " "cat &cat[IntegerToString(j-1)cat " "cat IntegerToString(Integers()!T[i,j])cat " ":j in supp]);
end for;
vv:=e1;prefix:=[];uc:=Matrix(Fq,nd,1,Eltseq(u));for i in[1..64]do Append(~prefix,Integers()!(vv*uc)[1]);vv:=vv*T;end for;
PrintFile(SparseOut,"64 "cat &cat[IntegerToString(a)cat " ":a in prefix]);
printf "S12_SPARSE_EXPORT_COMPLETE p=%o order=%o q=%o dimension=%o nnz=%o native_prefix=64 elapsed=%o\n",p,n,q,k,NNZEntries(T),Cputime(tt);quit;
