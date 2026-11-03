SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();p:=StringToInteger(P);
load "work/degree21/full71/units_data.m";
g:=genus;D:=DiamondMatrix;m:=DiamondOrder;I:=IdentityMatrix(GF(2),g);AA:=[* *];qs:=[];alpha:=p eq 71 select I else D-I;
for q in[2,3,5,7]do
 cut:=Min((p^2-1)div 12,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,cut+1);if Rank(C)lt g then continue;end if;
 log:=Min([k:k in[0..m-1]|DiamondRoot^k mod p in[q,p-q]]);DQ:=D^log*qcoeffs;TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;Append(~AA,alpha*(T-D^log-(GF(2)!q)*I));Append(~qs,q);
end for;JC:=[**];
for k in[0..m-1]do
 M:=ZeroMatrix(GF(2),0,21);for A in AA do M:=VerticalJoin(M,A*D^k*Submatrix(qcoeffs,1,2,g,21));end for;Append(~JC,[Eltseq(v):v in Rows(M)]);
end for;
PrintFile(Sprintf("work/degree21/full_cusps%o_data.m",p),Sprintf("RelativeSSMatrices:=[* *];RelativeCuspJets:=%o;RelativeHeckePrimes:=%o;",JC,qs):Overwrite:=true);print "S21_FULL_CUSPS_EXTRA_EXPORTED",p,qs,Cputime(tt);quit;
