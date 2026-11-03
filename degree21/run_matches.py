from pathlib import Path
import subprocess,json,concurrent.futures
W=Path(__file__).resolve().parent;ns=[n for n in json.loads((W/'local_levels.json').read_text())['levels']if True]
def one(n):
 with(W/f'match{n}.log').open('w')as f:r=subprocess.run(['magma','-b',f'P:={n}',str(W/f'match{n}.m')],stdout=f,stderr=subprocess.STDOUT)
 s=(W/f'match{n}.log').read_text();assert r.returncode==0 and'S21_INHERITED_ORBITS_MATCHED'in s and'Runtime error'not in s,n
 print('S21_MATCH_PASS',n,flush=True);return n
with concurrent.futures.ThreadPoolExecutor(max_workers=1)as ex:a=list(ex.map(one,ns))
(W/'matches_verified.json').write_text(json.dumps({'status':'PASS','levels':a},indent=2)+'\n')
