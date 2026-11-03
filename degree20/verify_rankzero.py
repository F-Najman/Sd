from pathlib import Path
import json
from sage.all import QQ,matrix
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;records=lit((W/'rankzero_data.m').read_text(),'RankzeroData');out=[]
for p,g,entries in records:
 A=matrix(QQ,g,g,[QQ(a)/QQ(b)for a,b in entries]);assert A.rank()==g==(p-5)*(p-7)//24;out.append({'p':p,'genus':g,'winding_rank':g,'status':'PASS','period_action':'transpose DualHeckeOperator(T2)'})
assert [r['p']for r in out]==[59,71]
(W/'rankzero_verified.json').write_text(json.dumps({'status':'PASS','cases':out},indent=2)+'\n');print('S20_RANKZERO_INDEPENDENT_PASS',flush=True)
