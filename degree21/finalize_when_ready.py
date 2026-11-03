"""Wait for complete certificates, then run all final proof guards in order."""
from pathlib import Path
import time,json,subprocess
W=Path(__file__).resolve().parent
required=['new_ordinary_job_results.json','new_ordinary_sieve_jobs.json','independent_rank_checks.json','ss_jets_independent.json','large_verified.json','independent_sequence_results.json']
while not all((W/f).exists()for f in required):time.sleep(20)
for f in required:
 a=json.loads((W/f).read_text())
 if isinstance(a,dict):assert a['status']=='PASS',f
 else:assert all(r['status']=='PASS'for r in a),f
for script,engine in[('verify_coverage.py','sage'),('package_result.py','python3'),('build_manifest.py','python3'),('verify_manifest.py','python3')]:
 with(W/(script[:-3]+'.log')).open('w')as out:r=subprocess.run([engine,str(W/script)],stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,script
 print('S21_FINAL_STAGE_PASS',script,flush=True)
print('S21_ALL_PROOF_OUTPUTS_AND_MANIFEST_VERIFIED',flush=True)
