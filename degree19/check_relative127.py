from pathlib import Path
import sys,itertools,json
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
s=(W/'relative127_data.m').read_text();B=lit(s,'Relative127Base');C=lit(s,'Relative127CuspJets');assert len(C)==63

def rank(rr):
 b={}
 for x in rr:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return len(b)
base=[sum(v<<j for j,v in enumerate(row))for row in B];assert rank(base)==14;counts={};bad=[]
for positions in itertools.combinations_with_replacement(range(63),3):
 counts0={k:positions.count(k)for k in set(positions)};rows=base[:];width=16
 for k,m in sorted(counts0.items()):rows=[v|sum(C[k][i][j]<<(width+j)for j in range(m))for i,v in enumerate(rows)];width+=m
 assert width==19
 r=rank(rows);counts[r]=counts.get(r,0)+1
 if r!=17:bad.append([positions,r])
out={'status':'PASS'if not bad else'FAIL','degree':19,'family_dimension':2,'relative_rank':17,'patterns_checked':sum(counts.values()),'ranks':counts,'failures':bad};(W/'relative127_verified.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
