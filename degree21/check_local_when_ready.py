from pathlib import Path
import time,subprocess
W=Path(__file__).resolve().parent
while not(W/'independent_rank_checks.json').exists():time.sleep(20)
with(W/'verify_local_coverage.log').open('w')as f:r=subprocess.run(['sage',str(W/'verify_coverage.py'),'--local-only'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
print('S21_LOCAL_COVERAGE_COMPLETE_PENDING_GLOBAL_CHARACTERS',flush=True)
