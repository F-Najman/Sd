from pathlib import Path
import json,re,shutil
W=Path(__file__).resolve().parent; O=W.parent/'degree18'; D12=W.parent/'degree12'
for name in ['export_large_sparse.m','finish_cpp.m','krylov.cpp']:
 (W/name).write_text((D12/name).read_text().replace('S12_','S19_'))
J=W/'large_orders';J.mkdir(exist_ok=True)
code='''from pathlib import Path
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
 dat=job|{'status':'PASS','seconds':time.monotonic()-t,'sparse_export_sha256':h,'sequence_sha256':hashlib.sha256(seq.read_bytes()).hexdigest()};meta.write_text(json.dumps(dat,indent=2)+'\\n');print('S19_CHARACTER_PASS',p,n,round(dat['seconds'],1),flush=True);return dat
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as ex:results=list(ex.map(one,jobs))
(W/'large_native_results.json').write_text(json.dumps({'status':'PASS','characters':len(results),'results':results},indent=2)+'\\n');print('S19_CHARACTER_BATCH_COMPLETE',len(results),flush=True)
'''
(W/'run_characters.py').write_text(code)
src=(O/'full127/stage2_chunk.m').read_text();jobs=[]
import sys
sys.path.insert(0,str(W));from unit_arithmetic import lit
for n in [47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137]:
 H=W/f'full{n}';H.mkdir(exist_ok=True)
 s=src.replace(str(O/'full127'),str(H)).replace(str(O/'sources127.m'),str(W/f'sources{n}.m')).replace('144 div d','152 div d').replace('rec[1]ne 18','rec[1]ne 19')
 if n==137:s=s.replace('or rec[1]ne 19','').replace('N eq 101 select 4 else 3','8')
 (H/'stage2_chunk.m').write_text(s)
 records=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');inds=[i+1 for i,r in enumerate(records)if r[6]and(n==137 or r[0]==19)]
 for k in range(0,len(inds),8):jobs.append({'N':n,'start':inds[k],'end':inds[min(k+7,len(inds)-1)]})
(W/'new_ordinary_jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
(W/'run_new_ordinary.py').write_text((O/'run_new_ordinary.py').read_text().replace('S18_','S19_'))
s=(W.parent/'audit11/rational_two.m').read_text().replace('4*10^9','32*10^9');(W/'rational_two163.m').write_text(s)
print('new character jobs',len(json.loads((W/'large_selected_orders.json').read_text())['jobs']),'jet chunks',len(jobs))
