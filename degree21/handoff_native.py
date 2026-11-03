"""Safe native worker reallocation: drain existing children before resuming."""
from pathlib import Path
import os,signal,time,json,subprocess,psutil
W=Path(__file__).resolve().parent
old=psutil.Process(3603759);assert 'run_new_ordinary.py'in' '.join(old.cmdline());children=old.children(recursive=True);records=[{'pid':p.pid,'cmdline':p.cmdline()}for p in children];os.kill(old.pid,signal.SIGSTOP)
while any(p.is_running()and p.status()!=psutil.STATUS_ZOMBIE for p in children):time.sleep(2)
os.kill(old.pid,signal.SIGKILL)
s=(W/'run_new_ordinary.py').read_text().replace('max_workers=3','max_workers=8');(W/'run_new_ordinary_8.py').write_text(s)
# The flock on the old launcher is released on process exit. Native point files
# already completed are reused solely after their exact completion markers.
(W/'native_worker_checkpoint.json').write_text(json.dumps({'status':'ALL_CHILDREN_DRAINED','old_parent':old.pid,'children':records,'new_workers':8},indent=2)+'\n')
with(W/'run_new_ordinary_8.log').open('w')as f:r=subprocess.run(['python3',str(W/'run_new_ordinary_8.py')],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
