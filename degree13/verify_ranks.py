from pathlib import Path
import gzip,json
from sage.all import matrix,GF
W=Path(__file__).resolve().parent;out=[]
for h in sorted([x for x in W.glob('full*')if x.is_dir()],key=lambda x:int(x.name[4:])):
 import time
 while not(h/'sieve.json').exists():time.sleep(2)
 s=json.loads((h/'sieve.json').read_text());ms=json.load(gzip.open(h/'matrices.json.gz','rt'))
 for m in ms:
  M=matrix(GF(2),[[int(v,16)>>j&1 for j in range(m['columns'])]for v in m['rows']]);assert M.nrows()==M.rank()==s['dimension']
 out.append({'N':s['N'],'matrices':len(ms),'rank':s['dimension'],'status':'PASS'});print(out[-1],flush=True)
assert len(out)==18
(W/'independent_rank_checks.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n')
