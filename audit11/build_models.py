from pathlib import Path
import subprocess,concurrent.futures,json,time
W=Path(__file__).resolve().parent;L=Path('/home/fnajman/degree9_torsion/nonic-torsion')
def one(n):
 h=W/f'full{n}';t=time.monotonic()
 with open(h/'build.log','w')as f:r=subprocess.run(['magma','-b',str(h/'build.m')],cwd=L,stdout=f,stderr=subprocess.STDOUT)
 s=(h/'build.log').read_text();ok=f'AUDIT_FULL_MODEL_COMPLETE N={n}'in s and not any(x in s for x in['Runtime error','User error','Traceback']);rec={'N':n,'status':'PASS'if ok else'FAIL','exit':r.returncode,'elapsed':time.monotonic()-t};print('AUDIT_MODEL',rec,flush=True);return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(one,[37,41,43,47,53,59,61,67,71,73,79,83,89]))
 (W/'model_build_results.json').write_text(json.dumps(rs,indent=2)+'\n')
