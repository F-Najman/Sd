from pathlib import Path
import time,subprocess,concurrent.futures
W=Path(__file__).resolve().parent

def one(n):
 H=W/f'full{n}'
 while not(H/'hecke_jets.m').exists():time.sleep(5)
 with(H/'mixed_sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'mixed_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S17_MIXED_FINISHED',n,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:list(ex.map(one,[73,127]))
