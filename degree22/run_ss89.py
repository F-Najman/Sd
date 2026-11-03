from pathlib import Path
import json,subprocess,shutil
W=Path(__file__).resolve().parent;a=json.loads((W/'ss89_job.json').read_text());ids=a['sources'];H=W/'full89'
with(W/'ss89_native.log').open('w')as out:r=subprocess.run(['magma','-b',f'Start:={min(ids)}',f'End:={max(ids)}',str(H/'stage2_ss.m')],stdout=out,stderr=subprocess.STDOUT)
s=(W/'ss89_native.log').read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(x in s for x in ['Runtime error','User error','Assertion failed'])
shutil.copy2(H/f'ss_jets_{min(ids)}.m',W/'ss89/hecke_jets.m')
with(W/'ss89/sieve.log').open('w')as out:r=subprocess.run(['sage',str(W/'ss_sieve.py'),'89'],stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
print('S22_SS89_COMPUTATION_COMPLETE',json.loads((W/'ss89/sieve.json').read_text())['status'],flush=True)
