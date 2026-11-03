from pathlib import Path
import subprocess,concurrent.futures,json,time
W=Path(__file__).resolve().parent
Ns=[37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
def run(n):
 t=time.monotonic()
 with(W/f'full{n}/sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'full_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0 and f'AUDIT_FULL_SIEVE_COMPLETE {n} 'in(W/f'full{n}/sieve.log').read_text(),n
 rec={'N':n,'status':'PASS','elapsed':time.monotonic()-t};print(rec,flush=True);return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(run,Ns))
(W/'sieve_results_final.json').write_text(json.dumps(rs,indent=2)+'\n')
