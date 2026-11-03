from pathlib import Path
import psutil,json,time,signal,subprocess
W=Path(__file__).resolve().parent;a=json.loads((W/'free_engine_checkpoint.json').read_text());pp=psutil.Process(a['parent_pid']);assert pp.status()==psutil.STATUS_STOPPED
while True:
 active=[]
 for r in a['children']:
  try:
   p=psutil.Process(r['pid'])
   if p.is_running()and p.status()!=psutil.STATUS_ZOMBIE:active.append(p.pid)
  except psutil.NoSuchProcess:pass
 print('S21_FREE_CHECKPOINT_CHILDREN_REMAINING',len(active),flush=True)
 if not active:break
 time.sleep(30)
a['parent_cpu_before_kill']=pp.cpu_times()._asdict();a['finished_child_cpu']={}
for r in a['children']:
 try:a['finished_child_cpu'][str(r['pid'])]=psutil.Process(r['pid']).cpu_times()._asdict()
 except psutil.NoSuchProcess:pass
pp.kill()
while True:
 try:
  if not pp.is_running()or pp.status()==psutil.STATUS_ZOMBIE:break
 except psutil.NoSuchProcess:break
 time.sleep(.05)
a['status']='ALL_CHILDREN_FINISHED_PARENT_TERMINATED';(W/'free_engine_checkpoint.json').write_text(json.dumps(a,indent=2)+'\n');print('S21_FREE_ENGINE_HANDOFF_SAFE',flush=True)
with(W/'run_characters_free.log').open('w')as f:r=subprocess.run(['python3',str(W/'run_characters_free.py')],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0;print('S21_FREE_BATCH_FINISHED',flush=True)
