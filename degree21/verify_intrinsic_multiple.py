from pathlib import Path
import json
from sage.all import GF,matrix,PolynomialRing,PowerSeriesRing,ZZ
from intrinsic_model import Model,stack,coeff
from unit_arithmetic import lit,decode_record
from compact_records import compact
W=Path(__file__).resolve().parent;M=Model(73);s=(W/'relative73_multiple_data.m').read_text();raw=compact((W/'ss73/hecke_jets.m').read_text());r=decode_record(lit(raw,'SourceRecords')[0]);PR=PolynomialRing(GF(2),'t');F=GF(2**r['F'].d,'a',modulus=PR(ZZ(r['F'].p).digits(2)));cv=lambda z:F(PR(ZZ(z).digits(2)));Z=matrix(F,[[cv(v)for v in row[:3]]for row in r['jets']]);PS=PowerSeriesRing(F,'u',default_prec=3);AA=M.operators(2,[2,3,5,7]);SS=lit(s,'SS73ClosedJets')
for k in range(4):
 Zk=M.D.change_ring(F)**k*Z;ki=next(i for i in range(M.g)if Zk[i,0]);den=PS(list(Zk.row(ki)));rows=[]
 for A in AA:
  AZ=A.change_ring(F)*Zk
  for row in AZ.rows():
   v=PS(list(row))/den;rows.append([v[j]._vector_()[h]for j in range(3)for h in range(6)])
 assert matrix(GF(2),rows)==matrix(GF(2),SS[k])
assert lit(s,'SS73NC')==lit((W/'relative73_nc_data.m').read_text(),'RelativeSSMatrices')
assert lit(s,'SS73CuspJets')==lit((W/'relative73_data.m').read_text(),'RelativeCuspJets')
(W/'intrinsic_multiple_independent.json').write_text(json.dumps({'status':'PASS','all_entries_rebuilt':True,'SS_translates':4,'SS_jet_precision':3,'SS_NC_positions':16,'double_SS_positions':10},indent=2)+'\n');print('S21_INTRINSIC_MULTIPLE_COMPLETE',flush=True)
