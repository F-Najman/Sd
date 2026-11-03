from pathlib import Path
import json,gzip,time
from sage.all import matrix,GF,ZZ
W=Path(__file__).resolve().parent;H=W/'full131';log=H/'pair_low_sieve.log';tt=time.monotonic()
while not log.exists()or'AUDIT_FULL_SIEVE_COMPLETE'not in log.read_text():time.sleep(5)
a=json.loads((H/'pair_low_sieve.json').read_text());ms=json.load(gzip.open(H/'pair_low_matrices.json.gz','rt'));assert a['dimension']==651 and len(a['results'])==1042 and not a['exceptions']and a['nonprincipal']==len(ms)==1042
for i,v in enumerate(ms):
 rr=[ZZ(int(z,16)).digits(2,padto=v['columns'])for z in v['rows']];A=matrix(GF(2),rr);assert A.nrows()==651 and A.rank()==651
 if i%100==99:print('S18_LOW131_RANKS',i+1,flush=True)
out={'status':'PASS','N':131,'kind':'pair_low_','totals':[16,17],'matrices':1042,'rank':651};(W/'independent_rank_low131.json').write_text(json.dumps(out,indent=2)+'\n');print('S18_ALL_LOW131_MATRICES_INDEPENDENTLY_VERIFIED',round(time.monotonic()-tt,1),flush=True)
