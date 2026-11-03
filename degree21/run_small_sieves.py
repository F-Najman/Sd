from pathlib import Path
import time,subprocess,json
W=Path(__file__).resolve().parent
while not(W/'small_jet_results.json').exists():time.sleep(5)
assert json.loads((W/'small_jet_results.json').read_text())['status']=='PASS'
sets=json.loads((W/'small_jet_jobs.json').read_text())['degree_sets']
for n in map(int,sets):
 with(W/f'full{n}/pair_sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'pair_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S21_PAIR_TRIPLE_FINISHED',n,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(n)
for n in[73,89,109,113,127]:
 with(W/f'full{n}/mixed_new_sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'mixed_new_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S21_MIXED_NEW_FINISHED',n,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(n)
