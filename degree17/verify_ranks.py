from pathlib import Path
import json,gzip,time
from sage.all import matrix,GF
W=Path(__file__).resolve().parent;out=[]
for n in[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]:
 H=W/f'full{n}'
 while not(H/'sieve.json').exists():time.sleep(1)
 a=json.load(open(H/'sieve.json'))
 for kind in['','pair_','mixed_']:
  p=H/(kind+'matrices.json.gz')
  required=kind=='' or(kind=='mixed_'and n in[73,127]) or(kind=='pair_'and n in[47,59,61,67,71,73,113,127])
  if required:
   while not p.exists()or'AUDIT_FULL_SIEVE_COMPLETE'not in(H/(kind+'sieve.log')).read_text():time.sleep(5)
  elif not p.exists():continue
  ms=json.load(gzip.open(p,'rt'))
  for v in ms:
   rows=[int(z,16)for z in v['rows']];A=matrix(GF(2),[[z>>j&1 for j in range(v['columns'])]for z in rows]);assert A.rank()==a['dimension']
  out.append({'N':n,'kind':kind or'ordinary','matrices':len(ms),'rank':a['dimension'],'status':'PASS'});print(out[-1],flush=True)
for n in[59,61,67,71,73]:
 H=W.parent/f'degree14/full{n}';a=json.load(open(H/'sieve.json'));ms=json.load(gzip.open(H/'pair_matrices.json.gz','rt'))
 for v in ms:
  rows=[int(z,16)for z in v['rows']];assert matrix(GF(2),[[z>>j&1 for j in range(v['columns'])]for z in rows]).rank()==a['dimension']
 out.append({'N':n,'kind':'borrowed_7plus7','matrices':len(ms),'rank':a['dimension'],'status':'PASS'});print(out[-1],flush=True)
for n in[59,61,67,71]:
 H=W.parent/f'degree15/full{n}';a=json.load(open(H/'sieve.json'));ms=json.load(gzip.open(H/'pair_matrices.json.gz','rt'))
 for v in ms:
  rows=[int(z,16)for z in v['rows']];assert matrix(GF(2),[[z>>j&1 for j in range(v['columns'])]for z in rows]).rank()==a['dimension']
 out.append({'N':n,'kind':'borrowed_7plus8','matrices':len(ms),'rank':a['dimension'],'status':'PASS'});print(out[-1],flush=True)
(W/'independent_rank_checks.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n');print('S17_ALL_PRINCIPAL_DIVISOR_MATRICES_INDEPENDENTLY_VERIFIED',sum(v['matrices']for v in out),flush=True)
