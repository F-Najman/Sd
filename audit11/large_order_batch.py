from pathlib import Path
import subprocess,concurrent.futures,json,time,sys
W=Path(__file__).resolve().parent;J=W/'large_orders';J.mkdir(exist_ok=True)
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];state={};start=time.monotonic()
def one(job):
 p,n=job['p'],job['order'];key=f'p{p}_n{n}';out=J/f'{key}.log'
 if '--reuse'in sys.argv and out.exists()and'S11_SELECTED_CHARACTER_NONSTRANGE'in out.read_text():return job|{'status':'PASS','reused':True}
 state[key]={'status':'running','started':time.monotonic()-start}
 with out.open('w')as f:r=subprocess.run(['magma','-b',f'P:={p}',f'OrderToTest:={n}',str(W/'large_order.m')],stdout=f,stderr=subprocess.STDOUT)
 s=out.read_text();ok=r.returncode==0 and'S11_SELECTED_CHARACTER_NONSTRANGE'in s
 rec=job|{'status':'PASS'if ok else'FAILED','exit_code':r.returncode,'elapsed':time.monotonic()-start-state[key]['started']};state[key]=rec
 (J/f'{key}.json').write_text(json.dumps(rec,indent=2)+'\n');print('SELECTED_CHARACTER_FINISHED',rec,flush=True)
 (J/'progress.json').write_text(json.dumps(state,indent=2)+'\n')
 return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=16)as ex:results=list(ex.map(one,jobs))
 out={'status':'PASS'if all(r['status']=='PASS'for r in results)else'PARTIAL','characters':len(results),'results':results,'elapsed_seconds':time.monotonic()-start};(J/'all_results.json').write_text(json.dumps(out,indent=2)+'\n');print('S11_SELECTED_CHARACTER_BATCH_COMPLETE',out['status'],len(results),flush=True)
