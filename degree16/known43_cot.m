SetQuitOnError(true);SetColumns(0);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree16/full43/units_data.m";load "work/degree16/full43/hecke_jets.m";
D:=DiamondMatrix;g:=genus;cut:=(43^2-1)div 12;C:=Submatrix(qcoeffs,1,1,g,cut+1);assert Rank(C)eq g;
T2Q:=Submatrix(qcoeffs,1,1,g,cut+1);T2Q:=Matrix(GF(2),[[qcoeffs[i,2*n+1]:n in[0..cut]]:i in[1..g]]);T2:=Solution(C,T2Q);assert T2*C eq T2Q;
AA:=[];for q in[3,5,7]do
 log:=Min([k:k in[0..20]|DiamondRoot^k mod 43 in[q,43-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;A:=T2*(T-D^log-IdentityMatrix(GF(2),g));assert A*D eq D*A;Append(~AA,A);
end for;
Data:=[**];PF:=PolynomialRing(GF(2));
for si in[29,91,207,221]do
 ix:=Index([v[1]:v in SourceMetadata],si);assert ix ne 0;rr:=SourceRecords[ix];F:=ext<GF(2)|PF!rr[1]>;d:=Degree(F);z:=Vector(F,[F!PF!c:c in rr[4]]);B:=ZeroMatrix(GF(2),0,d);JC:=[**];
 for A in AA do
  v:=z*Transpose(ChangeRing(A,F));mat:=Matrix(GF(2),[[GF(2)!c:c in Eltseq(v[i],GF(2))]:i in[1..g]]);B:=VerticalJoin(B,mat);
 end for;
 for k in[0..20]do
  jets:=ZeroMatrix(GF(2),0,4);
  for A in AA do
   cols:=[Transpose(Matrix(Vector(GF(2),[qcoeffs[i,n+1]:i in[1..g]])*Transpose(A*D^k))):n in[1..4]];J:=HorizontalJoin(cols[1],cols[2]);J:=HorizontalJoin(J,cols[3]);J:=HorizontalJoin(J,cols[4]);jets:=VerticalJoin(jets,J);
  end for;Append(~JC,[Eltseq(v):v in Rows(jets)]);
 end for;
 Append(~Data,<si,d,[Eltseq(v):v in Rows(B)],JC>);printf "S16_KNOWN43_COT source=%o point_rank=%o\n",si,Rank(B);
end for;
PrintFile("work/degree16/known43_cot_data.m",Sprintf("Known43CotangentData:=%o;",Data):Overwrite:=true);print "S16_KNOWN43_COT_EXPORT_COMPLETE";quit;
