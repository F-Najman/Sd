SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
p:=StringToInteger(P);hh:=StringToInteger(H);ssdeg:=StringToInteger(SSDegree);
load "work/degree22/full73/units_data.m";load "work/degree22/sources73.m";
g:=genus;D:=DiamondMatrix;m:=DiamondOrder;cut:=(p^2-1)div 12;C:=Submatrix(qcoeffs,1,1,g,cut+1);assert Rank(C)eq g;
logh:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[hh,p-hh]]);dh:=D^logh;
AA:=[];
for q in[2,3,5,7]do
 qc:=Min(cut,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,qc+1);if Rank(C)lt g then continue;end if;
 log:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[q,p-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..qc]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;
 A:=(dh-IdentityMatrix(GF(2),g))*(T-D^log-(GF(2)!q)*IdentityMatrix(GF(2),g));assert A*D eq D*A;Append(~AA,A);
end for;assert #AA gt 0;
load "work/degree21/ss73/hecke_jets.m";rec:=SourceRecords[1];PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[1]>;assert Degree(F)eq 6;PS<u>:=PowerSeriesRing(F,3);
z:=[PS![F!PF!rec[6][3][i][j]:j in[1..3]]:i in[1..g]];assert &or[Coefficient(v,1)ne 0:v in z];SSJ:=[**];
for k in[0..3]do
 zk:=Vector(PS,z)*Transpose(ChangeRing(D^k,PS));ki:=Min([i:i in[1..g]|Valuation(zk[i])eq 0]);den:=zk[ki];zk:=Vector(PS,[v/den:v in Eltseq(zk)]);B:=ZeroMatrix(GF(2),0,18);
 for A in AA do
  vv:=zk*Transpose(ChangeRing(A,PS));B:=VerticalJoin(B,Matrix(GF(2),[&cat[Eltseq(Coefficient(vv[i],j),GF(2)):j in[0..2]]:i in[1..g]]));
 end for;Append(~SSJ,[Eltseq(v):v in Rows(B)]);
end for;
load "work/degree22/relative73_data.m";RC:=RelativeCuspJets;
load "work/degree22/relative73_nc_data.m";NC:=RelativeSSMatrices;assert &and[#r eq 9:r in NC[1]]and #NC[1]eq #SSJ[1];
PrintFile("work/degree22/relative73_multiple_data.m",Sprintf("SS73ClosedJets:=%o;SS73NC:=%o;SS73CuspJets:=%o;",SSJ,NC,RC):Overwrite:=true);
print "S22_SS73_MULTIPLE_COTANGENTS_EXPORTED";quit;
