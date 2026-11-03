from pathlib import Path
import subprocess,concurrent.futures,time,json
W=Path(__file__).resolve().parent
ns=[41, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
def one(n):
 H=W/f'full{n}';t=time.monotonic()
 with(H/'stage2.log').open('w')as f:r=subprocess.run(['magma','-b',str(H/'stage2.m')],stdout=f,stderr=subprocess.STDOUT)
 s=(H/'stage2.log').read_text();ok='AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(x in s for x in['User error','Runtime error','Assertion failed']);print('S13_ORDINARY_JETS',n,ok,round(time.monotonic()-t,1),flush=True)
 if ok:
  with(H/'sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'full_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
  ok=(H/'sieve.json').exists();print('S13_ORDINARY_SIEVE',n,ok,round(time.monotonic()-t,1),flush=True)
 return {'N':n,'export_ok':ok}
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as ex:rs=list(ex.map(one,ns))
(W/'ordinary_jobs.json').write_text(json.dumps(rs,indent=2)+'\n')
