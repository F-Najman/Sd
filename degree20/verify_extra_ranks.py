from pathlib import Path
import gzip,json
from sage.all import GF,matrix,ZZ
W=Path(__file__).resolve().parent;out=[]
for n,kind in [(73,'mixed_pair_'),(109,'mixed_')]:
 H=W/f'full{n}';a=json.loads((H/(kind+'sieve.json')).read_text());assert a['status']=='PASS'and not a['exceptions'];records=json.load(gzip.open(H/(kind+'matrices.json.gz'),'rt'));assert len(records)==a['nonprincipal']
 for r in records:
  M=matrix(GF(2),[ZZ(int(v,16)).digits(2,padto=r['columns'])for v in r['rows']]);assert M.rank()==a['dimension']==r['rank']
 out.append({'N':n,'kind':kind,'status':'PASS','matrices':len(records),'rank':a['dimension']})
assert [r['matrices']for r in out]==[19,2]
(W/'extra_rank_checks.json').write_text(json.dumps({'status':'PASS','matrices':21,'results':out},indent=2)+'\n');print('S20_EXTRA_MIXED_RANKS_INDEPENDENT_PASS 21',flush=True)
