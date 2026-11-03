SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
p:=StringToInteger(P);hh:=StringToInteger(H);ssdeg:=StringToInteger(SSDegree);
load "work/degree20/full73/units_data.m";load "work/degree20/sources73.m";
g:=genus;D:=DiamondMatrix;m:=DiamondOrder;cut:=(p^2-1)div 12;C:=Submatrix(qcoeffs,1,1,g,cut+1);assert Rank(C)eq g;
logh:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[hh,p-hh]]);dh:=D^logh;
AA:=[];
for q in[3,5,7]do
 qc:=Min(cut,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,qc+1);if Rank(C)lt g then continue;end if;
 log:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[q,p-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select DQ[i,n div q+1]else 0):n in[0..qc]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;
 A:=(dh-IdentityMatrix(GF(2),g))*(T-D^log-IdentityMatrix(GF(2),g));assert A*D eq D*A;Append(~AA,A);
end for;assert #AA gt 0;
function UnitValues(aa,xx,yy)
 a1,a2,a3,a4,a6:=Explode(aa);aa3:=2*yy+a3+a1*xx;aa2:=3*xx+a2;aa4:=3*xx^2+2*xx*a2+a4-a1*yy;aaa1:=2*aa4/aa3+a1;aaa2:=aa2-(aa4/aa3)^2-a1*aa4/aa3;b:=-aaa2^3/aa3^2;c:=-(aaa1*aaa2-aa3)/aa3;r:=b/c;s:=c^2/(b-c);t:=r*s-2*r+1;return[(s-r)/t,t/(s^2-s-r+1)];
end function;
F<a>:=GF(2^9);zz:=a^ExactQuotient(#F-1,73);assert Order(zz)eq 73;
xy:=UnitValues([F!1,F!0,F!0,F!0,F!0],zz/(1+zz)^2,zz^2/(1+zz)^3);
RM:=VerticalJoin(Matrix(F,[[F!v[i]+xy[1]*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+xy[2]*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));assert Rank(RM)eq g-1;
z:=Basis(Kernel(Transpose(RM)))[1];z:=z/z[Min([i:i in[1..g]|z[i]ne 0])];SSM:=[**];
for k in[0..3]do
 zk:=z*Transpose(ChangeRing(D^k,F));B:=ZeroMatrix(GF(2),0,9);
 for A in AA do v:=zk*Transpose(ChangeRing(A,F));B:=VerticalJoin(B,Matrix(GF(2),[Eltseq(v[i],GF(2)):i in[1..g]]));end for;
 assert Rank(B)eq 8;Append(~SSM,[Eltseq(v):v in Rows(B)]);
end for;
JC:=[**];c:=11;
for k in[0..m-1]do
 jets:=ZeroMatrix(GF(2),0,c);
 for A in AA do J:=Matrix(GF(2),[[&+[A[i,j]*qcoeffs[j,n+1]:j in[1..g]]:n in[1..c]]:i in[1..g]]);J:=D^k*J;jets:=VerticalJoin(jets,J);end for;
 Append(~JC,[Eltseq(v):v in Rows(jets)]);
end for;
PrintFile(Sprintf("work/degree20/relative%o_nc_data.m",p),Sprintf("RelativeSSPrime:=%o;RelativeSSDegree:=%o;RelativeSSMatrices:=%o;RelativeCuspJets:=%o;",p,ssdeg,SSM,JC):Overwrite:=true);
PrintFile("work/degree20/relative73_nc_data.m",Sprintf("RelativeNCPolynomial:=%o;RelativeNCZeta:=%o;RelativeNCZ:=%o;",[Integers()!a:a in Eltseq(DefiningPolynomial(F,GF(2)))],[Integers()!a:a in Eltseq(zz,GF(2))],[[Integers()!a:a in Eltseq(v,GF(2))]:v in Eltseq(z)]));
printf "S20_RELATIVE_SS_COTANGENT_EXPORT_COMPLETE p=%o operators=%o elapsed=%o\n",p,#AA,Cputime(tt);quit;
