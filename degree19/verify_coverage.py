"""Complete prime, source, support and certificate audit for degree19."""
from pathlib import Path
import sys,json,re,math,hashlib
from fractions import Fraction
from sage.all import prime_range,is_prime,divisors,valuation
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;B=W.parents[1];O=W.parent/'degree18';Ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137];oldNs=Ns[:-1]
def read(p):return json.loads(p.read_text())
def mark(p,needle):
 s=p.read_text();assert needle in s and not any(e in s for e in['Runtime error','User error','Assertion failed','Traceback','System Error']),str(p)
def src(folder,n):return lit((folder/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
def good(p):assert read(p)['status']=='PASS',str(p)
for p,needle in[(W/'verify_small_occurrences.log','S19_SMALL_OCCURRENCES_AND_RIEMANN_ROCH_BOUND_VERIFIED'),(W/'verify_occurrences.log','S19_ALL_OCCURRENCES_COMPLETE'),(W/'census_sources.log','S19_ALL_FINITE_SOURCE_ORBITS_COMPLETE'),(W/'bound_ss.log','S19_SS19_ORDERS_COMPLETE'),(W/'stabilizers.log','S19_ALL_STABILIZERS_COMPLETE'),(W/'stabilizers127.log','S19_ALL_STABILIZERS_COMPLETE'),(W/'stabilizer137_ordinary.log','S19_ORDINARY137_STABILIZER_EXCLUSION'),(W/'verify_anti163_norms.log','S19_GLOBAL163_EXCLUSION_CERTIFIED')]:mark(p,needle)
for name in['inherited_manifest_verified.json','auxiliary_verified.json','jet_inverse_replay_verified.json','record_compaction_verified.json','fi_matrices_independent.json','cusps53_verified.json','cusps53_intrinsic_verified.json','relative73_relations_verified.json','relative73_relation_spaces_independent.json','relative73_nc_intrinsic_verified.json','relative127_intrinsic_verified.json','relative_cusps_intrinsic_verified.json','anti163_norms_verified.json']:good(W/name)
for n in[53,61,127]:good(W/f'relative{n}_verified.json')
a=read(W/'relative73_relations_verified.json');assert len(a['profiles'])==148 and all(x['status']=='PASS'for x in a['profiles'])
assert [(r['p'],r['cusp_patterns'],r['relative_rank'])for r in read(W/'relative_cusps_intrinsic_verified.json')['results']]==[(103,153,18),(131,18564,18)]
assert read(W/'relative53_verified.json')['patterns_checked']==76256 and read(W/'relative53_verified.json')['expected_rank']==18
assert read(W/'relative61_verified.json')['patterns_checked']==4119 and read(W/'relative61_verified.json')['expected_rank']==16
assert read(W/'relative127_verified.json')['patterns_checked']==43680 and read(W/'relative127_verified.json')['relative_rank']==17
assert read(W/'cusps53_intrinsic_verified.json')['lifts_independently_rank_checked']==20444
assert len((W/'FI/FI53_bad_patterns.txt').read_text().splitlines())==7
assert [r['N']for r in read(W/'occurrences.json')]==[23,29,31,37,41,43]
parent=read(O/'final_coverage.json');assert parent['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'and(parent['ordinary_source_orbits'],parent['ordinary_nonprincipal'])==(14024,14022)
for name in['operator_annihilation_verified.json','operator97_verified.json']:good(W.parent/'degree17'/name)
assert read(W/'inherited_manifest_verified.json')['files']==3782
rs={};newOrd=0;allOrd=0;pairCount=0;mixedCount=0;matrixCount=0
jobs=read(W/'new_ordinary_jobs.json');assert len(jobs)==1697
assert all(j['status']=='PASS'for j in read(W/'new_ordinary_job_results.json'))
for j in jobs:mark(W/f"full{j['N']}/chunk_{j['start']}.log",'AUDIT_ACTUAL_HECKE_JETS_COMPLETE')
for n in Ns:
 H=W/f'full{n}';rs[n]=src(W,n);r=rs[n];expected=[(i+1,z[0],z[5],z[4])for i,z in enumerate(r)if z[6]and(n==137 or z[0]==19)];a=read(H/'sieve.json');meta=lit((H/'hecke_jets.m').read_text(),'SourceMetadata');assert sorted(meta)==sorted(expected)
 assert sorted((v['source'],v['degree'],v['orbit'])for v in a['results'])==sorted((v[0],v[1],v[2])for v in expected)
 assert len(expected)==a['source_orbits']==a['nonprincipal']+len(a['exceptions']);ex=[(v['source'],v['degree'],v['orbit'])for v in a['exceptions']];assert ex==([(159,17,4)]if n==137 else[])
 mark(H/'sieve.log','AUDIT_FULL_SIEVE_COMPLETE');newOrd+=len(expected);allOrd+=sum(bool(z[6])for z in r);matrixCount+=a['nonprincipal']
 if n in oldNs:
  old=src(O,n);matches=lit((W/f'inherited{n}.m').read_text(),'InheritedOrbitMatches');assert sorted(z[0]for z in matches)==[i+1 for i,z in enumerate(r)if z[6]and z[0]<=18];assert sorted(z[1]for z in matches)==[i+1 for i,z in enumerate(old)if z[6]]
  for ni,oi,d,orb,k in matches:
   u,v=r[ni-1],old[oi-1];assert u[0]==v[0]==d and u[5]==v[5]==orb and u[4]==v[4]and 1<=k<=(n-1)//2
  mark(W/f'match{n}.log','S19_INHERITED_ORBITS_MATCHED');assert hashlib.sha256((H/'units_data.m').read_bytes()).digest()==hashlib.sha256((O/f'full{n}/units_data.m').read_bytes()).digest()
 fi=read(W/f'FI/FI{n}_verified.json');assert not fi['exceptional_failures'];assert fi['status']==('FAIL'if n==53 else('PASS_RELATIVE'if n in[103,131]else'PASS'))
 if n in[47,53,59,61,67,71,73,83,89,113,127,131]:
  md=[u for u in lit((H/'small_hecke_jets.m').read_text(),'SourceMetadata')if u[1]in[7,8,9,10,11,12]];tasks=set()
  for i,u in enumerate(md):
   for j in range(i,len(md)):
    v=md[j]
    if u[1]+v[1]!=19:continue
    for off in range(math.gcd(u[2],v[2])):
     if i==j and off>u[2]//2:continue
     tasks.add((u[0],v[0],off))
  pa=read(H/'pair_sieve.json');assert not pa['exceptions']and len(pa['results'])==pa['nonprincipal']==len(tasks)and{tuple(v['source'])for v in pa['results']}==tasks;mark(H/'pair_sieve.log','AUDIT_FULL_SIEVE_COMPLETE');pairCount+=len(tasks);matrixCount+=len(tasks)
 if n==137:
  md=lit((H/'small_hecke_jets.m').read_text(),'SourceMetadata');assert len(md)==4 and sorted(v[1]for v in md)==[8,8,8,9];tasks=set()
  for i,u in enumerate(md):
   for j in range(i,len(md)):
    v=md[j]
    if u[1]+v[1]not in[16,17,18,19]:continue
    for off in range(math.gcd(u[2],v[2])):
     if i==j and off>u[2]//2:continue
     tasks.add((u[0],v[0],off))
  pa=read(H/'pair_low_sieve.json');assert not pa['exceptions']and{tuple(v['source'])for v in pa['results']}==tasks and pa['nonprincipal']==len(tasks)==369;mark(H/'pair_low_sieve.log','AUDIT_FULL_SIEVE_COMPLETE');matrixCount+=369
 if n in[73,113,127]:
  ma=read(H/'mixed_sieve.json');d=13 if n==73 else 12;ids={i+1 for i,z in enumerate(r)if z[6]and z[0]==d};assert not ma['exceptions']and{z['source']for z in ma['results']}==ids and ma['nonprincipal']==len(ids)==(21 if n==73 else(9 if n==113 else 4));mark(H/'mixed_sieve.log','AUDIT_FULL_SIEVE_COMPLETE');mixedCount+=len(ids);matrixCount+=len(ids)
ss_expected={53:[(13,1)],61:[(15,1)],73:[(6,4),(18,2),(18,4),(18,4),(18,1)],97:[(16,2)],109:[(9,3),(12,3)],113:[(7,4)],127:[(14,3)]+[(14,9)]*5,137:[(17,2)]}
for n,expected in ss_expected.items():assert sorted((z[0],z[5])for z in rs[n]if not z[6])==sorted(expected)
assert(newOrd,allOrd,pairCount,mixedCount,matrixCount)==(13495,27519,7495,34,21392)
for n,alpha in[(61,{6:1,0:-1}),(97,{12:1,0:-1}),(101,{6:1,5:-1,1:1,0:-1})]:assert{int(k):v for k,v in read(W/f'full{n}/sieve.json')['alpha_coefficients'].items()}==alpha
ranks=read(W/'independent_rank_checks.json');assert ranks['status']=='PASS'and ranks['matrices']==21392 and len(ranks['results'])==35
for z in ranks['results']:
 kind=''if z['kind']=='ordinary'else z['kind'];a=read(W/f"full{z['N']}/{kind}sieve.json");assert z['status']=='PASS'and z['matrices']==a['nonprincipal']and z['rank']==a['dimension']
# Inherited mixed73 certificates apply to any added delta2-invariant divisor.
ma=read(W.parent/'degree17/full73/mixed_sieve.json');assert not ma['exceptions']and sorted(z['degree']for z in ma['results'])==[7,10,10,10,11,11,11]
assert read(O/'full73/mixed_sieve.json')['nonprincipal']==4 and read(O/'full113/mixed_sieve.json')['nonprincipal']==4 and read(O/'full127/mixed_sieve.json')['nonprincipal']==4
for n,c,k in[(73,7,1),(73,4,1),(73,1,1),(89,8,1),(97,3,2),(109,10,2),(109,7,2),(109,1,2),(113,12,2),(113,5,2),(113,11,2),(113,3,2),(113,4,2),(127,12,2),(127,5,2),(127,10,2),(127,1,2),(137,2,2)]:assert Fraction(325*(n*n-1),65536)>k*(19+c)
assert 98**2%113==112 and 19%2==1
pre=read(W/'support_precheck.json');assert len(pre['cases'])==353;support=[v for v in pre['cases']if v['p']in Ns];assert len(support)==344
for z in support:
 if z['p']==137 and z['support']==[['O',17]]:z['argument']+='; source159 excluded by order17 diamond81'
(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','degree':19,'cases':support,'global163':'independently verified odd-degree anti-Jacobian annihilator for diamond8'},indent=2)+'\n')
local={'status':'PASS','degree':19,'local_levels':Ns,'support_types':344,'ordinary_source_orbits':allOrd,'new_ordinary_sources':newOrd,'new_ordinary_nonprincipal':13494,'new_pairs':7495,'new_low137_pairs':369,'new_mixed':34,'new_independent_matrices':21392,'exceptions':['inherited113O8 order8','inherited127O9 order9','new137O17 order17'],'global163':True}
(W/'local_coverage_verified.json').write_text(json.dumps(local,indent=2)+'\n');print('S19_LOCAL_COVERAGE_VERIFIED',local,flush=True)
if '--local-only'in sys.argv:raise SystemExit(0)
# The prime ledger is rebuilt independently of the preparatory exclusions.
g=read(W/'global_bound.json');assert(g['degree'],g['cap'],g['M'],g['coefficient_rank'])==(19,525313,181,38)and g['local_levels']==Ns+[163]
lower=list(map(int,prime_range(2,44)));cases={p:'verified occurrence in exact degree19'for p in lower};table={};pending=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if' p&'in line:pending=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif'\\ord(\\chi)&'in line:
  vals=[math.lcm(*map(int,v.split(',')))for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(pending)==len(vals);table.update(zip(pending,vals));pending=None
assert len(table)==74
for z in g['excluded']:
 p,t=z['p'],z['strangeness'];assert is_prime(p)and 43<p<100000 and p not in cases and t==table.get(p,1)
 if z['reason']=='Corollary7.5':assert p*p>Fraction(2**19,325)*19+1 and 19%((p-1)//(2*t))
 else:
  ell=int(z['reason'].split('=')[1]);assert ell in[2,3]and t==1
  if ell==2:assert p<=157
  assert Fraction(325*(p*p-1),65536)>(2*ell+1)*19;o=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1]);assert all(19%(o//a)for a in[1,2,3]if o%a==0)
 cases[p]=z['reason']
for p in Ns:assert p not in cases;cases[p]='completed local exclusion at2'
assert 163 not in cases;cases[163]='diamond8, odd-degree anti-Jacobian Hecke determinant, gonality114<131.7'
partial='--pending-global'in sys.argv
large=read(W/'large_verified.json');assert large['required']==1147
if not partial:assert large['status']=='PASS'and large['verified']==1147 and not large['missing']
sel=read(W/'large_selected_orders.json');assert len(sel['primes'])==196 and(len(sel['jobs']),len(sel['reused']))==(592,555)
verified_orders={(z['p'],z['order'])for z in large['results']};required_orders={(z['p'],n)for z in sel['primes']for n in z['orders']};assert verified_orders<=required_orders
if not partial:assert verified_orders==required_orders
for z in sel['primes']:
 p,r,v,w,th=[z[k]for k in['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2;assert is_prime(p)and is_prime(r)and valuation(m,r)==v and valuation(19,r)==w and th==v-w>0;assert[int(n)for n in divisors(m)if n%(r**th)==0]==z['orders'];assert p*p>Fraction(2**19,325)*19+1 and p not in cases;cases[p]='completed selected-order character screen and Corollary7.5'
assert sorted(z['p']for z in sel['primes'])==g['large_screen_primes']
assert all(max(int(p)for p,e in __import__('sage.all',fromlist=['factor']).factor(v))<100000 for v in[130561,131073,131585])
for p in map(int,prime_range(100000,525314)):
 ordinary=False
 for f in[18,19]:
  q=2**f;t=math.isqrt(4*q);lo=(q+1-t+p-1)//p;hi=(q+1+t)//p;ordinary|=lo+lo%2<=hi
 goodred=ordinary or any(v%p==0 for v in[261121,261633,262145,262657,263169,523265,524289,525313]);toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,20))
 if p==524287:
  assert not goodred and toric and [f for f in range(1,20)if(2**f-1)%p==0 or(2**f+1)%p==0]==[19]and p in g['unique_toric_dyadic_exclusions'];cases[p]='unique residue-degree19 multiplicative identity place; single-cusp dyadic exclusion'
 elif goodred or toric:assert p in g['large_screen_primes']and p in cases
 else:assert p in g['large_dyadic_excluded']and p not in cases;cases[p]='dyadic parity, complete supersingular orders and single-cusp exclusion'
primes=list(map(int,prime_range(2,525314)));assert set(cases)==set(primes)
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':19,'S':lower,'proved_lower_bound':lower,'proved_upper_bound':lower,'unresolved_primes':[],'dyadic_bound':525313,'dyadic_M':181,'coefficient_rank':38,'audited_primes':len(primes),'large_primes_screened':196,'selected_characters_screened':1147,'new_characters_screened':592,'inherited_characters':555,**{k:v for k,v in local.items()if k not in['status','degree']},'cases':[{'p':p,'reason':cases[p]}for p in primes]}
if partial:
 pending=[z['p']for z in sel['primes']if any((z['p'],n)not in verified_orders for n in z['orders'])]
 out['status']='PRIME_LEDGER_COMPLETE_PENDING_CHARACTERS';out.pop('S');out['unresolved_primes']=pending;out['proved_upper_bound']=sorted(lower+pending);out['selected_characters_screened']=large['verified'];out['new_characters_screened']=large['verified']-555;out['large_primes_screened']=196-len(pending)
 for z in out['cases']:
  if z['p']in pending:z['reason']='pending selected-order character screen'
 (W/'prime_coverage_precheck.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_PRIME_LEDGER_COMPLETE_PENDING_CHARACTERS',len(primes),'primes; unresolved',len(pending),flush=True)
else:
 (W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_FULL_COVERAGE_PROVED',len(primes),'primes,344 support types',flush=True)
