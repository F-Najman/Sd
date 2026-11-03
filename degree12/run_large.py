from pathlib import Path
import subprocess,json,time,concurrent.futures,threading,hashlib
W=Path(__file__).resolve().parent;J=W/'large_orders';jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];cv=threading.Condition();used=0.0
def one(job):
 global used
 p,n=job['p'],job['order'];stem=f'p{p}_n{n}';out=J/f'{stem}.log';meta=J/f'{stem}.json';seq=J/f'{stem}_sequence.m'
 if meta.exists() and json.loads(meta.read_text()).get('status')=='PASS':return
 # The largest-prime benchmark is already running in its own recorded session.
 if (p,n)==(530807,265403):return
 weight=max(3.,85.*(p/530807.)**2)
 with cv:
  while used+weight>215.:cv.wait(10)
  used+=weight
 t=time.monotonic()
 try:
  with out.open('w')as f:r=subprocess.run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',f'SequenceOutput:={seq}',str(W/'large_order.m')],stdout=f,stderr=subprocess.STDOUT)
  ok=r.returncode==0 and f'S12_SELECTED_CHARACTER_NONSTRANGE p={p} order={n} 'in out.read_text()and seq.exists()
  dat=job|{'status':'PASS'if ok else'FAIL','returncode':r.returncode,'seconds':time.monotonic()-t,'sequence_sha256':hashlib.sha256(seq.read_bytes()).hexdigest()if seq.exists()else None};meta.write_text(json.dumps(dat,indent=2)+'\n');print(dat,flush=True)
 finally:
  with cv:used-=weight;cv.notify_all()
with concurrent.futures.ThreadPoolExecutor(max_workers=18)as ex:list(ex.map(one,jobs))
print('S12_SELECTED_CHARACTER_BATCH_FINISHED',flush=True)
