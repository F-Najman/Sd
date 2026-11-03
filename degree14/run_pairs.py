from pathlib import Path
import subprocess,time,concurrent.futures
W=Path(__file__).resolve().parent

def one(n):
 p=W/f'full{n}/hecke_jets.m'
 while not p.exists():time.sleep(1)
 with(W/f'full{n}/pair_sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'pair_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S14_PAIRS',n,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:list(ex.map(one,[59,61,67,71,73]))
with(W/'full73/mixed_sieve.log').open('w')as f:subprocess.run(['python',str(W/'mixed_sieve.py'),'73'],stdout=f,stderr=subprocess.STDOUT,check=True)
