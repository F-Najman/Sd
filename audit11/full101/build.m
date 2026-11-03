// Root-allocated first canonical/unit stage only; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("mdmagma/v2/mdmagma.spec");
N:=101;g:=376;QPrec:=1900;TatePrec:=2500;
DiamondRoot:=1;repeat DiamondRoot:=NextPrime(DiamondRoot);until Order(GF(N)!DiamondRoot)eq N-1;
MS:=CuspidalSubspace(ModularSymbolsH(N,[1],2,1));assert Dimension(MS)eq g;decomp:=NewformDecomposition(MS);
printf "NONIC83_CANONICAL_UNIT_NEWFORMS dimensions=%o time=%o\n",[Dimension(A):A in decomp],Cputime(tt);
function Flat(z)
 if Type(z)eq FldRatElt or Type(z)eq RngIntElt then return [Rationals()|z];end if;return &cat[Flat(y):y in Eltseq(z)];
end function;
Q0:=[];D0:=[];A0:=[];
for A in decomp do
 ff:=qEigenform(A,QPrec);KF:=BaseRing(Parent(ff));chi:=(Coefficient(ff,DiamondRoot)^2-Coefficient(ff,DiamondRoot^2))/DiamondRoot;
 if KF cmpeq Rationals()then
  Append(~Q0,[Rationals()!Coefficient(ff,n):n in[0..QPrec-1]]);Append(~D0,[Rationals()!(chi*Coefficient(ff,n)):n in[0..QPrec-1]]);
 else
  dd:=#Flat(KF!1);cofs:=[Flat(KF!Coefficient(ff,n)):n in[0..QPrec-1]];dcofs:=[Flat(KF!(chi*Coefficient(ff,n))):n in[0..QPrec-1]];
  assert &and[#c eq dd:c in cofs]and &and[#c eq dd:c in dcofs];for k in[1..dd]do Append(~Q0,[c[k]:c in cofs]);Append(~D0,[c[k]:c in dcofs]);end for;
 end if;
if N eq 43 then
  chi11:=(Coefficient(ff,11)^2-Coefficient(ff,121))/11;
  lam:=(chi-1)*(Coefficient(ff,11)-chi11-11);
  ac:=[Flat(KF!(lam*Coefficient(ff,n))):n in[0..QPrec-1]];
  for k in[1..#Flat(KF!1)]do Append(~A0,[a[k]:a in ac]);end for;
 end if;
 printf "NONIC83_CANONICAL_UNIT_EIGENFORM dimension=%o accumulated=%o time=%o\n",Dimension(A),#Q0,Cputime(tt);
end for;
QM0:=Matrix(Rationals(),Q0);DM0:=Matrix(Rationals(),D0);assert Nrows(QM0)eq g;
den:=LCM([Denominator(a):a in Eltseq(QM0)]);QMZ:=Saturation(ChangeRing(den*QM0,Integers()));QMR:=ChangeRing(QMZ,Rationals());assert Nrows(QMZ)eq g and RowSpace(QMR)eq RowSpace(QM0);
Q2:=ChangeRing(QMZ,GF(2));assert Rank(Q2)eq g and Rank(Submatrix(Q2,1,1,g,851))eq g;
TT:=Solution(QM0,QMR);assert TT*QM0 eq QMR;Dfull:=TT*DM0;MdQ:=Solution(QMR,Dfull);assert MdQ*QMR eq Dfull and &and[IsOdd(Denominator(a)):a in Eltseq(MdQ)];Md:=ChangeRing(MdQ,GF(2));assert Md^50 eq IdentityMatrix(GF(2),g)and Md ne IdentityMatrix(GF(2),g);
printf "NONIC83_CANONICAL_UNIT_SATURATED_BASIS rank247=true precision1300=true Sturm_weight2=310 diamond2order41=true time=%o\n",Cputime(tt);
LS<q>:=LaurentSeriesRing(GF(2),TatePrec);xp:=q/(1+q)^2;yp:=q^2/(1+q)^3;s1:=LS!0;a6:=LS!0;
for n in[1..TatePrec div N+1]do
 if N*n+1 lt TatePrec then z:=q^(N*n+1);xp+:=z/(1+z)^2;yp+:=z^2/(1+z)^3;end if;
 if N*n-1 lt TatePrec then w:=q^(N*n-1);xp+:=w/(1+w)^2;yp+:=w/(1+w)^3;end if;
 if N*n lt TatePrec then z:=q^(N*n);s1+:=(GF(2)!n)*z/(1+z);a6+:=(GF(2)!((5*n^3+7*n^5)div 12))*z/(1+z);end if;
end for;
yp+:=s1;a4:=s1;assert Valuation(yp^2+xp*yp+xp^3+a4*xp+a6)ge TatePrec;
// The universal Tate point u=q on E(q^101) has exact order83.
aa4:=xp^2+a4+yp;aaa2:=xp+(aa4/xp)^2+aa4/xp;b:=aaa2^3/xp^2;c:=(aaa2+xp)/xp;r:=b/c;s:=c^2/(b+c);t:=r*s+1;xu:=(s+r)/t;yu:=t/(s^2+s+r+1);
assert AbsolutePrecision(xu)ge QPrec and AbsolutePrecision(yu)ge QPrec and Valuation(xu)ge -95 and Valuation(yu)ge -95;
printf "NONIC83_TATE_UNIT_SERIES valuation_x=%o valuation_y=%o absolute_precision_x=%o absolute_precision_y=%o time=%o\n",Valuation(xu),Valuation(yu),AbsolutePrecision(xu),AbsolutePrecision(yu),Cputime(tt);
Q:=[LS!Eltseq(v)+O(q^QPrec):v in Rows(Q2)];low:=Min(0,Min(Valuation(xu),Valuation(yu))+1);RelPrec:=Min(QPrec,QPrec+Min(Valuation(xu),Valuation(yu)));assert RelPrec-1 gt 890;
function UnitRelations(uu)
 AA:=Matrix(GF(2),[[Coefficient(f,n):n in[low..RelPrec-1]]:f in Q cat[uu*f:f in Q]]);B:=BasisMatrix(Kernel(AA));assert Ncols(B)eq 2*g;
 for row in Rows(B)do assert Valuation(&+[row[i]*Q[i]+row[g+i]*uu*Q[i]:i in[1..g]])ge RelPrec;end for;
 return B;
end function;
RX:=UnitRelations(xu);RY:=UnitRelations(yu);assert Nrows(RX)gt 0 and Nrows(RY)gt 0;
printf "NONIC83_CANONICAL_UNIT_RELATIONS x=%o y=%o exact_global_order_lower_bound=%o section_degree_bounds=[884,890] time=%o\n",Nrows(RX),Nrows(RY),RelPrec-1,Cputime(tt);

function TateUnits(k)
 xx:=q^k/(1+q^k)^2;yy:=q^(2*k)/(1+q^k)^3+s1;
 for n in[1..TatePrec div N+1]do
  if N*n+k lt TatePrec then z:=q^(N*n+k);xx+:=z/(1+z)^2;yy+:=z^2/(1+z)^3;end if;
  if N*n-k lt TatePrec then z:=q^(N*n-k);xx+:=z/(1+z)^2;yy+:=z/(1+z)^3;end if;
 end for;
 assert Valuation(yy^2+xx*yy+xx^3+s1*xx+a6)ge TatePrec;
 aa4:=xx^2+s1+yy;aaa2:=xx+(aa4/xx)^2+aa4/xx;b:=aaa2^3/xx^2;c:=(aaa2+xx)/xx;r:=b/c;s:=c^2/(b+c);t:=r*s+1;
 return(s+r)/t,t/(s^2+s+r+1);
end function;
ux2,uy2:=TateUnits(DiamondRoot);MDinv:=Md^(-1);DQ:=[&+[MDinv[i,j]*Q[j]:j in[1..g]]:i in[1..g]];
for dat in[*<ux2,RX>,<uy2,RY>*]do
 for row in Rows(dat[2])do assert Valuation(&+[row[i]*DQ[i]+row[g+i]*dat[1]*DQ[i]:i in[1..g]])ge QPrec-20-DiamondRoot;end for;
end for;
printf "GLOBAL_POINT_DIAMOND2_INVERSE_CERTIFIED N=%o zero_order1290 pole_bound=%o\n",N,2*g-2+140;


function CodePoly(z)return[Integers()!a:a in Eltseq(z)];end function;
out:="/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/full101/units_data.m";
PrintFile(out,Sprintf("N:=%o;genus:=%o;precision:=%o;DiamondRoot:=%o;DiamondOrder:=%o;PoleBoundX:=%o;PoleBoundY:=%o;SturmWeight2:=%o;SturmWeight4:=%o;qcoeffs:=Matrix(GF(2),%o,%o,%o);DiamondMatrix:=Matrix(GF(2),%o,%o,%o);UnitXRelations:=Matrix(GF(2),%o,%o,%o);UnitYRelations:=Matrix(GF(2),%o,%o,%o);",N,g,QPrec,DiamondRoot,(N-1)div 2,134,140,(N*N-1)div 12,(N*N-1)div 6,g,QPrec,Eltseq(Q2),g,g,Eltseq(Md),Nrows(RX),2*g,Eltseq(RX),Nrows(RY),2*g,Eltseq(RY)):Overwrite:=true);
if N eq 43 then
 AFull:=TT*Matrix(Rationals(),A0);AM:=Solution(QMR,AFull);assert AM*QMR eq AFull and &and[IsOdd(Denominator(a)):a in Eltseq(AM)];
 PrintFile(out,Sprintf("AlphaA11Cotangent:=Matrix(GF(2),%o,%o,%o);",g,g,Eltseq(ChangeRing(AM,GF(2)))));
end if;
printf "AUDIT_FULL_MODEL_COMPLETE N=%o genus=%o primitive=%o precision=%o pole_bounds=%o elapsed=%o\n",N,g,DiamondRoot,QPrec,[134,140],Cputime(tt);quit;
