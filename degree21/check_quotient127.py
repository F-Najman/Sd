from pathlib import Path
import itertools,json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;s=(W/'quotient127_cusps_data.m').read_text();RC=lit(s,'Q127RC');NC=lit(s,'Q127NC');M=RC+NC;cols=[[sum(row[j]<<i for i,row in enumerate(mat))for j in range(3)]for mat in M]
def rank(rr):
 b={}
 for x in rr:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return len(b)
results=[]
for pos in itertools.combinations_with_replacement(range(18),3):
 mult={i:pos.count(i)for i in set(pos)};r=rank([v for i,c in mult.items()for v in cols[i][:c]]);results.append({'positions':pos,'rank':r})
a={'status':'PASS'if all(r['rank']==3 for r in results)else'FAIL','quotient_genus':88,'degree':3,'patterns':len(results),'results':results};(W/'quotient127_cusps_verified.json').write_text(json.dumps(a,indent=2)+'\n');print('S21_QUOTIENT127_CUSP_RANKS',a['status'],len(results),[(r['positions'],r['rank'])for r in results if r['rank']!=3],flush=True)
