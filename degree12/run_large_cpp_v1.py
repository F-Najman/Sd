from pathlib import Path
import subprocess,json,time,concurrent.futures,threading,hashlib,re,psutil
W=Path(__file__).resolve().parent;J=W/'large_orders';jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];cv=threading.Condition();used=0.;active={}
def weight(p):return max(3.,100.*(p/530807.)**2)
def log_ok(p,n):return f'S12_SELECTED_CHARACTER_NONSTRANGE p={p} order={n} 'in (J/f'p{p}_n{n}.log').read_text()if (J/f'p{p}_n{n}.log').exists()else False
for proc in psutil.process_iter(['cmdline','name']):
 try:
  a=proc.info['cmdline']or[]
  if proc.info['name']!='magma.exe' or str(W/'large_order.m')not in a:continue
  p=int(next(z[3:]for z in a if z.startswith('P:=')));n=int(next(z[13:]for z in a if z.startswith('OrderToTest:=')))
  active[p,n]=proc;used+=weight(p)
 except(psutil.NoSuchProcess,psutil.AccessDenied,StopIteration):pass
print('ADOPTED_NATIVE_JOBS',len(active),'reserved_GiB',used,flush=True)
def acquire(w):
 global used
 with cv:
  while used+w>310.:cv.wait(5)
  used+=w
def release(w):
 global used
 with cv:used-=w;cv.notify_all()
def native(p,n,seq):
 out=J/f'p{p}_n{n}.log'
 with out.open('w')as f:r=subprocess.run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'SequenceOutput:={seq}',str(W/'large_order.m')],stdout=f,stderr=subprocess.STDOUT)
 return r.returncode==0 and log_ok(p,n)
def one(job):
 p,n=job['p'],job['order'];key=p,n;stem=f'p{p}_n{n}';meta=J/f'{stem}.json';seq=J/f'{stem}_sequence.m';w=weight(p);t=time.monotonic()
 if meta.exists()and json.loads(meta.read_text()).get('status')=='PASS':return
 if key in active:
  proc=active[key]
  while True:
   try:
    if not proc.is_running()or proc.status()==psutil.STATUS_ZOMBIE:break
   except psutil.NoSuchProcess:break
   time.sleep(2)
  release(w);ok=log_ok(p,n)and seq.exists();method='adopted native Magma'
 elif log_ok(p,n)and seq.exists():ok=True;method='completed native Magma'
 else:
  acquire(w);f=J/f'{stem}_sparse.txt';log=J/f'{stem}_sparse.log';raw=J/f'{stem}_cpp_raw.m';cpp=J/f'{stem}_cpp.log';bm=J/f'{stem}_bm.log'
  try:
   with log.open('w')as o:r=subprocess.run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'SparseOut:={f}',str(W/'export_large_sparse.m')],stdout=o,stderr=subprocess.STDOUT)
   exported=r.returncode==0 and'S12_SPARSE_EXPORT_COMPLETE'in log.read_text()
  finally:release(w)
  ok=False;method='Magma sparse export; C++ exact arithmetic; Magma Berlekamp-Massey'
  if exported:
   with cpp.open('w')as o:r=subprocess.run([str(W/'krylov'),str(f),str(raw)],stdout=o,stderr=subprocess.STDOUT)
   if r.returncode==0:
    with bm.open('w')as o:r=subprocess.run(['magma','-b',f'Raw:={raw}',f'Final:={seq}',str(W/'finish_cpp.m')],stdout=o,stderr=subprocess.STDOUT)
    ok=r.returncode==0 and'S12_CPP_LINEAR_COMPLEXITY_CERTIFIED'in bm.read_text()
  if ok:
   h=hashlib.sha256(f.read_bytes()).hexdigest();f.unlink();raw.unlink()
  else:
   acquire(w)
   try:ok=native(p,n,seq);method='native Magma fallback'
   finally:release(w)
 dat=job|{'status':'PASS'if ok else'FAIL','method':method,'seconds':time.monotonic()-t,'sequence_sha256':hashlib.sha256(seq.read_bytes()).hexdigest()if seq.exists()else None}
 if 'h'in locals():dat['sparse_export_sha256']=h
 meta.write_text(json.dumps(dat,indent=2)+'\n');print(dat,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=20)as ex:list(ex.map(one,jobs))
rs=[json.loads((J/f"p{j['p']}_n{j['order']}.json").read_text())for j in jobs];ok=all(r['status']=='PASS'for r in rs);(W/'large_native_results.json').write_text(json.dumps({'status':'PASS'if ok else'FAIL','characters':len(rs),'results':rs},indent=2)+'\n');print('S12_CHARACTER_BATCH_COMPLETE',ok,len(rs),flush=True)
