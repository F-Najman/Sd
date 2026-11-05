SetQuitOnError(true);SetColumns(0);SetMemoryLimit(160*10^9);SetSeed(20261029);SequenceOut:="unused_export_only";
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree20/strange_primes_export.magma";
import "/opt/magma-2.30-1/package/Geometry/ModSym/operators.m": Get_Tquot,Heilbronn,get_fixed_eps_values;
import "/opt/magma-2.30-1/package/Geometry/ModSym/core.m": UnwindManinSymbol,ManinSymbolApply;
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
M:=ModularSymbols(chi,2,1);raw:=M`quot`Tquot;CompactQuotient(~M,raw);delete raw;
Get_Tquot(M,~qq,~qt,~Action2,~Action);pp:=M`mlist`p1list;hl:=Heilbronn(M,2,false);ns:=#qq`Sgens;nd:=Dimension(M);k:=nd-2;assert Rank(BoundaryMap(M))eq 2;
print "S20_RAW_DIMENSIONS",p,n,ns,nd,hl[2];
R:=SparseMatrix(Fq,ns,ns);dat:=<pp,qt,qq`Squot,qq`Scoef,get_fixed_eps_values(M)>;
function project(v,qt,nd)
 r:=VectorSpace(Fq,nd)!0;
 for j in Support(v)do
  jx:=qt[1][j];rr:=jx gt 0 select qt[2][jx]else qt[3][-jx];r+:=v[j]*(VectorSpace(Fq,nd)!rr);
 end for;return r;
end function;
for i in[1..ns]do
 uv,w:=UnwindManinSymbol(qq`Sgens[i],M`mlist);assert w eq 0;
 for h in hl[2]do
  for term in ManinSymbolApply(<[],h>,qq`Sgens[i],M`mlist,chi,2)do
   c,j:=Explode(term);a:=qq`Squot[j];if a gt 0 then R[i,a]+:=c*qq`Scoef[j];end if;
  end for;
 end for;
 if assigned AuditAll or i le 200 or i mod 1000 eq 0 then
  assert project(R[i],qt,nd)eq Action2(dat,uv,hl[2]);
 end if;
end for;
print "S20_RAW_OPERATOR_PROJECTED",NNZEntries(R),Cputime(tt);
T:=DirectSparseHecke(M,2);V,VtoM,MtoV:=VectorSpace(M);e:=MtoV(M!<1,[Cusps()|0,Infinity()]>);e1:=eisenstein_killer(e,T,2,chi(2));assert not IsZero(e1);
if assigned ReferenceSparse then
 lines:=Split(Read(ReferenceSparse),"\n");assert [StringToInteger(z):z in Split(lines[1]," ")]eq[q,nd,k,NNZEntries(T)];vv:=V![Fq!StringToInteger(z):z in Split(lines[2]," ")];assert vv eq e1;u:=V![Fq!StringToInteger(z):z in Split(lines[3]," ")];
else u:=Random(V);end if;
vs:=VectorSpace(Fq,ns)!0;
for i in[1..nd]do
 t:=qq`Tgens[i];ix:=qt[1][t];row:=ix gt 0 select qt[2][ix]else qt[3][-ix];assert Support(row)eq{i}and row[i]eq 1;vs[t]+:=e1[i];
end for;assert project(vs,qt,nd)eq e1;
us:=VectorSpace(Fq,ns)!0;
uc:=Matrix(Fq,nd,1,Eltseq(u));ud:=qt[2]*uc;uu:=qt[3]*uc;for j in[1..ns]do ix:=qt[1][j];us[j]:=ix gt 0 select ud[ix,1]else uu[-ix,1];end for;
vv:=e1;ww:=vs;checks:=[];uc:=Matrix(Fq,nd,1,Eltseq(u));usc:=Matrix(Fq,ns,1,Eltseq(us));
for i in[1..128]do
 assert(ww*usc)[1]eq(vv*uc)[1];Append(~checks,Integers()!(vv*uc)[1]);vv:=vv*T;ww:=ww*R;
end for;
PrintFile(SparseOut,Sprintf("%o %o %o %o",q,ns,k,NNZEntries(R)):Overwrite:=true);
PrintFile(SparseOut,&cat[IntegerToString(Integers()!a)cat " ":a in Eltseq(vs)]);PrintFile(SparseOut,&cat[IntegerToString(Integers()!a)cat " ":a in Eltseq(us)]);
for i in[1..ns]do supp:=Support(R,i);PrintFile(SparseOut,IntegerToString(#supp)cat " "cat &cat[IntegerToString(j-1)cat " "cat IntegerToString(Integers()!R[i,j])cat " ":j in supp]);end for;
PrintFile(SparseOut,"64 "cat &cat[IntegerToString(a)cat " ":a in checks[1..64]]);
printf "S20_RAW_SPARSE_EXPORT_COMPLETE p=%o order=%o q=%o ambient=%o dimension=%o nnz=%o audited_all=%o seconds=%o\n",p,n,q,ns,k,NNZEntries(R),assigned AuditAll,Cputime(tt);quit;
