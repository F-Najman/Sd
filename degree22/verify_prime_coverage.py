"""Independent exhaustive prime ledger; a plan until all certificate guards pass."""
from pathlib import Path
import json,math,hashlib,sys
from fractions import Fraction
from sage.all import prime_range,is_prime,divisors,valuation,factor
W=Path(__file__).resolve().parent;B=W.parents[1];read=lambda p:json.loads(p.read_text());g=read(W/'global_bound.json');assert(g['degree'],g['cap'],g['M'],g['coefficient_rank'])==(22,2099200,229,44)
lower=list(map(int,prime_range(2,54)))+[67];assert lower==read(W/'occurrences_verified.json')['proved_lower_bound'];cases={p:'verified occurrence over an exact degree22 field'for p in lower};table={};ps=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if' p&'in line:ps=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif'\\ord(\\chi)&'in line:
  vv=[math.lcm(*map(int,v.split(',')))for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(ps)==len(vv);table.update(zip(ps,vv))
assert len(table)==74;cm={int(p)for d in divisors(22)if d%2==0 for p in[2*d+1,3*d+1]if is_prime(p)};assert cm=={5,7,67}
for z in g['excluded']:
 p,t=z['p'],z['strangeness'];assert is_prime(p)and 53<p<100000 and p not in cases and p not in cm and t==table.get(p,1)
 if z['reason']=='Corollary7.5':assert p*p>Fraction(2**19,325)*22+1 and 22%((p-1)//(2*t))
 else:
  ell=int(z['reason'].split('=')[1]);assert ell in[2,3]and t==1
  if ell==2:assert p<=157
  assert Fraction(325*(p*p-1),65536)>(2*ell+1)*22;order=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1]);assert all(22%(order//a)for a in[1,2,3]if order%a==0)
 cases[p]=z['reason']
Ns=read(W/'local_levels.json')['levels'];assert g['local_levels']==Ns+[163,167,173,181]
for p in Ns+[163,167,173,181]:assert p not in cases;cases[p]='local or additional global certificate'
sel=read(W/'large_selected_orders.json');assert len(sel['primes'])==1488 and(len(sel['jobs']),len(sel['reused']))==(5018,5047)
for z in sel['primes']:
 p,r,v,w,th=[z[k]for k in['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2;assert is_prime(p)and is_prime(r)and valuation(m,r)==v and valuation(22,r)==w and th==v-w>0;assert[int(n)for n in divisors(m)if n%(r**th)==0]==z['orders']and p*p>Fraction(2**19,325)*22+1 and p not in cases;cases[p]='selected nonstrange-character family'
assert sorted(z['p']for z in sel['primes'])==g['large_screen_primes']and 599479 in g['large_screen_primes']
# Independently bound every smaller SS and toric group, including odd f17.
ss={}
for f in range(1,23):
 q=2**f;ss[f]=[q+1+j*2**(f//2)for j in[-2,-1,0,1,2]]if f%2==0 else[q+1+j*2**((f+1)//2)for j in[-1,0,1]]
 # Small f may have duplicate/degenerate formal trace options. They are only
 # overestimates here, and the Hasse bound itself suffices below f17.
 if f>=17 and f not in[18,19,20,21,22]:assert max(int(p)for n in ss[f]for p,e in factor(n))<100000
 if f>=18:assert ss[f]==g['supersingular_orders'][str(f)]
assert max(int(p)for f in range(17,23)for n in ss[f]for p,e in factor(n))==599479<2099200
assert max(int(p)for f in range(1,23)for n in[2**f-1,2**f+1]if n>1 for p,e in factor(n))<2099200
allss=[n for f in range(18,23)for n in ss[f]];large=set(g['large_screen_primes']);dyadic=set(g['large_dyadic_excluded'])
for p in map(int,prime_range(100000,2099201)):
 ordinary=False
 for f in range(18,23):
  q=2**f;t=math.isqrt(4*q);lo=(q+1-t+p-1)//p;hi=(q+1+t)//p;ordinary|=lo+lo%2<=hi
 good=ordinary or any(n%p==0 for n in allss);toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,23))
 if good or toric:assert p in large and p in cases
 else:assert p in dyadic and p not in cases;cases[p]='dyadic parity, SS and toric orders, single-cusp immersion'
primes=list(map(int,prime_range(2,2099201)));assert set(cases)==set(primes)
plan={'status':'EXHAUSTIVE_PRIME_PLAN_PENDING_CERTIFICATES','degree':22,'prime_count':len(primes),'cap':2099200,'large_primes':1488,'selected_character_orders':10065,'new_character_orders':5018,'reused_character_orders':5047,'CM_possible_primes_for_divisors_of22':sorted(cm),'cases':[{'p':p,'reason':cases[p]}for p in primes],'input_sha256':{f:hashlib.file_digest((W/f).open('rb'),'sha256').hexdigest()for f in ['global_bound.json','large_selected_orders.json','occurrences_verified.json','local_levels.json','../audit11/derickx_stoll_table2.txt']},'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(W/'prime_coverage_plan.json').write_text(json.dumps(plan,indent=2)+'\n');print('S22_EXHAUSTIVE_PRIME_PLAN_COMPLETE',len(primes),flush=True)
