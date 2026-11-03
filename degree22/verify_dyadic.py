from pathlib import Path
import json
from sage.all import GF,matrix,ZZ,PolynomialRing,EllipticCurve,factor
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;a=json.loads((W/'dyadic_jets.json').read_text());assert(a['m'],a['M'],a['p_cutoff'])==(44,229,20152);F=GF(2)
for rec in a['classes']:
 u=rec['u'];rr=[]
 for n in range(1,45):rr.append(sum((int(n*k%229>=115)^int(n*u*pow(k,-1,229)%229>=115))<<(k-1)for k in range(1,229)))
 assert rr==[int(z,16)for z in rec['rows']]and matrix(F,[ZZ(x).digits(2,padto=228)for x in rr]).rank()==44
assert [r['u']for r in a['classes']]==list(range(1,229))
print('S22_DYADIC_INDEPENDENT_PASS 228 rank44 cutoff20152',flush=True)
tw=lit((W/'bound_ss_data.m').read_text(),'BoundTwistData');results=[];PR=PolynomialRing(F,'t')
for d,poly,curves in tw:
 K=GF(2**d,name='a',modulus=PR(poly));orders=[]
 for aa,N in curves:
  E=EllipticCurve(K,[K(PR(c))for c in aa]);assert E.j_invariant()==0 and E.cardinality()==N;orders.append(N)
 expected=([2**d+1-2**((d+1)//2),2**d+1,2**d+1+2**((d+1)//2)]if d%2 else[2**d+1+j*2**(d//2)for j in [-2,-1,0,1,2]])
 assert sorted(set(orders))==expected and len(orders)==(3 if d%2 else 7)
 if d==22:assert max(int(p)for v in orders for p,e in factor(v))==599479<2099200
 results.append({'degree':d,'orders':sorted(set(orders)),'all_native_curves_independently_counted':True});print('S22_SS_BOUND_INDEPENDENT_PASS',d,flush=True)
(W/'dyadic_independent.json').write_text(json.dumps({'status':'PASS','degree':22,'matrix_classes':228,'rank':44,'M':229,'cutoff':20152,'supersingular_orders':results},indent=2)+'\n')
