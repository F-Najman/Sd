"""Drain the active sieve before resuming the same queue with two workers."""
from pathlib import Path
import psutil,os,signal,time,json
W=Path(__file__).resolve().parent;found=[]
for p in psutil.process_iter(['pid','cmdline']):
 a=p.info['cmdline']or[]
 if len(a)==2 and a[0].endswith(('python','python3'))and a[1].endswith('work/degree21/pipeline_sieves.py'):found.append(p)
assert len(found)==1;old=found[0];children=old.children(recursive=True);rec=[{'pid':p.pid,'cmdline':p.cmdline()}for p in children];os.kill(old.pid,signal.SIGSTOP)
while any(p.is_running()and p.status()!=psutil.STATUS_ZOMBIE for p in children):time.sleep(2)
os.kill(old.pid,signal.SIGKILL)
s=(W/'pipeline_sieves.py').read_text().replace('max_workers=1','max_workers=2')
a="H=W/f'full{n}';merge(n);print('S21_SIEVE_STARTED',n,round(time.monotonic()-tt,1),flush=True)"
b="""H=W/f'full{n}'
 if(H/'sieve.json').exists()and(H/'sieve.log').exists()and'AUDIT_FULL_SIEVE_COMPLETE'in(H/'sieve.log').read_text():
  a=json.loads((H/'sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions'],(n,a['exceptions']);print('S21_SIEVE_REUSED_COMPLETE',n,flush=True);return{'N':n,'status':'PASS'}
 merge(n);print('S21_SIEVE_STARTED',n,round(time.monotonic()-tt,1),flush=True)"""
assert s.count(a)==1;s=s.replace(a,b);(W/'pipeline_sieves_2.py').write_text(s)
(W/'sieve_worker_checkpoint.json').write_text(json.dumps({'status':'OLD_CHILDREN_DRAINED_BEFORE_TWO_WORKER_RESUME','old_parent':old.pid,'children':rec,'new_workers':2},indent=2)+'\n')
import subprocess
with(W/'pipeline_sieves_2.log').open('w')as f:r=subprocess.run(['python3',str(W/'pipeline_sieves_2.py')],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
