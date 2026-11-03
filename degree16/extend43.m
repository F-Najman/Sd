SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();load "work/degree16/full43/units_data.m";OldQ:=qcoeffs;
S:=CuspidalSubspace(ModularSymbolsH(43,[1],2,1));dd:=NewformDecomposition(S);prec:=2000;
function Flat(z)
 if Type(z)eq FldRatElt or Type(z)eq RngIntElt then return[Rationals()|z];end if;return &cat[Flat(y):y in Eltseq(z)];end function;
qs:=[];for A in dd do
 ff:=qEigenform(A,prec);KF:=BaseRing(Parent(ff));cofs:=[Flat(KF!Coefficient(ff,n)):n in[0..prec-1]];d:=#cofs[1];for k in[1..d]do Append(~qs,[c[k]:c in cofs]);end for;
 printf "S16_EXTEND43_EIGENFORM dim=%o elapsed=%o\n",Dimension(A),Cputime(tt);
end for;
M:=Matrix(Rationals(),qs);den:=LCM([Denominator(a):a in Eltseq(M)]);Z:=Saturation(ChangeRing(den*M,Integers()));Q:=ChangeRing(Z,GF(2));assert Rank(Q)eq 57;
Qcut:=Submatrix(Q,1,1,57,Ncols(OldQ));T:=Solution(Qcut,OldQ);assert T*Qcut eq OldQ and Rank(T)eq 57;Q:=T*Q;
PrintFile("work/degree16/full43/qcoeff_high.m",Sprintf("HighPrecision:=2000;HighQ:=Matrix(GF(2),57,2000,%o);",Eltseq(Q)):Overwrite:=true);print "S16_EXTEND43_SAME_BASIS_COMPLETE",Cputime(tt);quit;
