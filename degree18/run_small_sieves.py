from pathlib import Path
import subprocess,concurrent.futures,time,json
W=Path(__file__).resolve().parent
jobs=[('pair',n)for n in[47,53,59,61,67,71,73,79,83,89,127]]+[('mixed',n)for n in[73,113,127]]
def one(job):
 kind,n=job;H=W/f'full{n}'
 while not(H/'export_small.log').exists()or'S18_SMALL_HEKKE_EXPORT_COMPLETE'not in(H/'export_small.log').read_text():time.sleep(5)
 with(H/f'{kind}_sieve.log').open('w')as f:r=subprocess.run(['python',str(W/f'{kind}_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 ok=r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in(H/f'{kind}_sieve.log').read_text();print('S18_SMALL_SIEVE',kind,n,ok,flush=True);return {'kind':kind,'N':n,'status':'PASS'if ok else'FAILED'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:rs=list(ex.map(one,jobs))
(W/'small_sieve_jobs.json').write_text(json.dumps(rs,indent=2)+'\n')
