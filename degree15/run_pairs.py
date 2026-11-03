from pathlib import Path
import subprocess,concurrent.futures
W=Path(__file__).resolve().parent

def one(n):
 with(W/f'full{n}/pair_sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'pair_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S15_PAIR7_8',n,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:list(ex.map(one,[59,61,67,71]))
