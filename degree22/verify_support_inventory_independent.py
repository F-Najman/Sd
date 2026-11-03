"""Independent support enumeration from class counts and Sage partitions."""
from pathlib import Path
import json,itertools
from sage.all import Partitions,divisors,Mod
W=Path(__file__).resolve().parent;A=json.loads((W/'census_counts_independent.json').read_text());assert A['status']=='PASS';inv=json.loads((W/'support_inventory.json').read_text());plans={a['p']:a for a in inv['levels']};out=[];total_count=0
for a in A['results']:
 p=a['p'];assert p in plans;v=plans[p];counts={int(z['degree']):int(z['rational_ordinary_points'])for z in a['ordinary_counts']};closed={}
 for d in range(1,23):
  n=counts[d]-sum(e*closed[e]for e in map(int,divisors(d))if e<d);assert n>=0 and n%d==0;closed[d]=n//d
 ordinary=[d for d,n in closed.items()if n];ss=sorted({int(d)for d,orb in a['supersingular_closed_diamond_orbits']if d<=22});o=int(Mod(2,p).multiplicative_order());nc=o//2 if o%2==0 else o;assert pow(2,nc,p)in[1,p-1]
 assert ordinary==v['ordinary_degrees']and ss==v['supersingular_degrees']and nc==v['NC_degree'];types=[('O',d)for d in ordinary]+[('SS',d)for d in ss]+([('NC',nc)]if nc<=22 else[]);assert[list(t)for t in types]==v['types'];idx={z:i for i,z in enumerate(types)};bydegree={d:[z for z in types if z[1]==d]for t,d in types};expected=set()
 for n in range(23):
  for lam in Partitions(n):
   parts=list(map(int,lam))
   if any(d not in bydegree for d in parts):continue
   for labels in itertools.product(*(bydegree[d]for d in parts)):
    key=tuple(sorted(labels,key=idx.__getitem__));expected.add((key,22-n))
 actual={(tuple(tuple(z)for z in r['support']),r['cusp_complement'])for r in v['cases']};assert expected==actual and len(actual)==len(v['cases']);total_count+=len(actual);out.append({'p':p,'support_types':len(actual),'independent_closed_ordinary_counts':closed,'SS_degrees':ss,'NC_degree':nc});print('S22_INDEPENDENT_SUPPORT_PARTITIONS',p,len(actual),flush=True)
assert total_count==514;z={'status':'PASS','degree':22,'support_types':514,'method':'Möbius inversion of independent class-number point counts, independent quaternion SS orbits, multiplicative order, and all Sage integer partitions with all type assignments','levels':out};(W/'symmetric_supports_independent.json').write_text(json.dumps(z,indent=2)+'\n');print('S22_ALL514_SUPPORTS_INDEPENDENTLY_ENUMERATED',flush=True)
