from pathlib import Path
import itertools,json,sys
from unit_arithmetic import lit
W=Path(__file__).resolve().parent

def rank(rows):
 b={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 return len(b)

out=[]
for p,r in [(53,1),(61,3)]:
 s=(W/f'relative{p}_data.m').read_text();ss=lit(s,'RelativeSSMatrices');cusps=lit(s,'RelativeCuspJets');d=int(lit(s,'RelativeSSDegree'));c=18-d;cnt=0;bad=[];ranks={}
 for si,mat in enumerate(ss):
  base=[sum(v<<j for j,v in enumerate(row))for row in mat]
  assert rank(base)==d-r
  for positions in itertools.combinations_with_replacement(range(len(cusps)),c):
   counts={k:positions.count(k)for k in set(positions)};rows=base[:];width=d
   for k,m in sorted(counts.items()):
    rows=[x|sum(cusps[k][i][j]<<(width+j)for j in range(m))for i,x in enumerate(rows)];width+=m
   assert width==18;rr=rank(rows);ranks[rr]=ranks.get(rr,0)+1
   if rr!=18-r:bad.append({'ss_translate':si,'cusps':positions,'rank':rr})
   cnt+=1
 rec={'p':p,'family_dimension':r,'expected_rank':18-r,'patterns_checked':cnt,'ranks':ranks,'failures':bad,'status':'PASS'if not bad else'FAIL'}
 (W/f'relative{p}_verified.json').write_text(json.dumps(rec,indent=2)+'\n');print(rec if not bad else {**rec,'failures':bad[:10]},flush=True);out.append(rec)
(W/'relative_verified.json').write_text(json.dumps(out,indent=2)+'\n')
