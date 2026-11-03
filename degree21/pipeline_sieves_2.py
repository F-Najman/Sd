from pathlib import Path
import sys,json,time,subprocess,concurrent.futures
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit

while not(W/'new_ordinary_jobs.json').exists():time.sleep(5)
jobs=json.loads((W/'new_ordinary_jobs.json').read_text());pending=sorted(set(j['N']for j in jobs));futures={};tt=time.monotonic()
def merge(n):
 H=W/f'full{n}';js=sorted([j for j in jobs if j['N']==n],key=lambda j:j['start']);parts=[]
 for name in ['SourceMetadata','SourceRecords','SourceHeckeRecords']:
  pieces=[]
  for j in js:
   s=(H/f"hecke_jets_{j['start']}.m").read_text();v=s.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');pieces.append(v[2:-2].strip())
  parts.append(name+':=[*'+','.join(v for v in pieces if v)+'*];')
 text='\n'.join(parts)+'\n';meta=lit(text,'SourceMetadata');src=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');expected=[(i+1,r[0],r[5],r[4])for i,r in enumerate(src)if r[6]and (r[0]in[20,21]if n==61 else r[0]==21)];assert sorted(meta)==sorted(expected)
 (H/'hecke_jets.m').write_text(text)
def run(n):
 H=W/f'full{n}'
 if(H/'sieve.json').exists()and(H/'sieve.log').exists()and'AUDIT_FULL_SIEVE_COMPLETE'in(H/'sieve.log').read_text():
  a=json.loads((H/'sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions'],(n,a['exceptions']);print('S21_SIEVE_REUSED_COMPLETE',n,flush=True);return{'N':n,'status':'PASS'}
 merge(n);print('S21_SIEVE_STARTED',n,round(time.monotonic()-tt,1),flush=True)
 with(H/'sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'full_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 s=(H/'sieve.log').read_text();ok=r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in s;print('S21_SIEVE_FINISHED',n,ok,round(time.monotonic()-tt,1),flush=True);return {'N':n,'status':'PASS'if ok else'FAILED'}
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:
 while pending:
  for n in pending[:]:
   js=[j for j in jobs if j['N']==n];H=W/f'full{n}'
   if all((H/f"chunk_{j['start']}.log").exists()and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in(H/f"chunk_{j['start']}.log").read_text()for j in js):futures[n]=ex.submit(run,n);pending.remove(n)
  if pending:time.sleep(10)
 results=[f.result()for f in futures.values()]
(W/'new_ordinary_sieve_jobs.json').write_text(json.dumps(results,indent=2)+'\n');print('S21_ALL_NEW_ORDINARY_SIEVES_COMPLETE',results,flush=True)
