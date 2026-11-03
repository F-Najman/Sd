"""Drain only our old character workers after complete independent replay."""
from pathlib import Path
import psutil,time,json,subprocess,sys,hashlib,os
W=Path(__file__).resolve().parent;O=W/'optimization'
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
expected={str(W/f):sha(W/f)for f in ['krylov_packed','krylov_packed.cpp','krylov_simd','krylov_simd.cpp','run_characters.py','run_characters_simd.py','verify_large_simd.py']}
for tag in ['huge','reference']:
 while not ('S22_SIMD_GRAPH_KRYLOV_COMPLETE'in(O/f'simd_{tag}_full.log').read_text()):time.sleep(10)
cp=subprocess.run([sys.executable,str(O/'verify_simd_replay.py')],capture_output=True,text=True);assert cp.returncode==0,(cp.stdout,cp.stderr);print(cp.stdout,flush=True)
assert all(sha(Path(p))==h for p,h in expected.items())
p=psutil.Process(2065541);assert p.cmdline()==['python3','work/degree22/run_characters.py'];p.suspend();children=p.children(recursive=True)
for c in children:
 try:args=c.cmdline()
 except psutil.ZombieProcess:continue
 assert any(str(W/'large_orders')in a for a in args),args
print('S22_CHARACTER_DRAIN_STARTED',p.pid,[c.pid for c in children],flush=True)
while True:
 active=[]
 for c in children:
  try:
   if c.is_running()and c.status()!=psutil.STATUS_ZOMBIE:active.append(c.pid)
  except psutil.Error:pass
 if not active:break
 print('S22_CHARACTER_DRAIN_WAIT',active,flush=True);time.sleep(30)
p.kill();print('S22_CHARACTER_CHILDREN_DRAINED',flush=True)
q=psutil.Process(2065381);assert q.cmdline()==['python3','work/degree22/verify_large.py'];assert not q.children(recursive=True);q.terminate()
try:q.wait(timeout=10)
except psutil.TimeoutExpired:q.kill()
time.sleep(1)
assert all(sha(Path(f))==h for f,h in expected.items())
with(W/'run_characters_simd.log').open('w')as out:
 driver=subprocess.Popen(['nice','-n','10','python3',str(W/'run_characters_simd.py')],stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
with(W/'verify_large_simd.log').open('w')as out:
 verifier=subprocess.Popen(['nice','-n','10','sage',str(W/'verify_large_simd.py')],stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
time.sleep(2);assert driver.poll()is None and verifier.poll()is None
cert={'status':'PASS','old_driver':p.pid,'old_verifier':q.pid,'drained_children':[c.pid for c in children],'new_driver':driver.pid,'new_verifier':verifier.pid,'frozen_sources_and_binaries':expected,'all_full_replays_passed_before_handoff':True,'completed_packed_raw_outputs_reused_with_identical_regenerated_plan_hashes':True}
(W/'character_handoff_complete.json').write_text(json.dumps(cert,indent=2)+'\n');print('S22_SIMD_CHARACTER_HANDOFF_COMPLETE',driver.pid,verifier.pid,flush=True)
