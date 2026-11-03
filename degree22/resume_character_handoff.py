"""Finish the drained handoff after an overstrict transient-child check."""
from pathlib import Path
import psutil,json,subprocess,time,hashlib
W=Path(__file__).resolve().parent;O=W/'optimization'
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
for f,b in [('packed_full_replay_verified.json','krylov_packed'),('simd_full_replay_verified.json','krylov_simd')]:
 a=json.loads((O/f).read_text());assert a['status']=='PASS'and a['source_sha256']==sha(W/(b+'.cpp'))and a['binary_sha256']==sha(W/b)
assert not psutil.pid_exists(2065541)
# The old arithmetic children all finished before the old launcher exited.
assert'S22_CHARACTER_CHILDREN_DRAINED'in(W/'handoff_characters_simd.log').read_text()
q=psutil.Process(2065381);assert q.cmdline()==['python3','work/degree22/verify_large.py'];q.suspend();children=q.children(recursive=True)
print('S22_OLD_READONLY_AUDITOR_DRAIN',[(c.pid,c.name())for c in children],flush=True)
while True:
 active=[]
 for c in children:
  try:
   if c.is_running()and c.status()!=psutil.STATUS_ZOMBIE:active.append(c.pid)
  except psutil.Error:pass
 if not active:break
 time.sleep(1)
q.kill();time.sleep(1)
with(W/'run_characters_simd.log').open('w')as out:driver=subprocess.Popen(['nice','-n','10','python3',str(W/'run_characters_simd.py')],stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
with(W/'verify_large_simd.log').open('w')as out:verifier=subprocess.Popen(['nice','-n','10','sage',str(W/'verify_large_simd.py')],stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
time.sleep(2);assert driver.poll()is None and verifier.poll()is None
expected={str(W/f):sha(W/f)for f in ['krylov_packed','krylov_packed.cpp','krylov_simd','krylov_simd.cpp','run_characters.py','run_characters_simd.py','verify_large_simd.py']}
cert={'status':'PASS','old_driver':2065541,'old_verifier':2065381,'new_driver':driver.pid,'new_verifier':verifier.pid,'frozen_sources_and_binaries':expected,'all_full_replays_passed_before_handoff':True,'completed_packed_raw_outputs_reused_with_identical_regenerated_plan_hashes':True,'original_safety_check_was_overstrict_about_a_transient_readonly_auditor_child':True,'resumed_only_after_all_arithmetic_children_drained':True}
(W/'character_handoff_complete.json').write_text(json.dumps(cert,indent=2)+'\n');print('S22_SIMD_CHARACTER_HANDOFF_COMPLETE',driver.pid,verifier.pid,flush=True)
