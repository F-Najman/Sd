from pathlib import Path
import json,gzip,time
from sage.all import matrix,GF,ZZ
W=Path(__file__).resolve().parent;F=GF(2);tt=time.monotonic();out=[]
# Descending order lets the independent check follow the completed large levels.
for n in[131,127,113,109,107,103,101,97,89,83,79,73,71,67,61,59,53,47]:
 H=W/f'full{n}'
 for kind in['','pair_','mixed_']:
  required=kind==''or(kind=='pair_'and n in[47,53,59,61,67,71,73,79,83,89,127,131])or(kind=='mixed_'and n in[73,113,127])
  if not required:continue
  log=H/(kind+'sieve.log');p=H/(kind+'matrices.json.gz');jp=H/(kind+'sieve.json')
  while not p.exists()or not log.exists()or'AUDIT_FULL_SIEVE_COMPLETE'not in log.read_text():time.sleep(5)
  a=json.loads(jp.read_text());ms=json.load(gzip.open(p,'rt'));assert len(ms)==a['nonprincipal'];seen=set()
  for v in ms:
   key=tuple(v['source'])if isinstance(v['source'],list)else v['source'];assert key not in seen;seen.add(key);rows=[ZZ(int(z,16))for z in v['rows']];assert len(rows)==a['dimension'];A=matrix(F,[z.digits(2,padto=v['columns'])for z in rows]);assert A.ncols()==v['columns']and A.rank()==a['dimension']==v['rank']
  rec={'N':n,'kind':kind or'ordinary','matrices':len(ms),'rank':a['dimension'],'status':'PASS'};out.append(rec);print('S18_RANK_INDEPENDENT_PASS',rec,'elapsed',round(time.monotonic()-tt,1),flush=True)
  (W/'independent_rank_progress.json').write_text(json.dumps(out,indent=2)+'\n')
(W/'independent_rank_checks.json').write_text(json.dumps({'status':'PASS','results':out,'matrices':sum(v['matrices']for v in out)},indent=2)+'\n');print('S18_ALL_NEW_OBSTRUCTION_MATRICES_INDEPENDENTLY_VERIFIED',sum(v['matrices']for v in out),flush=True)
