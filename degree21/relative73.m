SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
p:=StringToInteger(P);hh:=StringToInteger(H);ssdeg:=StringToInteger(SSDegree);
load "work/degree21/full73/units_data.m";load "work/degree21/sources73.m";
g:=genus;D:=DiamondMatrix;m:=DiamondOrder;cut:=(p^2-1)div 12;C:=Submatrix(qcoeffs,1,1,g,cut+1);assert Rank(C)eq g;
logh:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[hh,p-hh]]);dh:=D^logh;
AA:=[];
for q in[2,3,5,7]do
 qc:=Min(cut,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,qc+1);if Rank(C)lt g then continue;end if;
 log:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[q,p-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..qc]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;
 A:=(dh-IdentityMatrix(GF(2),g))*(T-D^log-(GF(2)!q)*IdentityMatrix(GF(2),g));assert A*D eq D*A;Append(~AA,A);
end for;assert #AA gt 0;
PF:=PolynomialRing(GF(2));rr:=Rep([r:r in AuditSources|not r[7]and r[1]eq ssdeg]);F:=ext<GF(2)|PF!rr[2]>;E:=EllipticCurve([F!PF!a:a in rr[3]]);P0:=E![F!PF!a:a in rr[4]];xy:=TateNormalForm_xy(E,P0);
RM:=VerticalJoin(Matrix(F,[[F!v[i]+xy[1]*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+xy[2]*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));
printf "S21_RELATIVE_SS_CANONICAL p=%o degree=%o relation_rank=%o expected=%o elapsed=%o\n",p,ssdeg,Rank(RM),g-1,Cputime(tt);assert Rank(RM)eq g-1;
z:=Basis(Kernel(Transpose(RM)))[1];ki:=Min([k:k in[1..g]|z[k]ne 0]);z:=z/z[ki];SSM:=[**];
for k in[0..rr[6]-1]do
 zk:=z*Transpose(ChangeRing(D^k,F));B:=ZeroMatrix(GF(2),0,ssdeg);
 for A in AA do v:=zk*Transpose(ChangeRing(A,F));B:=VerticalJoin(B,Matrix(GF(2),[Eltseq(v[i],GF(2)):i in[1..g]]));end for;
 Append(~SSM,[Eltseq(v):v in Rows(B)]);printf "S21_RELATIVE_SS_RANK p=%o translate=%o rank=%o\n",p,k,Rank(B);
end for;
JC:=[**];c:=21-ssdeg;
for k in[0..m-1]do
 jets:=ZeroMatrix(GF(2),0,c);
 for A in AA do J:=Matrix(GF(2),[[&+[A[i,j]*qcoeffs[j,n+1]:j in[1..g]]:n in[1..c]]:i in[1..g]]);J:=D^k*J;jets:=VerticalJoin(jets,J);end for;
 Append(~JC,[Eltseq(v):v in Rows(jets)]);
end for;
PrintFile(Sprintf("work/degree21/relative%o_data.m",p),Sprintf("RelativeSSPrime:=%o;RelativeSSDegree:=%o;RelativeSSMatrices:=%o;RelativeCuspJets:=%o;",p,ssdeg,SSM,JC):Overwrite:=true);
printf "S21_RELATIVE_SS_COTANGENT_EXPORT_COMPLETE p=%o operators=%o elapsed=%o\n",p,#AA,Cputime(tt);quit;
