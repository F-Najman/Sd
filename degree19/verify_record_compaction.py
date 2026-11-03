from pathlib import Path
import json
from unit_arithmetic import lit,decode_record
from compact_records import compact
W=Path(__file__).resolve().parent;s=(W/'full127/hecke_jets_432.m').read_text();count=0
def norm(r):
 a=decode_record(r);return(a['F'].p,a['ainv'],a['point'],a['z'],a['units'],a['xjet'],a['yjet'],a['jets'])
for name in['SourceRecords','SourceHeckeRecords']:
 v=s.split(name+':=',1)[1].split(';',1)[0];a=lit(s,name);b=lit(name+':='+compact(v)+';',name)
 if name=='SourceRecords':assert[norm(z)for z in a]==[norm(z)for z in b];count+=len(a)
 else:
  assert[[(e,d,m,norm(z))for e,d,m,z in t]for t in a]==[[(e,d,m,norm(z))for e,d,m,z in t]for t in b];count+=sum(len(t)for t in a)
assert count==24
(W/'record_compaction_verified.json').write_text(json.dumps({'status':'PASS','level':127,'exact_source_and_target_records_compared':count},indent=2)+'\n');print('S19_RECORD_COMPACTION_REPLAY_PASS',count,flush=True)
