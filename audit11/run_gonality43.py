from pathlib import Path
import concurrent.futures,subprocess,json,time
W=Path(__file__).resolve().parent
def one(i):
 t=time.monotonic();out=W/f'gon43_{i}.m';log=W/f'gon43_{i}.log'
 with log.open('w')as f:r=subprocess.run(['magma','-b',f'Part:={i}','Parts:=8',f'Out:={out}',str(W/'gonality43.m')],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();ok=f'AUDIT_GON43_PART_COMPLETE part={i}'in s and not any(x in s for x in['User error','Runtime error']);rec={'part':i,'status':'PASS'if ok else'FAIL','elapsed':time.monotonic()-t};print(rec,flush=True);return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:rs=list(ex.map(one,range(1,9)))
 (W/'gon43_results.json').write_text(json.dumps(rs,indent=2)+'\n')
