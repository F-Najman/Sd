# User-authorized Phi(10) resource allocation; one live launcher per batch.
import fcntl as _phi10_fcntl, sys as _phi10_sys
_phi10_lock = open(str(__file__)+'.phi10-priority.lock','a+')
try:
 _phi10_fcntl.flock(_phi10_lock, _phi10_fcntl.LOCK_EX | _phi10_fcntl.LOCK_NB)
except BlockingIOError:
 print('An existing launcher already owns this batch; no duplicate workers started.',flush=True)
 _phi10_sys.exit(0)
from pathlib import Path
import gzip
def read_native(p):
 try:return p.read_text()
 except FileNotFoundError:
  with gzip.open(p.with_suffix(p.suffix+".gz"),"rt")as f:return f.read()

import subprocess,concurrent.futures,json,time,sys
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit

while not(W/'new_ordinary_jobs.json').exists():time.sleep(5)
jobs=json.loads((W/'new_ordinary_jobs.json').read_text());jobs.sort(key=lambda j:(j['start'],j['N']));tt=time.monotonic()
def one(j):
 n,a,b=j['N'],j['start'],j['end'];H=W/f'full{n}';log=H/f'chunk_{a}.log'
 while not(H/'units_data.m').exists():time.sleep(5)
 if not(log.exists()and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in log.read_text()):
  with log.open('w')as f:r=subprocess.run(['magma','-b',f'Start:={a}',f'End:={b}',str(H/'stage2_chunk.m')],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();ok='AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(e in s for e in['Runtime error','User error','Assertion failed']);print('S22_CHUNK_COMPLETE',n,a,b,ok,'wall',round(time.monotonic()-tt,1),flush=True);return j|{'status':'PASS'if ok else'FAILED'}
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:done=list(ex.map(one,jobs))
(W/'new_ordinary_job_results.json').write_text(json.dumps(done,indent=2)+'\n')
for n in sorted(set(j['N']for j in jobs)):
 H=W/f'full{n}';js=sorted([j for j in done if j['N']==n],key=lambda j:j['start']);assert all(j['status']=='PASS'for j in js)
 parts=[]
 for name in ['SourceMetadata','SourceRecords','SourceHeckeRecords']:
  pieces=[]
  for j in js:
   t=read_native(H/f"hecke_jets_{j['start']}.m");v=t.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');pieces.append(v[2:-2].strip())
  parts.append(name+':=[*'+','.join(v for v in pieces if v)+'*];')
 (H/'hecke_jets.m').write_text('\n'.join(parts)+'\n')
 print('S22_JETS_MERGED',n,len(lit((H/'hecke_jets.m').read_text(),'SourceMetadata')),flush=True)
print('S22_ALL_NEW_ORDINARY_JETS_COMPLETE',flush=True)
