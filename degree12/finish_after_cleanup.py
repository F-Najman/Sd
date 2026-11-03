from pathlib import Path
import json,time,subprocess,sys
W=Path(__file__).resolve().parent
print('FINAL_VERIFICATION_WAITING_FOR_CLEAN_REGENERATION',flush=True)
while not (W/'scheduler_cleanup.json').exists():time.sleep(5)
assert json.loads((W/'scheduler_cleanup.json').read_text())['status']=='PASS'
for script,log in [('verify_large.py','verify_large_final.log'),('verify_coverage.py','verify_coverage_final.log'),('finalize_result.py','finalize_result.log'),('package_result.py','package_result.log')]:
 print('FINAL_STAGE_START',script,flush=True)
 with(W/log).open('w')as out:r=subprocess.run([sys.executable,str(W/script)],stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,(script,(W/log).read_text()[-3000:])
 print('FINAL_STAGE_PASS',script,flush=True)
print('S12_PROOF_AND_PACKET_COMPLETE',flush=True)
