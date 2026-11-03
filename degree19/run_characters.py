from pathlib import Path
import subprocess,json,time,concurrent.futures,threading,hashlib,fcntl
W=Path(__file__).resolve().parent;J=W/'large_orders';lock=open(W/'characters.lock','w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];exports=threading.Semaphore(2);cpps=threading.Semaphore(4);bms=threading.Semaphore(1)
def one(job):
 p,n=job['p'],job['order'];stem=f'p{p}_n{n}';meta=J/f'{stem}.json';seq=J/f'{stem}_sequence.m';t=time.monotonic()
 if meta.exists()and json.loads(meta.read_text()).get('status')=='PASS':return json.loads(meta.read_text())
 sparse=J/f'{stem}_sparse.txt';elog=J/f'{stem}_sparse.log';raw=J/f'{stem}_cpp_raw.m';clog=J/f'{stem}_cpp.log';blog=J/f'{stem}_bm.log'
 if not(elog.exists()and 'S19_SPARSE_EXPORT_COMPLETE'in elog.read_text()and sparse.exists()):
  with exports,elog.open('w')as o:r=subprocess.run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'SparseOut:={sparse}',str(W/'export_large_sparse.m')],stdout=o,stderr=subprocess.STDOUT)
 assert sparse.exists()and'S19_SPARSE_EXPORT_COMPLETE'in elog.read_text(),stem+' export'
 if not(clog.exists()and'S19_CPP_KRYLOV_COMPLETE'in clog.read_text()and raw.exists()):
  with cpps,clog.open('w')as o:r=subprocess.run([str(W/'krylov'),str(sparse),str(raw)],stdout=o,stderr=subprocess.STDOUT)
 assert 'S19_CPP_KRYLOV_COMPLETE'in clog.read_text(),stem+' krylov'
 with bms,blog.open('w')as o:r=subprocess.run(['magma','-b',f'Raw:={raw}',f'Final:={seq}',str(W/'finish_cpp.m')],stdout=o,stderr=subprocess.STDOUT)
 assert r.returncode==0 and'S19_CPP_LINEAR_COMPLEXITY_CERTIFIED'in blog.read_text(),stem+' BM'
 h=hashlib.sha256(sparse.read_bytes()).hexdigest();raw.unlink();sparse.unlink()
 dat=job|{'status':'PASS','seconds':time.monotonic()-t,'sparse_export_sha256':h,'sequence_sha256':hashlib.sha256(seq.read_bytes()).hexdigest()};meta.write_text(json.dumps(dat,indent=2)+'\n');print('S19_CHARACTER_PASS',p,n,round(dat['seconds'],1),flush=True);return dat
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as ex:results=list(ex.map(one,jobs))
(W/'large_native_results.json').write_text(json.dumps({'status':'PASS','characters':len(results),'results':results},indent=2)+'\n');print('S19_CHARACTER_BATCH_COMPLETE',len(results),flush=True)
