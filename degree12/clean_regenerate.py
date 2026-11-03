"""Regenerate the conservatively affected group after all old stages finish."""
from pathlib import Path
import subprocess,psutil,json,time,hashlib,sys
W=Path(__file__).resolve().parent;J=W/'large_orders';jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];todo=json.loads((W/'clean_regeneration_required.json').read_text())['jobs'];assert len(todo)==20
def global_stages():
 out=[]
 for p in psutil.process_iter(['name','cmdline']):
  try:
   a=p.info['cmdline']or[]
   if p.info['name']in ['magma.exe','krylov']and any(str(W)in z and Path(z).name in ['large_order.m','export_large_sparse.m','finish_cpp.m','krylov']for z in a):out.append(p)
  except(psutil.NoSuchProcess,psutil.AccessDenied):pass
 return out
print('CLEAN_REGENERATION_WAITING_FOR_ORIGINAL_BATCH',flush=True)
while True:
 states=[]
 for r in jobs:
  p=J/f"p{r['p']}_n{r['order']}.json"
  if p.exists():
   try:states.append(json.loads(p.read_text()))
   except json.JSONDecodeError:pass
 assert all(r['status']=='PASS'for r in states),[r for r in states if r['status']!='PASS']
 if len(states)==len(jobs)and not global_stages():break
 time.sleep(5)
for proc in psutil.process_iter(['name','cmdline']):
 try:
  a=proc.info['cmdline']or[]
  if proc.info['name']=='python'and any(Path(z).name=='check_sequences.py'and'work/degree12/'in z for z in a):proc.terminate();proc.wait(timeout=10)
 except(psutil.NoSuchProcess,psutil.AccessDenied):pass
for proc in psutil.process_iter(['name','cmdline']):
 try:
  a=proc.info['cmdline']or[]
  
  if proc.info['name']=='python'and any(Path(z).name=='run_large_cpp.py'and'work/degree12/'in z for z in a):proc.wait(timeout=15)
 except(psutil.NoSuchProcess,psutil.AccessDenied):pass
start=time.time();archive=W/'overlap_review_archive';archive.mkdir(exist_ok=False)
suffixes=['.json','_sequence.m','_independent_pade.json','.log','_sparse.log','_sparse.txt','_cpp_raw.m','_cpp.log','_bm.log']
for r in todo:
 stem=f"p{r['p']}_n{r['order']}"
 for suf in suffixes:
  p=J/(stem+suf)
  if p.exists():p.rename(archive/p.name)
print('CLEAN_REGENERATION_STARTED',len(todo),'jobs',flush=True)
checker=W/'check_sequences.py';s=checker.read_text();at=s.index('while len(done)<len(jobs):')
cache='''# Reuse only unchanged previously constructed certificates as a cache.
# verify_large.py independently checks every polynomial identity afterwards.
for job in jobs:
 p,n=job['p'],job['order'];stem=f'p{p}_n{n}';cf=J/f'{stem}_independent_pade.json';sf=J/f'{stem}_sequence.m';mf=J/f'{stem}.json'
 if not all(f.exists()for f in[cf,sf,mf]):continue
 c=json.loads(cf.read_text());state=json.loads(mf.read_text())
 if state['status']=='PASS'and c['sequence_sha256']==hashlib.sha256(sf.read_bytes()).hexdigest():done[p,n]={k:v for k,v in c.items()if k not in ['C','A']}
'''
if '# Reuse only unchanged previously constructed certificates as a cache.'not in s:checker.write_text(s[:at]+cache+s[at:])
with (W/'clean_pade.log').open('w')as out:
 sage=subprocess.Popen([sys.executable,'-u',str(checker)],stdout=out,stderr=subprocess.STDOUT)
 with (W/'clean_batch.log').open('w')as log:r=subprocess.run([sys.executable,'-u',str(W/'run_large_cpp.py')],stdout=log,stderr=subprocess.STDOUT)
 assert r.returncode==0,'Clean batch failed'
 assert sage.wait()==0,'Clean Pade verification failed'
assert not global_stages(),'Unfinished numerical stages remain'
data=[]
for r in todo:
 stem=f"p{r['p']}_n{r['order']}";mf=J/(stem+'.json');sf=J/(stem+'_sequence.m');cf=J/(stem+'_independent_pade.json');m=json.loads(mf.read_text());c=json.loads(cf.read_text());assert m['status']=='PASS'and sf.stat().st_mtime>=start and cf.stat().st_mtime>=start
 sha=hashlib.sha256(sf.read_bytes()).hexdigest();assert c['sequence_sha256']==sha and m['sequence_sha256']==sha
 data.append(r|{'sequence_sha256':sha,'pade_certificate_sha256':hashlib.sha256(cf.read_bytes()).hexdigest(),'method':m['method']})
summary={'status':'PASS','jobs':data,'count':len(data),'isolated_regeneration':True,'started_unix':start,'finished_unix':time.time(),'all_previous_numerical_stages_exited_before_regeneration':True};(W/'scheduler_cleanup.json').write_text(json.dumps(summary,indent=2)+'\n');print('CLEAN_REGENERATION_COMPLETE',len(data),'PASS',flush=True)
