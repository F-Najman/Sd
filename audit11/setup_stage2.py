from pathlib import Path
import re
W=Path(__file__).resolve().parent;B=W.parents[1];L=Path('/home/fnajman/degree9_torsion/nonic-torsion')
s=(B/'work/degree11/P61_full/canonical_units/stage2.m').read_text();s=s[:s.index('F<a>:=GF(2^11);')]
s=s.replace('AttachSpec("mdmagma/v2/mdmagma.spec");Attach("common/fast_hecke.m");',f'AttachSpec("{L}/mdmagma/v2/mdmagma.spec");')
s=re.sub(r'load ".*stage1_data.m";', 'load MODELFILE;',s)
s=s.replace('function Code(z)return [Integers()!a:a in Eltseq(z,GF(2))];end function;', 'function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;')
s=s.replace('Psi61','PsiN').replace('61*','N*').replace('[5..61]','[5..N]').replace('pp[62]','pp[N+1]')
s=re.sub(r'\b126\b','g',s);s=re.sub(r'\b125\b','g-1',s)
s=s.replace('PowerSeriesRing(F,5)','PowerSeriesRing(F,8)').replace('[1..4]','[1..7]').replace('[0..4]','[0..7]')
s+='''
load SOURCEFILE;assert AuditN eq N;
SourceRecords:=[**];SourceHeckeRecords:=[**];SourceMetadata:=[**];
for si in[1..#AuditSources]do
 rec:=AuditSources[si];if not rec[7]then continue;end if;
 PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];assert N*P eq E!0 and P ne E!0;
 E,P:=SimplifyPoint(E,P);sr,sd:=RecordPoint(E,P);d:=rec[1];assert sd eq d;Append(~SourceRecords,sr);Append(~SourceMetadata,<si,d,rec[6],rec[5]>);
 fq:=DivisionPolynomial(E,3);fac:=Factorization(fq);assert Degree(fq)eq 4 and IsSquarefree(fq)and &+[Degree(a[1]):a in fac]eq 4;
 trs:=[**];for ff in fac do
  h:=ff[1];e:=Degree(h);if e eq 1 then L:=F;xx:=-Coefficient(h,0)/Coefficient(h,1);else L:=ext<F|h>;xx:=L.1;end if;
  EL:=EllipticCurve([L!a:a in aInvariants(E)]);PL:=EL![L!P[1],L!P[2]];PX<X>:=PolynomialRing(L);ET,phi:=IsogenyFromKernel(EL,X-xx);PT:=phi(PL);assert N*PT eq ET!0 and PT ne ET!0;
  tr,td:=RecordPoint(ET,PT);assert (d*e)mod td eq 0;Append(~trs,<e,td,d*e div td,tr>);
 end for;assert &+[r[2]*r[3]:r in trs]eq 4*d;Append(~SourceHeckeRecords,trs);
 printf "AUDIT_ACTUAL_HECKE_JETS_SOURCE N=%o source=%o degree=%o orbit=%o target_degrees=%o weights=%o elapsed=%o\\n",N,si,d,rec[6],[r[2]:r in trs],[r[3]:r in trs],Cputime(tt);
end for;
PrintFile(OUTPUTFILE,Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",SourceMetadata,SourceRecords,SourceHeckeRecords):Overwrite:=true);
printf "AUDIT_ACTUAL_HECKE_JETS_COMPLETE N=%o sources=%o elapsed=%o\\n",N,#SourceRecords,Cputime(tt);quit;
'''
for N in[37,41,43,47,53,59,61,67,71,73,79,83,89]:
 H=W/f'full{N}';ss=s.replace('MODELFILE','"'+str(H/'units_data.m')+'"').replace('SOURCEFILE','"'+str(W/f'sources{N}.m')+'"').replace('OUTPUTFILE','"'+str(H/'hecke_jets.m')+'"');ss=ss.replace('function Code(z)', 'g:=genus;\nfunction Code(z)',1);(H/'stage2.m').write_text(ss)
