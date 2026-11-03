SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);SetSeed(20261028);
p:=StringToInteger(P);ind:=StringToInteger(Ind);ns:=[StringToInteger(v):v in Split(Tn,",")];qs:=[StringToInteger(v):v in Split(Q,",")];d:=18;tt:=Cputime();
h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);
M:=ModularSymbolsH(p,[h],2,0);MS:=CuspidalSubspace(M);e:=WindingElementProjection(MS);
S:=ModularSymbolsH(p,[h],2,-1);Id:=IntegralHeckeOperator(S,1);
function Dia(q)
 op:=IntegralHeckeOperator(S,q)^2-IntegralHeckeOperator(S,q^2);
 return ChangeRing((1/q)*ChangeRing(op,Rationals()),Integers());
end function;
r:=1;repeat r:=NextPrime(r);until Order(GF(p)!r) eq p-1;
dia:=ChangeRing(Dia(r),GF(2));assert dia^ind eq Parent(dia)!1;
hecke:=[ChangeRing(IntegralHeckeOperator(S,j),GF(2)):j in [1..d]];
// Applying each operator to fixed binary vectors is a linear projection.
// Independence after projection proves independence of the full operators.
g:=Dimension(S); probes:=[Vector(GF(2),[Random(GF(2)):i in [1..g]]):k in [1..4]];
rows:=ZeroMatrix(GF(2),d+(d div 2)*(ind-1),0);
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree18/finite_FI_polynomials.m";
for n in ns do
 TnS:=IntegralHeckeOperator(S,n);
// Every integral polynomial has finite image at these rank-zero levels.
if p in[41,47,59,71]then
 TnMS:=HeckeOperator(MS,n);pol:=CharacteristicPolynomial(TnS);fac:=Factorization(pol);
 flags:=[f[2]ge 2 or IsZero(e*Evaluate(ExactQuotient(pol,f[1]^f[2]),TnMS)):f in fac];
 killpol:=&*[Parent(pol)|fac[i][1]^fac[i][2]:i in[1..#fac]|flags[i]];
else killpol:=FiniteFIPolynomials[<p,n>];end if;t1:=Evaluate(killpol,TnS);
 for q in qs do
  t2:=IntegralHeckeOperator(S,q)-q*Id-Dia(q);t:=ChangeRing(t1*t2,GF(2));
  products:=&cat[[t*dia^k*T:T in hecke[1..k eq 0 select d else d div 2]]:k in [0..ind-1]];
  block:=Matrix([&cat[Eltseq(v*op):v in probes]:op in products]);rows:=HorizontalJoin(rows,block);
  printf "DECIC_FI_COMBINED_STEP p=%o Tn=%o q=%o rank=%o elapsed=%o\n",p,n,q,Rank(rows),Cputime(tt);
 end for;
end for;
n:=ns[1];q:=qs[1];killpol:=Parent(CharacteristicPolynomial(Id))!1;
PrintFile(Out,Sprintf("%o %o %o %o %o %o %o",p,ind,n,r,Nrows(rows),Ncols(rows),d):Overwrite:=true);
for row in Rows(rows) do PrintFile(Out,&cat[IntegerToString(Integers()!a):a in Eltseq(row)]);end for;
printf "DECIC_FI_EXPORT p=%o index=%o Tn=%o q=%o cusp_generator=%o genus=%o rows=%o rank=%o killpoly=%o elapsed=%o\n",p,ind,n,q,r,Dimension(S),Nrows(rows),Rank(rows),killpol,Cputime(tt);
print "DECIC_FI_EXPORT_COMPLETE";quit;
