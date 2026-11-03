SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree22/full97/units_data.m";assert N eq 97 and genus eq 345 and precision eq 1768;OldQ:=qcoeffs;QPrec:=3500;
M:=CuspidalSubspace(ModularSymbolsH(97,[1],2,1));assert Dimension(M)eq genus;parts:=NewformDecomposition(M);
function Flat(z)
 if Type(z)eq FldRatElt or Type(z)eq RngIntElt then return [Rationals()|z];end if;return &cat[Flat(a):a in Eltseq(z)];
end function;
qs:=[];
for A in parts do
 ff:=qEigenform(A,QPrec);K:=BaseRing(Parent(ff));cc:=[Flat(K!Coefficient(ff,n)):n in[0..QPrec-1]];dim:=#cc[1];assert &and[#v eq dim:v in cc];for j in[1..dim]do Append(~qs,[c[j]:c in cc]);end for;
 printf "S22_EXTEND97_EIGENFORM dimension=%o accumulated=%o elapsed=%o\n",Dimension(A),#qs,Cputime(tt);
end for;
Q0:=Matrix(Rationals(),qs);assert Nrows(Q0)eq genus;den:=LCM([Denominator(v):v in Eltseq(Q0)]);ZQ:=Saturation(ChangeRing(den*Q0,Integers()));assert Nrows(ZQ)eq genus and RowSpace(ChangeRing(ZQ,Rationals()))eq RowSpace(Q0);
Q2:=ChangeRing(ZQ,GF(2));assert Rank(Q2)eq genus;C:=Submatrix(Q2,1,1,genus,precision);assert Rank(C)eq genus;T:=Solution(C,OldQ);assert T*C eq OldQ;NewQ:=T*Q2;assert Submatrix(NewQ,1,1,genus,precision)eq OldQ;
PrintFile("work/degree22/full97/units_data_extended.m",Sprintf("N:=%o;genus:=%o;precision:=%o;DiamondRoot:=%o;DiamondOrder:=%o;PoleBoundX:=%o;PoleBoundY:=%o;SturmWeight2:=%o;SturmWeight4:=%o;qcoeffs:=Matrix(GF(2),%o,%o,%o);DiamondMatrix:=Matrix(GF(2),%o,%o,%o);UnitXRelations:=Matrix(GF(2),%o,%o,%o);UnitYRelations:=Matrix(GF(2),%o,%o,%o);",N,genus,QPrec,DiamondRoot,DiamondOrder,PoleBoundX,PoleBoundY,SturmWeight2,SturmWeight4,genus,QPrec,Eltseq(NewQ),genus,genus,Eltseq(DiamondMatrix),Nrows(UnitXRelations),2*genus,Eltseq(UnitXRelations),Nrows(UnitYRelations),2*genus,Eltseq(UnitYRelations)):Overwrite:=true);
PrintFile("work/degree22/extended97_basis_data.m",Sprintf("Extended97SaturatedQ:=%o;Extended97ChangeOfBasis:=%o;",[Eltseq(v):v in Rows(Q2)],[Eltseq(v):v in Rows(T)]):Overwrite:=true);
printf "S22_EXTENDED97_BASIS_COMPLETE genus345 oldprecision1768 newprecision3500 elapsed=%o\n",Cputime(tt);quit;
