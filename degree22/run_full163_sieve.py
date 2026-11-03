from pathlib import Path
import json,time,subprocess
W=Path(__file__).resolve().parent;H=W/'full163';p=W/'ordinary163_job_results.json'
while not p.exists()or'S22_ALL_163_ORDINARY_JETS_COMPLETE'not in(W/'run_ordinary163.log').read_text():time.sleep(20)
a=json.loads(p.read_text());assert all(v['status']=='PASS'for v in a)
assert'S22_ALL_163_ORDINARY_JETS_COMPLETE'in(W/'run_ordinary163.log').read_text()
with(H/'sieve.log').open('w')as f:r=subprocess.run(['sage',str(W/'full_sieve.py'),'163'],stdout=f,stderr=subprocess.STDOUT)
s=(H/'sieve.log').read_text();assert r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in s,s[-2000:];a=json.loads((H/'sieve.json').read_text());print('S22_FULL163_SIEVE_FINISHED',a['status'],'exceptions',[(v['source'],v['degree'],v['status'])for v in a['exceptions']],flush=True)
