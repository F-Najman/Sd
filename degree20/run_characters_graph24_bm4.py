from pathlib import Path
import subprocess,json,time,concurrent.futures,threading,hashlib,fcntl,re,psutil,gzip,shutil,os
W=Path(__file__).resolve().parent;J=W/'large_orders';OPT=W/'optimization';lock=open(W/'characters.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert json.loads((OPT/'graph_full_replay_verified.json').read_text())['status']=='PASS'and json.loads((OPT/'fast_graph_implementation_verified.json').read_text())['status']=='PASS'
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];active={'export':{},'cpp':{},'bm':{}};adopted=[]
for proc in psutil.process_iter(['pid','cmdline']):
 try:
  args=proc.info['cmdline']or[];s=' '.join(args);stage=None
  if str(W/'export_large_sparse.m')in args:stage='export';p=int(next(a[3:]for a in args if a.startswith('P:=')));n=int(next(a[13:]for a in args if a.startswith('OrderToTest:=')))
  elif any(str(W/name)in args for name in ['krylov','krylov_hybrid']):stage='cpp'
  elif str(W/'finish_cpp.m')in args:stage='bm'
  if not stage:continue
  if stage!='export':m=re.search(r'p(\d+)_n(\d+)',s);assert m;p,n=map(int,m.groups())
  active[stage][p,n]=proc;adopted.append({'pid':proc.pid,'stage':stage,'p':p,'order':n,'args':args})
 except(psutil.NoSuchProcess,psutil.AccessDenied):pass
assert len(active['export'])<=6 and len(active['cpp'])<=24 and len(active['bm'])<=2
exports=threading.Semaphore(6-len(active['export']));cpps=threading.Semaphore(24-len(active['cpp']));bms=threading.Semaphore(4-len(active['bm']));preps=threading.Semaphore(2)
(W/'character_worker_adoption_graph24_bm4.json').write_text(json.dumps({'status':'ADOPTED','workers':adopted,'worker_limit':24,'export_limit':6,'cpp_limit':24,'bm_limit':4,'cpu_affinity':list(range(14))},indent=2)+'\n');print('S20_GRAPH_WORKERS_ADOPTED',len(adopted),flush=True)
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def atomic_json(p,a):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(a,indent=2)+'\n');t.replace(p)
def wait_process(p):
 while True:
  try:
   if not p.is_running()or p.status()==psutil.STATUS_ZOMBIE:return
  except psutil.NoSuchProcess:return
  time.sleep(.5)
def run(cmd,log,marker):
 with log.open('w')as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();assert r.returncode==0 and marker in s and not any(e in s for e in ['Runtime error','User error','Assertion failed','Traceback']),(cmd,s[-2000:])
def stage_run(stage,key,sem,cmd,log,marker):
 if key in active[stage]:
  try:wait_process(active[stage][key])
  finally:sem.release()
 elif log.exists()and marker in log.read_text():return
 else:
  with sem:run(cmd,log,marker)
 s=log.read_text();assert marker in s and not any(e in s for e in ['Runtime error','User error','Assertion failed','Traceback']),(key,stage)
def archive(p):
 dst=p.with_suffix(p.suffix+'.gz');tmp=dst.with_suffix(dst.suffix+'.tmp')
 with p.open('rb')as source,tmp.open('wb')as target:
  with gzip.GzipFile(filename='',fileobj=target,mode='wb',mtime=0)as gz:shutil.copyfileobj(source,gz,1024*1024)
 tmp.replace(dst);return sha(dst)
active_keys=set().union(*(set(v)for v in active.values()))
def one(job):
 p,n=job['p'],job['order'];key=p,n;stem=f'p{p}_n{n}';meta=J/f'{stem}.json';seq=J/f'{stem}_sequence.m';t=time.monotonic()
 if meta.exists():
  try:
   a=json.loads(meta.read_text())
   if a.get('status')=='PASS':return a
  except json.JSONDecodeError:pass
 raw=J/f'{stem}_cpp_raw.m';clog=J/f'{stem}_cpp.log';blog=J/f'{stem}_bm.log';sparse=J/f'{stem}_sparse.txt';elog=J/f'{stem}_sparse.log';graph=J/f'{stem}_graph.txt';prepared=J/f'{stem}_prepared.txt';rankfile=J/f'{stem}_graph_rank.json';verified=J/f'{stem}_graph_verified.json'
 legacy=key in active_keys or elog.exists()or sparse.exists()
 if legacy:
  stage_run('export',key,exports,['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'SparseOut:={sparse}',str(W/'export_large_sparse.m')],elog,'S20_SPARSE_EXPORT_COMPLETE');assert sparse.exists()
  stage_run('cpp',key,cpps,[str(W/'krylov_hybrid'),str(sparse),str(raw)],clog,'S20_CPP_KRYLOV_COMPLETE');assert raw.exists()
  dat=job|{'sparse_export_sha256':sha(sparse),'cpp_implementation':'hybrid_dense_rows_v1'if'S20_HYBRID_MATRIX'in clog.read_text()else'legacy_csc'};dat['cpp_binary_sha256']=sha(W/('krylov_hybrid'if dat['cpp_implementation']=='hybrid_dense_rows_v1'else'krylov'))
 else:
  glog=J/f'{stem}_graph.log'
  with exports:
   if not(glog.exists()and'S20_MANIN_GRAPH_EXPORT_COMPLETE'in glog.read_text()and graph.exists()):run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'GraphOut:={graph}',str(OPT/'export_graph_fast.m')],glog,'S20_MANIN_GRAPH_EXPORT_COMPLETE')
  previous_prepared_sha=json.loads(verified.read_text())['prepared_sha256']if verified.exists()else None
  with preps:
   run([str(OPT/'prepare_graph'),str(graph),str(prepared),str(rankfile)],J/f'{stem}_graph_prep.log','S20_MANIN_GRAPH_PREPARED')
   run(['python3',str(OPT/'verify_graph.py'),str(graph),str(prepared),str(rankfile),str(verified)],J/f'{stem}_graph_check.log','S20_GRAPH_INDEPENDENT_CERTIFICATE_PASS')
   run(['magma','-b',f'GraphIn:={graph}',f'Prepared:={prepared}',str(OPT/'check_graph_prefix.m')],J/f'{stem}_native_prefix.log','S20_GRAPH_NATIVE_PREFIX_PASS')
  if clog.exists()and'S20_CPP_KRYLOV_COMPLETE'in clog.read_text():assert previous_prepared_sha==sha(prepared)and raw.exists()
  stage_run('cpp',key,cpps,[str(W/'krylov'),str(prepared),str(raw)],clog,'S20_CPP_KRYLOV_COMPLETE')
  a=json.loads(verified.read_text());assert a['status']=='PASS';dat=job|{'cpp_implementation':'raw_manin_graph_v1','cpp_binary_sha256':sha(W/'krylov'),'graph_source_sha256':sha(OPT/'export_graph_fast.m'),'preparer_binary_sha256':sha(OPT/'prepare_graph'),'preparer_source_sha256':sha(OPT/'prepare_graph.cpp'),'native_prefix_source_sha256':sha(OPT/'check_graph_prefix.m'),'graph_verifier_source_sha256':sha(OPT/'verify_graph.py'),'ambient_dimension':a['generators'],'cuspidal_dimension':a['cuspidal_dimension'],'graph_sha256':a['graph_sha256'],'prepared_sha256':a['prepared_sha256'],'rank_certificate_sha256':sha(rankfile),'graph_independent_certificate_sha256':sha(verified)}
 stage_run('bm',key,bms,['magma','-b',f'Raw:={raw}',f'Final:={seq}',str(W/'finish_cpp.m')],blog,'S20_CPP_LINEAR_COMPLEXITY_CERTIFIED');assert seq.exists()
 if not legacy:dat['graph_archive_sha256']=archive(graph);dat['prepared_archive_sha256']=archive(prepared)
 dat.update({'status':'PASS','seconds_after_resume':time.monotonic()-t,'sequence_sha256':sha(seq)});atomic_json(meta,dat);raw.unlink()
 if legacy:sparse.unlink()
 else:graph.unlink();prepared.unlink()
 print('S20_CHARACTER_PASS',p,n,dat['cpp_implementation'],round(dat['seconds_after_resume'],1),flush=True);return dat
jobs.sort(key=lambda j:((j['p'],j['order'])not in active_keys,-j['p'],-j['order']))
with concurrent.futures.ThreadPoolExecutor(max_workers=24)as ex:results=list(ex.map(one,jobs))
atomic_json(W/'large_native_results.json',{'status':'PASS','characters':len(results),'results':results});print('S20_CHARACTER_BATCH_COMPLETE',len(results),flush=True)
