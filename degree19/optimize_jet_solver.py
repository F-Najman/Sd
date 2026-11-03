from pathlib import Path
W=Path(__file__).resolve().parent
for H in W.glob('full*'):
 p=H/'stage2_chunk.m'
 if not p.exists():continue
 s=p.read_text()
 if 'function CanonicalPointFast' in s:continue
 pos=s.index('function PsiN')
 fast='''function CanonicalPointFast(E,P,GoodRows)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);RR:=UnitMatrix(F,xy[1],xy[2]);uk:=[2..g];selected:=GoodRows;ok:=true;
 try LL:=Submatrix(RR,selected,uk)^(-1);catch err ok:=false;end try;
 if ok then
  br:=Vector(F,[RR[r,1]:r in selected]);ur:=br*Transpose(LL);z:=[F!1]cat Eltseq(ur);assert IsZero(Vector(F,z)*Transpose(RR));
 else
  assert Rank(RR)eq g-1;z:=Eltseq(Basis(Kernel(Transpose(RR)))[1]);ki:=Index([a ne 0:a in z],true);z:=[a/z[ki]:a in z];uk:=[i:i in[1..g]|i ne ki];selected:=[1..Nrows(RR)];M0:=Submatrix(RR,selected,uk);LL:=Solution(M0,IdentityMatrix(F,g-1));assert LL*M0 eq IdentityMatrix(F,g-1);
 end if;
 return z,xy,LL,uk,selected;
end function;
'''
 s=s[:pos]+fast+s[pos:]
 s=s.replace('function CanonicalJets(E,P,z0,jprec)','function CanonicalJets(E,P,z0,jprec,LL,uk,selected)')
 old='ki:=Index([z ne 0:z in z0],true);assert z0[ki]eq 1;uk:=[i:i in[1..g]|i ne ki];M0:=Matrix(F,[[RM[1][r,c]:c in uk]:r in[1..Nrows(RM[1])]]);assert Rank(M0)eq g-1;LL:=Solution(M0,IdentityMatrix(F,g-1));assert LL*M0 eq IdentityMatrix(F,g-1);zv:=[Vector(F,z0)];'
 new='ki:=Index([z ne 0:z in z0],true);assert z0[ki]eq 1 and uk eq[i:i in[1..g]|i ne ki];zv:=[Vector(F,z0)];'
 assert old in s;s=s.replace(old,new).replace('1..Nrows(M0)','1..Nrows(RM[1])')
 s=s.replace('ur:=br*Transpose(LL);zz:=','ur:=Vector(F,[br[r]:r in selected])*Transpose(LL);zz:=')
 s=s.replace('function RecordPoint(E,P)','function RecordPoint(E,P,GoodRows)').replace('z,xy:=CanonicalPoint(E,P);','z,xy,LL,uk,selected:=CanonicalPointFast(E,P,GoodRows);').replace('CanonicalJets(E,P,z,jprec)','CanonicalJets(E,P,z,jprec,LL,uk,selected)')
 s=s.replace('sr,sd:=RecordPoint(E,P);','sr,sd:=RecordPoint(E,P,GoodRows);').replace('tr,td:=RecordPoint(ET,PT);','tr,td:=RecordPoint(ET,PT,GoodRows);')
 at=s.index('SourceRecords:=[**];')
 pre='''rr0:=AuditSources[StringToInteger(Start)];PF0:=PolynomialRing(GF(2));F0:=ext<GF(2)|PF0!rr0[2]>;E0:=EllipticCurve([F0!PF0!a:a in rr0[3]]);P0:=E0![F0!PF0!a:a in rr0[4]];xy0:=TateNormalForm_xy(E0,P0);R0:=UnitMatrix(F0,xy0[1],xy0[2]);EF0:=EchelonForm(Transpose(R0));assert IsZero(EF0[g]);GoodRows:=[Min([j:j in[1..Ncols(EF0)]|EF0[i,j]ne 0]):i in[1..g-1]];assert #Seqset(GoodRows)eq g-1;
'''
 s=s[:at]+pre+s[at:];(H/'stage2_fast.m').write_text(s)
H=W/'full127';s=(H/'stage2_fast.m').read_text().replace('/hecke_jets_','/fast_jets_');(H/'fast_test.m').write_text(s)
