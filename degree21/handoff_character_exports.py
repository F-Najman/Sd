"""Drain all active native/CPP children before increasing graph-export capacity."""
from pathlib import Path
import os,signal,time,json,subprocess,psutil
W=Path(__file__).resolve().parent;found=[]
for p in psutil.process_iter(['pid','cmdline']):
 a=p.info['cmdline']or[]
 if len(a)==2 and a[0].endswith('python3')and a[1].endswith('work/degree21/run_characters_free.py'):found.append(p)
assert len(found)==1;old=found[0];children=old.children(recursive=True);records=[]
for p in children:
 try:records.append({'pid':p.pid,'cmdline':p.cmdline(),'cpu_user_at_checkpoint':p.cpu_times().user})
 except psutil.Error:pass
os.kill(old.pid,signal.SIGSTOP)
def alive(p):
 try:return p.is_running()and p.status()!=psutil.STATUS_ZOMBIE
 except psutil.Error:return False
while any(alive(p)for p in children):time.sleep(2)
os.kill(old.pid,signal.SIGKILL);old.wait(timeout=15)
s=(W/'run_characters_free.py').read_text();assert s.count('exports=threading.Semaphore(4)')==1;s=s.replace('exports=threading.Semaphore(4)','exports=threading.Semaphore(8)');(W/'run_characters_free8.py').write_text(s)
(W/'character_export_worker_checkpoint.json').write_text(json.dumps({'status':'ALL_ACTIVE_CHILDREN_DRAINED_BEFORE_RESUME','old_parent':old.pid,'children':records,'new_export_limit':8,'task_threads':24,'CPP_limit':24,'arithmetic_engines_unchanged':True,'global_affinity_and_resource_budget_unchanged':True},indent=2)+'\n')
with(W/'run_characters_free8.log').open('w')as f:r=subprocess.run(['python3',str(W/'run_characters_free8.py')],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
