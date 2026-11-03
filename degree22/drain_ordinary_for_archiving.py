from pathlib import Path
import psutil,time,json
W=Path(__file__).resolve().parent
p=psutil.Process(2075069);assert p.cmdline()==['python3','work/degree22/run_new_ordinary.py'];p.suspend()
q=psutil.Process(2143292);assert q.cmdline()==['python3','work/degree22/pipeline_sieves.py'];q.suspend();assert not q.children(recursive=True);q.kill()
children=p.children(recursive=True);assert children
for c in children:assert any('degree22/full'in a for a in c.cmdline()),c.cmdline()
print('S22_ORDINARY_CONTROLLER_DRAIN_STARTED',p.pid,[c.pid for c in children],flush=True)
while True:
 active=[]
 for c in children:
  try:
   if c.is_running()and c.status()!=psutil.STATUS_ZOMBIE:active.append(c.pid)
  except psutil.Error:pass
 if not active:break
 print('S22_ORDINARY_CONTROLLER_DRAIN_WAIT',active,flush=True);time.sleep(10)
p.kill();(W/'ordinary_drain_complete.json').write_text(json.dumps({'status':'PASS','old_driver':2075069,'old_pipeline':2143292,'finished_children':[c.pid for c in children]},indent=2)+'\n');print('S22_ORDINARY_DRAIN_COMPLETE',flush=True)
