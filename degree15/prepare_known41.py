from pathlib import Path
import json
W=Path(__file__).resolve().parent;dat=next(v for v in json.load(open(W.parent/'degree14/occurrences.json'))if v['N']==41)
def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
s=(W.parent/'degree13/mixed43_lifting.m').read_text().replace(str(W.parent/'degree13'),str(W)).replace('full43','full41').replace('29);assert ix','79);assert ix').replace('Degree(F)eq 12','Degree(F)eq 14')
a=s.index('z:=Vector');b=s.index('assert IsIrreducible(f);',a)
s=s[:a]+'''z:=Vector(F,[F!PF!c:c in rec[4]]);D:=DiamondMatrix;cut:=(41^2-1)div 12;C:=Submatrix(qcoeffs,1,1,genus,cut+1);assert Rank(C)eq genus;AA:=[];
for q in[3,5,7]do
 log:=Min([k:k in[0..19]|DiamondRoot^k mod 41 in[q,41-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..genus]]);T:=Solution(C,TQ);assert T*C eq TQ;A:=T-D^log-IdentityMatrix(GF(2),genus);assert A*D eq D*A;Append(~AA,A);
end for;
'''+f'f:={expr(dat["polynomial"])};\ng:={expr(dat["y_numerator"])};\n'+s[b:]
s=s.replace('#roots eq 12','#roots eq 14').replace('43*PP','41*PP').replace('[1..42]','[1..40]').replace('[0..11]','[0..13]').replace('S13_KNOWN43','S15_KNOWN41').replace('[0..20]','[0..19]').replace('source=29','source=79')
a=s.index('q1:=Vector');s=s[:a]+'''q1:=Vector(GF(2),[qcoeffs[i,2]:i in[1..genus]]);out:="'''+str(W/'known41_tangents.m')+'''";PrintFile(out,"TangentMatrices:=[**];":Overwrite:=true);
for k in[0..19]do
 B:=ZeroMatrix(GF(2),0,15);
 for A in AA do
  v:=z*Transpose(ChangeRing(A,F));mat:=Matrix(GF(2),[[GF(2)!c:c in Eltseq(v[i],GF(2))]:i in[1..genus]]);c:=q1*Transpose(A*D^k);B:=VerticalJoin(B,HorizontalJoin(mat,Transpose(Matrix(c))));
 end for;assert Rank(B)eq 15;printf "S15_KNOWN41_FI cusp=%o rank=%o\\n",k,Rank(B);PrintFile(out,Sprintf("Append(~TangentMatrices,%o);",[Eltseq(v):v in Rows(B)]));
end for;printf "S15_KNOWN41_LIFT_AND_FI_COMPLETE orbit_shift=%o elapsed=%o\\n",foundj,Cputime(tt);quit;
'''
(W/'known41_lifting.m').write_text(s)
