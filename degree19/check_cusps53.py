from pathlib import Path
import json,itertools,subprocess
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;s=(W/'full_cusps53_data.m').read_text();C=lit(s,'RelativeCuspJets');assert len(C)==26
M=len(C[0]);cols=[[sum(row[j]<<i for i,row in enumerate(mat))for j in range(19)]for mat in C]
patterns=[list(map(int,l.split()))for l in(W/'FI/FI53_bad_patterns.txt').read_text().splitlines()];assert len(patterns)==7
p=W/'cusps53_input.txt'
p.write_text(f'{len(patterns)}\n'+'\n'.join(' '.join(map(str,ms))for ms in patterns)+'\n'+'\n'.join(' '.join(str(x>>(64*k)&((1<<64)-1))for k in range(16))for row in cols for x in row)+'\n')
print('S19_CUSPS53_LIFT_COUNTS',[__import__('math').prod(v+1 for v in ms)for ms in patterns],flush=True)
r=subprocess.run([str(W/'cusps53'),str(p)],capture_output=True,text=True);(W/'cusps53.log').write_text(r.stdout+r.stderr)
print(r.stdout,flush=True);assert r.returncode==0
(W/'cusps53_verified.json').write_text(json.dumps({'status':'PASS','quotient_bad_patterns':7,'detail':r.stdout},indent=2)+'\n')
