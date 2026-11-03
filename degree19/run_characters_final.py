from pathlib import Path
import subprocess,json,time,concurrent.futures,threading,hashlib,fcntl,re,psutil
W=Path(__file__).resolve().parent;J=W/'large_orders';lock=open(W/'characters.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];active={'export':{},'cpp':{},'bm':{}};adopted=[]
for proc in psutil.process_iter(['pid','name','cmdline']):
 try:
  args=proc.info['cmdline']or[];s=' '.join(args);stage=None
  if str(W/'export_large_sparse.m')in args:stage='export';p=int(next(a[3:]for a in args if a.startswith('P:=')));n=int(next(a[13:]for a in args if a.startswith('OrderToTest:=')))
  elif str(W/'krylov')in args:stage='cpp'
  elif str(W/'finish_cpp.m')in args:stage='bm'
  if not stage:continue
  if stage!='export':m=re.search(r'p(\d+)_n(\d+)',s);assert m;p,n=map(int,m.groups())
  active[stage][p,n]=proc;adopted.append({'pid':proc.pid,'stage':stage,'p':p,'order':n,'args':args})
 except(psutil.NoSuchProcess,psutil.AccessDenied):pass
assert len(active['export'])<=2 and len(active['cpp'])<=8 and len(active['bm'])<=1
exports=threading.Semaphore(2-len(active['export']));cpps=threading.Semaphore(8-len(active['cpp']));bms=threading.Semaphore(1-len(active['bm']))
(W/'character_worker_adoption_final.json').write_text(json.dumps({'status':'ADOPTED','workers':adopted,'worker_limit':8,'export_limit':2,'cpp_limit':8},indent=2)+'\n');print('S19_CHARACTER_WORKERS_ADOPTED',len(adopted),'maximum total workers8',flush=True)
def wait_process(p):
 while True:
  try:
   if not p.is_running()or p.status()==psutil.STATUS_ZOMBIE:return
  except psutil.NoSuchProcess:return
  time.sleep(.5)
def stage_run(stage,key,sem,cmd,log,marker):
 if key in active[stage]:
  try:wait_process(active[stage][key])
  finally:sem.release()
 elif log.exists()and marker in log.read_text():return
 else:
  with sem,log.open('w')as o:r=subprocess.run(cmd,stdout=o,stderr=subprocess.STDOUT)
  assert r.returncode==0,(key,stage)
 assert marker in log.read_text()and not any(e in log.read_text()for e in['Runtime error','User error','Assertion failed','Traceback']),(key,stage)
def one(job):
 p,n=job['p'],job['order'];key=p,n;stem=f'p{p}_n{n}';meta=J/f'{stem}.json';seq=J/f'{stem}_sequence.m';t=time.monotonic()
 if meta.exists()and json.loads(meta.read_text()).get('status')=='PASS':return json.loads(meta.read_text())
 sparse=J/f'{stem}_sparse.txt';elog=J/f'{stem}_sparse.log';raw=J/f'{stem}_cpp_raw.m';clog=J/f'{stem}_cpp.log';blog=J/f'{stem}_bm.log'
 assert sparse.exists()or not(elog.exists()and'S19_SPARSE_EXPORT_COMPLETE'in elog.read_text()),(key,'missing sparse file from interrupted finalization')
 stage_run('export',key,exports,['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'SparseOut:={sparse}',str(W/'export_large_sparse.m')],elog,'S19_SPARSE_EXPORT_COMPLETE');assert sparse.exists()
 stage_run('cpp',key,cpps,[str(W/'krylov'),str(sparse),str(raw)],clog,'S19_CPP_KRYLOV_COMPLETE');assert raw.exists()
 stage_run('bm',key,bms,['magma','-b',f'Raw:={raw}',f'Final:={seq}',str(W/'finish_cpp.m')],blog,'S19_CPP_LINEAR_COMPLEXITY_CERTIFIED');assert seq.exists()
 h=hashlib.sha256(sparse.read_bytes()).hexdigest();dat=job|{'status':'PASS','seconds_after_resume':time.monotonic()-t,'sparse_export_sha256':h,'sequence_sha256':hashlib.sha256(seq.read_bytes()).hexdigest()};meta.write_text(json.dumps(dat,indent=2)+'\n');raw.unlink();sparse.unlink();print('S19_CHARACTER_PASS',p,n,round(dat['seconds_after_resume'],1),flush=True);return dat
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:results=list(ex.map(one,jobs))
(W/'large_native_results.json').write_text(json.dumps({'status':'PASS','characters':len(results),'results':results},indent=2)+'\n');print('S19_CHARACTER_BATCH_COMPLETE',len(results),flush=True)
