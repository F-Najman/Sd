"""Wait for every certificate, then issue and freeze the completed proof."""
from pathlib import Path
import json,time,subprocess,os,sys,psutil,hashlib
W=Path(__file__).resolve().parent
lock=open(W/'finalizer.lock','a+');import fcntl;fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
local_done=False
state=W/'finalizer_status.json'
def status(stage):state.write_text(json.dumps({'stage':stage,'exact_result_issued':(W/'final_coverage.json').exists()},indent=2)+'\n');print('S22_FINALIZER',stage,flush=True)
def run(script,*args):
 log=W/(Path(script).stem+'.log')
 with log.open('w')as f:r=subprocess.run([sys.executable,str(W/script),*args],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(script,log.read_text()[-4000:])
status('WAITING_FOR_CERTIFICATES')
while True:
 cp=subprocess.run([sys.executable,str(W/'verify_final.py'),'--pending'],capture_output=True,text=True);assert cp.returncode==0,cp.stderr
 a=json.loads(cp.stdout);missing=a['missing']
 local_missing=[f for f in missing if f not in ['large_verified.json','independent_sequence_results.json','large_native_results.json']]
 if not local_missing and not local_done:
  status('VERIFYING_COMPLETE_LOCAL_COVERAGE');run('verify_final.py','--local');local_done=True;status('LOCAL_PASS_WAITING_FOR_LARGE_CHARACTERS')
 if not missing:break
 time.sleep(30)
status('VERIFYING_COMPLETE_GLOBAL_COVERAGE');run('verify_final.py');run('package_result.py')
# Let producers flush their final markers, then stop only our resource watcher.
time.sleep(3);(W/'STOP_RESOURCE_WATCH').touch()
for _ in range(50):
 alive=False
 for p in psutil.process_iter(['pid','cmdline']):
  try:
   if any(a==str(W/'resource_watch.py')for a in(p.info['cmdline']or[])):alive=True
  except psutil.Error:pass
 if not alive:break
 time.sleep(1)
assert not alive,'resource watcher did not finish'
status('FREEZING_COMPLETE_PROOF_CLOSURE');run('build_manifest.py');run('verify_manifest.py')
a=json.loads((W/'manifest_verified.json').read_text());assert a['status']=='PASS';status('COMPLETE_MANIFEST_VERIFIED')
print('S22_FULL_PROOF_COMPLETE',json.loads((W/'final_coverage.json').read_text())['S'],'files',a['files'],flush=True)
