"""Certified Manin graph batch with independent dual-coordinate plans."""
from pathlib import Path
import subprocess,json,time,concurrent.futures,threading,hashlib,fcntl,gzip,shutil,re
W=Path(__file__).resolve().parent;J=W/'large_orders';OPT=W/'optimization';lock=open(W/'characters.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert json.loads((OPT/'free_full_replay_verified.json').read_text())['status']=='PASS'and json.loads((OPT/'free_fixtures_verified.json').read_text())['status']=='PASS'
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];exports=threading.Semaphore(8);preps=threading.Semaphore(2);cpps=threading.Semaphore(24);finishers=threading.Semaphore(4)
checkpoint=json.loads((W/'free_engine_checkpoint.json').read_text());assert checkpoint['status']=='ALL_CHILDREN_FINISHED_PARENT_TERMINATED';cache={}
for rec in checkpoint['children']:
 args=rec['cmdline'];mt=re.search(r'p(\d+)_n(\d+)', ' '.join(args))
 if mt and args and Path(args[0]).name in ['krylov','krylov_blocked','krylov_blocked_v2']:cache[tuple(map(int,mt.groups()))]=Path(args[0]).name
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def atomic(p,a):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(a,indent=2)+'\n');t.replace(p)
def run(cmd,log,marker):
 with log.open('w')as f:r=subprocess.run(list(map(str,cmd)),stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();assert r.returncode==0 and marker in s and not any(x in s for x in ['Runtime error','User error','Assertion failed','Traceback']), (cmd,s[-2000:])
def archive(p):
 dst=p.with_suffix(p.suffix+'.gz');tmp=dst.with_suffix(dst.suffix+'.tmp')
 with p.open('rb')as source,tmp.open('wb')as target:
  with gzip.GzipFile(filename='',fileobj=target,mode='wb',mtime=0)as f:shutil.copyfileobj(source,f,1024*1024)
 tmp.replace(dst);return sha(dst)
def one(job):
 p,n=job['p'],job['order'];stem=f'p{p}_n{n}';meta=J/f'{stem}.json';sf=J/f'{stem}_sequence.m';t=time.monotonic()
 if meta.exists():
  a=json.loads(meta.read_text());assert a['status']=='PASS'and a['sequence_sha256']==sha(sf);return a
 G=J/f'{stem}_graph.txt';P=J/f'{stem}_prepared.txt';C=J/f'{stem}_graph_rank.json';V=J/f'{stem}_graph_verified.json';L=J/f'{stem}_free.txt';F=J/f'{stem}_free_verified.json';raw=J/f'{stem}_cpp_raw.m';clog=J/f'{stem}_cpp.log';glog=J/f'{stem}_graph.log';ff=J/f'{stem}_fast_pade.json'
 with exports:
  if not(G.exists()and glog.exists()and'S20_MANIN_GRAPH_EXPORT_COMPLETE'in glog.read_text()):run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'GraphOut:={G}',OPT/'export_graph_fast.m'],glog,'S20_MANIN_GRAPH_EXPORT_COMPLETE')
 oldP=json.loads(V.read_text())['prepared_sha256']if V.exists()else None
 with preps:
  run([OPT/'prepare_graph',G,P,C],J/f'{stem}_graph_prep.log','S20_MANIN_GRAPH_PREPARED')
  run(['python3',OPT/'verify_graph.py',G,P,C,V],J/f'{stem}_graph_check.log','S20_GRAPH_INDEPENDENT_CERTIFICATE_PASS')
  run(['magma','-b',f'GraphIn:={G}',f'Prepared:={P}',OPT/'check_graph_prefix.m'],J/f'{stem}_native_prefix.log','S20_GRAPH_NATIVE_PREFIX_PASS')
 ss=clog.read_text()if clog.exists()else'';oldraw=raw.exists()and any(s in ss for s in ['S20_CPP_KRYLOV_COMPLETE','S21_CPP_BLOCKED_KRYLOV_COMPLETE']);freecached=raw.exists()and'S21_FREE_GRAPH_KRYLOV_COMPLETE'in ss
 v=json.loads(V.read_text());assert v['status']=='PASS';q=v['q'];ns=v['generators'];k=v['cuspidal_dimension']
 if oldraw:
  assert oldP==sha(P);binary=cache.get((p,n),'krylov_blocked_v2'if ns*(q-1)**2>2**64-1 else'krylov');assert('S21_CPP_BLOCKED_KRYLOV_COMPLETE'in ss)==(binary!='krylov');engine='raw_manin_graph_v1'
 else:
  oldL=json.loads(F.read_text())['free_plan_sha256']if F.exists()else None
  with preps:
   run(['python3',OPT/'prepare_free.py',G,P,C,L],J/f'{stem}_free_prep.log','S21_FREE_GRAPH_PREPARED')
   run(['python3',OPT/'verify_free.py',G,P,C,V,L,F],J/f'{stem}_free_check.log','S21_FREE_GRAPH_INDEPENDENT_PASS')
  if freecached:assert oldP==sha(P)and oldL==sha(L)
  else:
   with cpps:run([W/'krylov_free',L,raw],clog,'S21_FREE_GRAPH_KRYLOV_COMPLETE')
  binary='krylov_free';engine='free_dual_graph_v1'
 with finishers:run([W/'finish_fast',raw,sf,ff],J/f'{stem}_bm.log','S21_FAST_PADE_CERTIFIED')
 dat=job|{'status':'PASS','cpp_implementation':engine,'cpp_binary_name':binary,'cpp_binary_sha256':sha(W/binary),'cpp_source_sha256':sha(W/(binary+'.cpp')),'blocked_accumulation':binary in ['krylov_blocked','krylov_blocked_v2'],'ambient_dimension':ns,'cuspidal_dimension':k,'graph_source_sha256':sha(OPT/'export_graph_fast.m'),'preparer_binary_sha256':sha(OPT/'prepare_graph'),'preparer_source_sha256':sha(OPT/'prepare_graph.cpp'),'native_prefix_source_sha256':sha(OPT/'check_graph_prefix.m'),'graph_verifier_source_sha256':sha(OPT/'verify_graph.py'),'graph_sha256':v['graph_sha256'],'prepared_sha256':v['prepared_sha256'],'rank_certificate_sha256':sha(C),'graph_independent_certificate_sha256':sha(V),'recurrence_engine':'NTL_half_gcd','recurrence_source_sha256':sha(W/'finish_fast.cpp'),'recurrence_binary_sha256':sha(W/'finish_fast'),'fast_pade_sha256':sha(ff),'sequence_sha256':sha(sf),'seconds_after_resume':time.monotonic()-t}
 if not oldraw:
  dat.update({'free_plan_sha256':sha(L),'free_plan_producer_sha256':sha(OPT/'prepare_free.py'),'free_plan_verifier_sha256':sha(OPT/'verify_free.py'),'free_plan_verification_sha256':sha(F),'free_plan_archive_sha256':archive(L),'cpp_cpu_seconds':float(re.search(r'cpu_seconds=([0-9.]+)',clog.read_text())[1])})
 dat['graph_archive_sha256']=archive(G);dat['prepared_archive_sha256']=archive(P);atomic(meta,dat);raw.unlink();G.unlink();P.unlink()
 if not oldraw:L.unlink()
 print('S21_CHARACTER_PASS',p,n,engine,'seconds',round(time.monotonic()-t,1),flush=True);return dat
jobs.sort(key=lambda j:(-j['p'],-j['order']))
with concurrent.futures.ThreadPoolExecutor(max_workers=24)as ex:results=list(ex.map(one,jobs))
atomic(W/'large_native_results.json',{'status':'PASS','degree':21,'characters':len(results),'results':results});print('S21_CHARACTER_BATCH_COMPLETE',len(results),flush=True)
