from pathlib import Path
import json,gzip,hashlib,shutil
from sage.all import matrix,GF,PolynomialRing,QQ
W=Path(__file__).resolve().parent;H=W/'full97'
a=json.load(open(H/'sieve.json'))
if a.get('combined_independently_verified')and not a['exceptions']:
 proof=json.load(open(W/'operator97_verified.json'));assert proof['status']=='PASS'and proof['certificate_sha256']==hashlib.sha256((H/'matrices.json.gz').read_bytes()).hexdigest();print('S17_CORRECTED97_COMBINED_ALREADY_VERIFIED',flush=True);raise SystemExit(0)
ms=json.load(gzip.open(H/'matrices.json.gz','rt'));b=json.load(open(H/'cyclotomic_sieve.json'));bs=json.load(gzip.open(H/'cyclotomic_matrices.json.gz','rt'))
assert a['source_orbits']==359 and a['nonprincipal']==356 and len(ms)==356 and [(v['source'],v['degree'],v['orbit'])for v in a['exceptions']]==[(2,10,24),(3,10,24),(41,14,24)]
assert b['source_orbits']==b['nonprincipal']==len(bs)==3 and not b['exceptions'];assert {v['source']for v in b['results']}=={2,3,41}
R=PolynomialRing(QQ,'x');x=R.gen();alt=(x-1)*(x**4-x*x+1);primary=x**12-1;assert primary%alt==0 and alt(1)==0
for f in['sieve.json','matrices.json.gz']:shutil.copy2(H/f,H/('primary_'+f))
updates={v['source']:v for v in b['results']};witness={v['source']:v for v in ms};witness.update({v['source']:v for v in bs});results=[];combined=[]
for r in a['results']:
 si=r['source'];v=(updates[si]if si in updates else r).copy();v['operator']='(sigma-1)*Phi12(sigma)'if si in updates else'sigma^12-1';results.append(v);m=witness[si].copy();m['operator']=v['operator'];combined.append(m)
for v in combined:
 rows=[int(s,16)for s in v['rows']];A=matrix(GF(2),[[z>>j&1 for j in range(v['columns'])]for z in rows]);assert A.rank()==345
out=a.copy();out.update(status='PASS',nonprincipal=359,exceptions=[],results=results,alternative_alpha_coefficients=b['alpha_coefficients'],alternative_sources=[2,3,41],operator_counts={'sigma^12-1':356,'(sigma-1)*Phi12(sigma)':3},combined_independently_verified=True)
(H/'sieve.json').write_text(json.dumps(out,indent=2)+'\n')
with gzip.open(H/'matrices.json.gz.tmp','wt')as f:json.dump(combined,f,separators=(',',':'))
(H/'matrices.json.gz.tmp').replace(H/'matrices.json.gz')
proof={'status':'PASS','ordinary_orbits':359,'matrices':359,'rank':345,'operators':out['operator_counts'],'primary_coefficients':a['alpha_coefficients'],'alternative_coefficients':b['alpha_coefficients'],'certificate_sha256':hashlib.sha256((H/'matrices.json.gz').read_bytes()).hexdigest()};(W/'operator97_verified.json').write_text(json.dumps(proof,indent=2)+'\n');print('S17_CORRECTED97_COMBINED_COMPLETE',proof,flush=True)
