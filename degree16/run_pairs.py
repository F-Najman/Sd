from pathlib import Path
import subprocess,concurrent.futures
W=Path(__file__).resolve().parent
ns=[41,43,47,59,61,67,71,113]
def one(n):
 with(W/f'full{n}/pair_sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'pair_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('PAIR16',n,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:list(ex.map(one,ns))
