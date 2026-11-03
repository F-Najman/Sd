SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);SetSeed(20261028);
p:=StringToInteger(P);ind:=StringToInteger(Ind);n:=StringToInteger(Tn);q:=StringToInteger(Q);d:=13;tt:=Cputime();
h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);

S:=ModularSymbolsH(p,[h],2,-1);Id:=IntegralHeckeOperator(S,1);
function Dia(q)
 op:=IntegralHeckeOperator(S,q)^2-IntegralHeckeOperator(S,q^2);
 return ChangeRing((1/q)*ChangeRing(op,Rationals()),Integers());
end function;
r:=1;repeat r:=NextPrime(r);until Order(GF(p)!r)eq p-1;
dia:=ChangeRing(Dia(r),GF(2));assert dia^ind eq Parent(dia)!1;
// Table 2 proves p=107 non-strange, so (diamond(r)-1)J(Q) is finite.
assert p in [107,109,113];
t:=(dia-Parent(dia)!1)*ChangeRing(IntegralHeckeOperator(S,q)-q*Id-Dia(q),GF(2));
killpol:=PolynomialRing(Integers())!1;
hecke:=[ChangeRing(IntegralHeckeOperator(S,j),GF(2)):j in [1..d]];
prods:=[[t*dia^k*T:T in hecke[1..k eq 0 select d else (d div 2)]]:k in [0..ind-1]];
rows:=Matrix([Eltseq(z):z in &cat prods]);
PrintFile(Out,Sprintf("%o %o %o %o %o %o %o",p,ind,n,r,Nrows(rows),Ncols(rows),d):Overwrite:=true);
for row in Rows(rows) do PrintFile(Out,&cat[IntegerToString(Integers()!a):a in Eltseq(row)]);end for;
printf "DECIC_FI_EXPORT p=%o index=%o Tn=%o q=%o cusp_generator=%o genus=%o rows=%o rank=%o killpoly=%o elapsed=%o\n",p,ind,n,q,r,Dimension(S),Nrows(rows),Rank(rows),killpol,Cputime(tt);
print "DECIC_FI_EXPORT_COMPLETE";quit;
