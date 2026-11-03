SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");p:=StringToInteger(P);
if p eq 97 then sd:=16;c:=4;kh:=16;
else assert p eq 101;sd:=0;c:=20;kh:=1;end if;
load "work/degree20/strange_eigenvalues_data.m";
g:=genus;m:=DiamondOrder;D:=DiamondMatrix;I:=IdentityMatrix(GF(2),g);
function Hecke(q)
 cut:=Min((p^2-1)div 12,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,cut+1);if Rank(C)lt g then return false,ZeroMatrix(GF(2),g,g);end if;
 k:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[q,p-q]]);DQ:=D^k*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;return true,T;
end function;
AA:=[];
for n in[2,3,5,7]do
 ok,T:=Hecke(n);if not ok then continue;end if;cc:=StrangeHeckeEigenvalues[<p,n>];B:=T-&+[MatrixAlgebra(GF(2),g)|(GF(2)!cc[k+1])*D^k:k in[0..#cc-1]];
 for q in[3,5,7]do
  ok,U:=Hecke(q);if not ok then continue;end if;k:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[q,p-q]]);A:=(D^kh-I)*B*(U-D^k-(GF(2)!q)*I);assert A*D eq D*A;Append(~AA,A);printf "S20_SHARP_OPERATOR p=%o n=%o q=%o rank=%o\n",p,n,q,Rank(A);
 end for;
end for;assert #AA gt 0;
SSM:=[**];
if sd ne 0 then
 rr:=Rep([r:r in AuditSources|not r[7]and r[1]eq sd]);PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rr[2]>;E:=EllipticCurve([F!PF!a:a in rr[3]]);PP:=E![F!PF!a:a in rr[4]];xy:=TateNormalForm_xy(E,PP);
 RM:=VerticalJoin(ChangeRing(Submatrix(UnitXRelations,1,1,Nrows(UnitXRelations),g),F)+xy[1]*ChangeRing(Submatrix(UnitXRelations,1,g+1,Nrows(UnitXRelations),g),F),ChangeRing(Submatrix(UnitYRelations,1,1,Nrows(UnitYRelations),g),F)+xy[2]*ChangeRing(Submatrix(UnitYRelations,1,g+1,Nrows(UnitYRelations),g),F));assert Rank(RM)eq g-1;z:=Basis(Kernel(Transpose(RM)))[1];z:=z/z[Min([k:k in[1..g]|z[k]ne 0])];
 for k in[0..rr[6]-1]do
  zk:=z*Transpose(ChangeRing(D^k,F));B:=ZeroMatrix(GF(2),0,sd);
  for A in AA do v:=zk*Transpose(ChangeRing(A,F));B:=VerticalJoin(B,Matrix(GF(2),[Eltseq(v[i],GF(2)):i in[1..g]]));end for;
  Append(~SSM,[Eltseq(v):v in Rows(B)]);printf "S20_SHARP_SS_RANK p=%o translate=%o rank=%o\n",p,k,Rank(B);
 end for;
end if;
CJ:=[**];for k in[0..m-1]do
 B:=ZeroMatrix(GF(2),0,c);for A in AA do B:=VerticalJoin(B,A*D^k*Submatrix(qcoeffs,1,2,g,c));end for;Append(~CJ,[Eltseq(v):v in Rows(B)]);
end for;
PrintFile("work/degree20/"cat Stem cat"_data.m",Sprintf("RelativeSSPrime:=%o;RelativeSSDegree:=%o;RelativeSSMatrices:=%o;RelativeCuspJets:=%o;",p,sd,SSM,CJ):Overwrite:=true);
print "S20_SHARP_COTANGENT_EXPORT_COMPLETE",p,Cputime(tt);quit;
