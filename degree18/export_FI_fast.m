SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);SetSeed(20261028);
p:=StringToInteger(P);ind:=StringToInteger(Ind);n:=StringToInteger(Tn);q:=StringToInteger(Q);d:=18;tt:=Cputime();
h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);
M:=ModularSymbolsH(p,[h],2,0);MS:=CuspidalSubspace(M);e:=WindingElementProjection(MS);
S:=ModularSymbolsH(p,[h],2,-1);Id:=IntegralHeckeOperator(S,1);
function Dia(q)
 op:=IntegralHeckeOperator(S,q)^2-IntegralHeckeOperator(S,q^2);
 return ChangeRing((1/q)*ChangeRing(op,Rationals()),Integers());
end function;
function RowEval(v,poly,T)
 w:=Parent(v)!0;
 for j in[Degree(poly)..0 by -1]do w:=w*T+Coefficient(poly,j)*v;end for;
 return w;
end function;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree18/finite_FI_polynomials.m";
TnS:=IntegralHeckeOperator(S,n);
// Every integral polynomial has finite image at these rank-zero levels.
if p in[41,47,59,71]then
 TnMS:=HeckeOperator(MS,n);pol:=CharacteristicPolynomial(TnS);fac:=Factorization(pol);
 flags:=[f[2]ge 2 or IsZero(e*Evaluate(ExactQuotient(pol,f[1]^f[2]),TnMS)):f in fac];
 killpol:=&*[Parent(pol)|fac[i][1]^fac[i][2]:i in[1..#fac]|flags[i]];
else killpol:=FiniteFIPolynomials[<p,n>];end if;
t1:=Evaluate(killpol,TnS);t2:=IntegralHeckeOperator(S,q)-q*Id-Dia(q);t:=ChangeRing(t1*t2,GF(2));
r:=1;repeat r:=NextPrime(r);until Order(GF(p)!r) eq p-1;
dia:=ChangeRing(Dia(r),GF(2));assert dia^ind eq Parent(dia)!1;
hecke:=[ChangeRing(IntegralHeckeOperator(S,j),GF(2)):j in [1..d]];
prods:=[[t*dia^k*T:T in hecke[1..k eq 0 select d else (d div 2)]]:k in [0..ind-1]];
rows:=Matrix([Eltseq(z):z in &cat prods]);
PrintFile(Out,Sprintf("%o %o %o %o %o %o %o",p,ind,n,r,Nrows(rows),Ncols(rows),d):Overwrite:=true);
for row in Rows(rows) do PrintFile(Out,&cat[IntegerToString(Integers()!a):a in Eltseq(row)]);end for;
printf "DECIC_FI_EXPORT p=%o index=%o Tn=%o q=%o cusp_generator=%o genus=%o rows=%o rank=%o killpoly=%o elapsed=%o\n",p,ind,n,q,r,Dimension(S),Nrows(rows),Rank(rows),killpol,Cputime(tt);
print "DECIC_FI_EXPORT_COMPLETE";quit;
