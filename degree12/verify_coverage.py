from pathlib import Path
import json,math,re,sys
from sage.all import prime_range,GF,matrix,divisors
W=Path(__file__).resolve().parent;B=W.parents[1];cap=532900;S={2,3,5,7,11,13,17,19,23,29,31,37,43};local=[41,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109];cases={p:'occurrence'for p in S}
def add(p,kind):assert p not in cases,(p,kind,cases.get(p));cases[p]=kind
assert 'S12_OCCURRENCE_43_VERIFIED'in(W/'occurrence43.log').read_text()
for p in[23,29,31]:assert f'S12_OCCURRENCE_VERIFIED prime={p} exact_field_degree=12 exact_point_order=true'in(W/'verify_small_witnesses.log').read_text()
fi=json.loads((W/'formal_immersion_final.json').read_text());assert fi['status']=='PASS'and{r['N']for r in fi['results']}==set(local)and all(r['status']=='PASS'for r in fi['results'])
ri=json.loads((W/'independent_rank_checks.json').read_text());assert ri['status']=='PASS'and{r['N']for r in ri['results']}==set(local);assert sum(r['matrices']for r in ri['results'])==298
for p in local:
 d=json.loads((W/f'full{p}/sieve.json').read_text());assert d['status']=='PASS'and d['nonprincipal']==d['source_orbits']and not d['exceptions'];add(p,'complete local exclusion at 2')
assert 'S12_EXCEPTIONAL_STABILIZERS_COMPLETE'in(W/'stabilizers.log').read_text()
assert 'S12_ALL_REDUCTION_SUPPORTS_CLASSIFIED'in(W/'classify_supports.log').read_text()
assert 'AUDIT_ALL_UNIT_POLE_BOUNDS_COMPLETE'in(W/'unit_poles.log').read_text()
for file,marker in [('supersingular41.log','NONIC_PRIME_TEST_RESULT N=41 degree=5 index=1 q=3 principal=false'),('P41_cusps.log','DECIC41_NONRATIONAL_CUSP A3_principal=false'),('P41_NC5_clean.log','DECIC41_NC5_COMPLETE')]:assert marker in(B/'work/audit11'/file).read_text()
pub=json.loads((W/'published_prime_bound.json').read_text());assert pub['status']=='PASS'
for r in pub['midrange']:add(r['p'],'published strange-character table')
for r in pub['small_global']:add(r['p'],'diamond-2 orbit and gonality bound')
ss={}
for ell,d,cs in re.findall(r'S12_SS ell=(\d+) d=(\d+) orders=(\[.*?\])',(W/'ss_orders.log').read_text()):ss[int(ell),int(d)]=json.loads(cs)
for ell,M in[(3,61),(5,59),(7,59)]:
 for u in range(1,M):assert matrix(GF(ell),[[int(n*a%M>M//2)-int(n*u*pow(a,-1,M)%M>M//2)for a in range(1,M)]for n in range(1,13)]).rank()==12
def admissible(p,ell):
 for d in range(1,13):
  q=ell**d
  if (q-1)%p==0 or(q+1)%p==0:return True
  rad=math.isqrt(4*q);low=max(1,(q+1-rad+p-1)//p);high=(q+1+rad)//p
  for mult in range(low,high+1):
   trace=q+1-mult*p
   if trace%ell or any(c%p==0 for c in ss.get((ell,d),[])):return True
 return False
data=json.loads((W/'large_filter.json').read_text());assert data['cap']==cap and data['degree']==12
for r in data['excluded']:assert not admissible(r['p'],r['ell']);add(r['p'],'odd-characteristic formal immersion and reduction orders')
sel=json.loads((W/'large_selected_orders.json').read_text());assert{r['p']for r in sel['primes']}=={r['p']for r in data['survivors']}and len(sel['primes'])==92
verified=json.loads((W/'large_verified.json').read_text());have={(r['p'],r['order'])for r in verified['results']};pending=[]
for r in sel['primes']:
 p=r['p'];assert all(admissible(p,ell)for ell in[3,5,7])
 if all((p,n)in have for n in r['orders']):add(p,'verified character-order omission and Corollary 7.5')
 else:pending.append(p)
primes=set(map(int,prime_range(2,cap+1)));assert set(cases).isdisjoint(pending)and set(cases)|set(pending)==primes
cleanup=W/'scheduler_cleanup.json';clean=cleanup.exists()and json.loads(cleanup.read_text())['status']=='PASS'
status='PASS'if not pending and verified['status']=='PASS'and clean else'PARTIAL';out={'status':status,'degree':12,'occurring_primes':sorted(S),'oesterle_bound':cap,'covered_primes':len(cases),'all_primes_under_bound':len(primes),'pending_primes':pending,'clean_regeneration_complete':clean,'cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]};(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S12_FINAL_COVERAGE',status,len(cases),'/',len(primes),'pending',len(pending),'clean_regeneration',clean,flush=True)
if '--available-only'not in sys.argv:assert status=='PASS',pending
