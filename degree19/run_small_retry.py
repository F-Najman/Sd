from pathlib import Path
import concurrent.futures,subprocess,json
W=Path(__file__).resolve().parent
jobs=[('pair',n)for n in [113,127,131]]
def one(j):
 kind,n=j;H=W/f'full{n}';log=H/f'{kind}_sieve.log'
 with log.open('w')as o:r=subprocess.run(['python3',str(W/f'{kind}_sieve.py'),str(n)],stdout=o,stderr=subprocess.STDOUT)
 ok=r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in log.read_text();print('S19_SMALL_SIEVE',kind,n,ok,flush=True);return {'kind':kind,'N':n,'status':'PASS'if ok else'FAIL'}
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:rs=list(ex.map(one,jobs))
(W/'small_sieve_retry_jobs.json').write_text(json.dumps(rs,indent=2)+'\n')
