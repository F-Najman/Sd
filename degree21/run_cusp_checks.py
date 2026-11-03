from pathlib import Path
import time,json,subprocess
W=Path(__file__).resolve().parent
while not(W/'fi_exports.json').exists():time.sleep(5)
assert all(a['status']=='PASS'for a in json.loads((W/'fi_exports.json').read_text()))
ns=[59,61,67,71,73,79,83,89,97,103,107,109,113,127,131,137,139]
for n in ns:
 with(W/f'FI/check{n}.log').open('w')as f:r=subprocess.run(['python3',str(W/'check_cusp_profiles.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S21_CUSP_CHECK',n,r.returncode,flush=True)
