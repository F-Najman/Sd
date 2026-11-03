from pathlib import Path
import subprocess,concurrent.futures,json,sys
W=Path(__file__).resolve().parent;H=W/'full127'
sys.path.insert(0,str(W));from unit_arithmetic import lit
rs=lit((W/'sources127.m').read_text().replace('true','True').replace('false','False'),'AuditSources');n=len(rs)
def one(a):
 b=min(a+24,n);log=H/f'chunk_{a}.log'
 with log.open('w')as f:r=subprocess.run(['magma','-b',f'Start:={a}',f'End:={b}',str(H/'stage2_chunk.m')],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();ok='AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(x in s for x in['Runtime error','User error','Assertion failed']);print('S17_CHUNK127',a,b,ok,flush=True);assert ok
 return a
with concurrent.futures.ThreadPoolExecutor(max_workers=12)as ex:done=list(ex.map(one,range(1,n+1,25)))
meta=[];records=[];hecke=[]
for a in sorted(done):
 s=(H/f'hecke_jets_{a}.m').read_text();meta+=lit(s,'SourceMetadata');records+=lit(s,'SourceRecords');hecke+=lit(s,'SourceHeckeRecords')
# Preserve Magma's heterogeneous-sequence syntax from each chunk.
parts=[]
for name in ['SourceMetadata','SourceRecords','SourceHeckeRecords']:
 pieces=[]
 for a in sorted(done):
  t=(H/f'hecke_jets_{a}.m').read_text();v=t.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');pieces.append(v[2:-2].strip())
 parts.append(name+':=[*'+','.join(v for v in pieces if v)+'*];')
(H/'hecke_jets.m').write_text('\n'.join(parts)+'\n');assert len(meta)==sum(bool(r[6])for r in rs);assert len(records)==len(meta)==len(hecke)
print('S17_ALL_127_CHUNKS_COMPLETE',len(meta),flush=True)
with(H/'sieve.log').open('w')as f:subprocess.run(['python',str(W/'full_sieve.py'),'127'],stdout=f,stderr=subprocess.STDOUT,check=True)
