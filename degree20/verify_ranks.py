from pathlib import Path
import json,gzip,time
from sage.all import matrix,GF,ZZ
W=Path(__file__).resolve().parent;F=GF(2);tt=time.monotonic();tasks=[(53, ''), (59, ''), (67, ''), (71, ''), (73, ''), (79, ''), (83, ''), (89, ''), (97, ''), (101, ''), (103, ''), (107, ''), (109, ''), (113, ''), (127, ''), (131, ''), (137, ''), (139, ''), (53, 'pair_'), (59, 'pair_'), (67, 'pair_'), (71, 'pair_'), (73, 'pair_'), (79, 'pair_'), (83, 'pair_'), (89, 'pair_'), (97, 'pair_'), (101, 'pair_'), (103, 'pair_'), (107, 'pair_'), (113, 'pair_'), (127, 'pair_'), (131, 'pair_'), (137, 'pair_'), (139, 'pair_low_'), (73, 'mixed_'), (89, 'mixed_'), (113, 'mixed_'), (127, 'mixed_')];done={}
while len(done)<len(tasks):
 progress=False
 for n,kind in tasks:
  if(n,kind)in done:continue
  H=W/f'full{n}';log=H/(kind+'sieve.log');p=H/(kind+'matrices.json.gz');jp=H/(kind+'sieve.json')
  if not(p.exists()and log.exists()and'AUDIT_FULL_SIEVE_COMPLETE'in log.read_text()):continue
  a=json.loads(jp.read_text());ms=json.load(gzip.open(p,'rt'));assert len(ms)==a['nonprincipal'];seen=set()
  for v in ms:
   key=tuple(v['source'])if isinstance(v['source'],list)else v['source'];assert key not in seen;seen.add(key);rows=[ZZ(int(z,16))for z in v['rows']];assert len(rows)==a['dimension'];A=matrix(F,[z.digits(2,padto=v['columns'])for z in rows]);assert A.ncols()==v['columns']and A.rank()==a['dimension']==v['rank']
  rec={'N':n,'kind':kind or'ordinary','matrices':len(ms),'rank':a['dimension'],'status':'PASS'};done[n,kind]=rec;progress=True;print('S20_RANK_INDEPENDENT_PASS',rec,'elapsed',round(time.monotonic()-tt,1),flush=True);(W/'independent_rank_progress.json').write_text(json.dumps(list(done.values()),indent=2)+'\n')
 if not progress:time.sleep(5)
out={'status':'PASS','results':sorted(done.values(),key=lambda z:(z['N'],z['kind'])),'matrices':sum(v['matrices']for v in done.values())};(W/'independent_rank_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('S20_ALL_NEW_OBSTRUCTION_MATRICES_VERIFIED',out['matrices'],flush=True)
