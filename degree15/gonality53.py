from pathlib import Path
import sys,json,re,subprocess
from sage.all import matrix,GF
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import matbits,xorrows
s=(W/'full53/units_data.m').read_text();Q=matbits(s,'qcoeffs');D=matbits(s,'DiamondMatrix');g=len(Q);assert g==92
cols=[[int(v>>n&1)for v in Q]for n in range(1,10)];orbit=[]
for k in range(26):
 orbit.append([sum(v<<i for i,v in enumerate(c))for c in cols]);cols=[[xorrows(r,c)for r in D]for c in cols]
assert cols==[[int(v>>n&1)for v in Q]for n in range(1,10)]
base={}
def red(v):
 while v:
  j=v.bit_length()-1
  if j in base:v^=base[j]
  else:break
 return v
for rr in orbit:
 v=red(rr[0]);assert v;base[v.bit_length()-1]=v
assert len(base)==26
# Fully reduce against all base pivots, so the quotient coordinates are linear.
def quotient(v):
 for k,b in sorted(base.items(),reverse=True):
  if v>>k&1:v^=b
 return v
rows=[quotient(v)for v in orbit[0][1:9]]+[quotient(v)for rr in orbit[1:]for v in rr[1:5]]
rank=matrix(GF(2),[[v>>j&1 for j in range(g)]for v in rows]).rank();p=W/'gon53.compressed.txt';p.write_text(f'53 26 0 0 {len(rows)} {g} 8 {rank}\n'+'\n'.join(' '.join(str(v>>(64*k)&((1<<64)-1))for k in range(8))for v in rows)+'\n')
r=subprocess.run([str(W/'gon_prefixes'),str(p)],capture_output=True,text=True);(W/'gonality53_prefix.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stdout
expected=0
for first in range(1,9):
 cc=[1]+[0]*8
 for _ in range(25):cc=[sum(cc[t-k]for k in range(min(t,first,4)+1))for t in range(9)]
 expected+=cc[8-first]
assert expected>0 and f'checked={expected} status=PASS'in r.stdout
out={'status':'PASS','independent_expected_tuples':expected,'gonality_lower_bound':18,'rational_cusps':26,'no_other_places_degree_at_most':8,'base_rank':26,'extra_rank':int(rank),'maximum_excess_degree':8,'pigeonhole_distinct_rational_poles':9,'prefix_result':r.stdout};(W/'gonality53.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
