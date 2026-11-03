from pathlib import Path
import subprocess,concurrent.futures,json
W=Path(__file__).resolve().parent
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]
def one(n):
 with(W/f'inherited{n}.log').open('w')as f:r=subprocess.run(['magma','-b',f'P:={n}',str(W/f'match{n}.m')],stdout=f,stderr=subprocess.STDOUT)
 s=(W/f'inherited{n}.log').read_text();ok='S18_INHERITED_ORBITS_MATCHED'in s;print('S18_INHERITED',n,ok,flush=True);return {'N':n,'status':'PASS'if ok else'FAIL'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(one,ns))
(W/'inherited_verified.json').write_text(json.dumps(rs,indent=2)+'\n')
