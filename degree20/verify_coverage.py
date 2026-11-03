"""Rebuild the degree20 prime and residue-support coverage ledger."""
from pathlib import Path
import sys,json,re,math,hashlib
from fractions import Fraction
from sage.all import prime_range,is_prime,divisors,valuation,factor
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;B=W.parents[1];O=W.parent/'degree19';Ns=[53,59,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139]
def read(p):return json.loads(p.read_text())
def good(name):a=read(W/name);assert a['status']=='PASS',name;return a
def mark(p,needle):
 s=p.read_text();assert needle in s and not any(e in s for e in ['Runtime error','User error','Assertion failed','Traceback','System Error']),str(p)
def src(folder,n):return lit((folder/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
for name,needle in [('verify_small_occurrences.log','S20_SMALL_OCCURRENCES_AND_RIEMANN_ROCH_BOUND_VERIFIED'),('verify_occurrences.log','S20_ALL_OCCURRENCES_COMPLETE'),('census_sources.log','S20_ALL_FINITE_SOURCE_ORBITS_COMPLETE'),('stabilizers.log','S20_ALL_STABILIZERS_COMPLETE'),('relative_stabilizers.log','S20_RELATIVE_STABILIZERS_COMPLETE'),('verify_sharp_finite_native.log','S20_SHARP_FINITE_IMAGE_COMPLETE'),('bound_ss_certified.log','S20_BOUND_TWISTS_CERTIFIED_COMPLETE')]:mark(W/name,needle)
for name in ['inherited_manifest_verified.json','matches_verified.json','dyadic_independent.json','census_counts_independent.json','fi_matrices_independent.json','global_extra_verified.json','anti163_norms_verified.json','sharp_finite_verified.json','intrinsic_relative_independent.json','profile_spaces_independent.json','extra_rank_checks.json','rankzero_verified.json','finite_FI_verified.json','finite_FI_inheritance_verified.json','annihilator_characters_verified.json','stabilizer_torsion_verified.json']:good(name)
assert good('inherited_manifest_verified.json')['files']==11327
assert len(good('fi_matrices_independent.json')['results'])==16
assert len(good('census_counts_independent.json')['results'])==18
assert len(good('intrinsic_relative_independent.json')['results'])==10
assert sum(a['profiles']for a in good('profile_spaces_independent.json')['results'])==105240
for name,count in [('relative53',1),('full_cusps53',63926),('relative73',284),('relative73_nc',4),('relative113',224),('relative97_sharp',2),('full_cusps101_sharp',197),('relative109',3),('relative113_ordinary',392)]:
 a=good(name+'_profiles_verified.json');assert len(a['profiles'])==count and all(r['status']=='PASS'for r in a['profiles'])
a=good('ss73_double_verified.json');assert len(a['profiles'])==12 and {(v['offset'],v['shift'])for v in a['profiles']}=={(o,s)for o in range(3)for s in range(4)}
a=good('relative127_verified.json');assert(a['patterns_checked'],a['relative_rank'],a['full_relation_dimension'],a['relation_code_minimum_nonzero_weight'])==(720720,18,60,7)
assert [(r['p'],r['cusp_patterns'],r['relative_rank'])for r in good('relative_cusps_intrinsic_verified.json')['results']]==[(103,969,19),(131,50388,19)]
parent=read(O/'final_coverage.json');assert parent['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'
assert [r['N']for r in read(W/'occurrences.json')]==[29,31,37,41,43,47,61]
mark(W/'verify_occurrences.log','S20_OCCURRENCE_VERIFIED prime=23 exact_field_degree=10')
jobs=read(W/'new_ordinary_jobs.json');assert len(jobs)==2808 and all(j['status']=='PASS'for j in read(W/'new_ordinary_job_results.json'))
for j in jobs:mark(W/f"full{j['N']}/chunk_{j['start']}.log",'AUDIT_ACTUAL_HECKE_JETS_COMPLETE')
rs={};newOrd=allOrd=pairCount=mixedCount=matrixCount=0;ordinary_exceptions=[]
for n in Ns:
 H=W/f'full{n}';rs[n]=r=src(W,n);expected=[(i+1,z[0],z[5],z[4])for i,z in enumerate(r)if z[6]and(n==139 or z[0]==20)]
 a=read(H/'sieve.json');assert a['status']=='PASS'and not a['exceptions'];meta=lit((H/'hecke_jets.m').read_text(),'SourceMetadata');assert sorted(meta)==sorted(expected)
 assert sorted((v['source'],v['degree'],v['orbit'])for v in a['results'])==sorted(v[:3]for v in expected)
 assert len(expected)==a['source_orbits']==a['nonprincipal'];mark(H/'sieve.log','AUDIT_FULL_SIEVE_COMPLETE');newOrd+=len(expected);allOrd+=sum(bool(z[6])for z in r);matrixCount+=a['nonprincipal']
 if n!=139:
  old=src(O,n);matches=lit((W/f'inherited{n}.m').read_text(),'InheritedOrbitMatches');assert sorted(z[0]for z in matches)==[i+1 for i,z in enumerate(r)if z[6]and z[0]<=19];assert sorted(z[1]for z in matches)==[i+1 for i,z in enumerate(old)if z[6]]
  for ni,oi,d,orb,k in matches:
   u,v=r[ni-1],old[oi-1];assert u[0]==v[0]==d and u[5]==v[5]==orb and u[4]==v[4]and 1<=k<=(n-1)//2
  mark(W/f'match{n}.log','S20_INHERITED_ORBITS_MATCHED');assert sha(H/'units_data.m')==sha(O/f'full{n}/units_data.m')
 if n not in [53,101]:
  fi=read(W/f'FI/FI{n}_verified.json');assert fi['status']==('PASS_RELATIVE'if n in [103,131]else'PASS')and not fi.get('exceptional_failures',[])
 if n in [53,59,67,71,73,79,83,89,97,101,103,107,113,127,131,137,139]:
  md=lit((H/'small_hecke_jets.m').read_text(),'SourceMetadata');tasks=set()
  for i,u in enumerate(md):
   for j in range(i,len(md)):
    v=md[j]
    if not(u[1]+v[1]<=20 if n==139 else u[1]+v[1]==20):continue
    for off in range(math.gcd(u[2],v[2])):
     if i==j and off>u[2]//2:continue
     tasks.add((u[0],v[0],off))
  kind='pair_low_'if n==139 else'pair_';pa=read(H/(kind+'sieve.json'));assert pa['status']=='PASS'and not pa['exceptions']and {tuple(v['source'])for v in pa['results']}==tasks and pa['nonprincipal']==len(tasks)
  mark(H/(kind+'sieve.log'),'AUDIT_FULL_SIEVE_COMPLETE');pairCount+=len(tasks);matrixCount+=len(tasks)
 if n in [73,89,109,113,127]:
  d={73:14,89:9,109:11,113:13,127:13}[n];ma=read(H/'mixed_sieve.json');ids={i+1 for i,z in enumerate(r)if z[6]and z[0]==d}
  assert ma['status']=='PASS'and not ma['exceptions']and {z['source']for z in ma['results']}==ids and ma['nonprincipal']==len(ids);mark(H/'mixed_sieve.log','AUDIT_FULL_SIEVE_COMPLETE');mixedCount+=len(ids);matrixCount+=len(ids)
pa=read(W/'full73/mixed_pair_sieve.json');assert not pa['exceptions']and pa['nonprincipal']==19 and {tuple(r['source'])for r in pa['results']}=={(2,2,k)for k in range(19)};matrixCount+=19
assert {int(k):v for k,v in read(W/'full97/sieve.json')['alpha_coefficients'].items()}=={7:1,6:-1,1:1,0:-1}
assert read(W/'full67/sieve.json')['section_degree']==2 and read(W/'full67/sieve.json')['verification_bound_type']=='canonical_section_zero_divisor'
ranks=good('independent_rank_checks.json');extra=good('extra_rank_checks.json');assert len(ranks['results'])==39 and ranks['matrices']+extra['matrices']==matrixCount
for r in ranks['results']+extra['results']:
 kind=''if r['kind']=='ordinary'else r['kind'];a=read(W/f"full{r['N']}/{kind}sieve.json");assert r['status']=='PASS'and r['matrices']==a['nonprincipal']and r['rank']==a['dimension']
ss_expected={53:[(13,1)],73:[(6,4),(18,1),(18,2),(18,4),(18,4)],97:[(16,2)],109:[(9,3),(12,3)],113:[(7,4)],127:[(14,3)]+[(14,9)]*5,137:[(17,2)]}
for n in Ns:assert sorted((r[0],r[5])for r in rs[n]if not r[6])==sorted(ss_expected.get(n,[]))
# All lower-total ordinary pairs are inherited through the matched models.
# New degree20 mixed cases, including the pair-plus-SS6 case, are explicit.
def strict(p,c,mult):assert Fraction(325*(p*p-1),65536)>mult*(20+c)
support=[];inventory=read(W/'support_inventory_provisional.json');inventory={r['p']:r for r in inventory['levels']}
for n in Ns:
 ordinary=sorted({r[0]for r in rs[n]if r[6]});ss=sorted({r[0]for r in rs[n]if not r[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',d)for d in ordinary]+[('SS',d)for d in ss]+([('NC',nc)]if nc<=20 else[]);assert [list(t)for t in types]==inventory[n]['types']
 def classify(s,c):
  oo=[d for t,d in s if t=='O'];other=[(t,d)for t,d in s if t!='O'];total=20-c
  if not s:return 'full-curve relative cusp immersion'if n==53 else('sharper full-curve cusp immersion'if n==101 else('absolute cusp immersion plus quotient relative fibers'if n in [103,131]else'absolute cusp immersion'))
  if len(oo)==2:
   if other:assert n==73 and oo==[7,7]and other==[('SS',6)];return 'new mixed pair obstruction, 19 relative positions'
   assert total<=20
   if n==113 and oo==[8,8]:strict(n,c,2);return 'ordinary pair obstructions; exceptional H8 invariance and CM exclusion'
   return 'ordinary pair obstruction, all relative positions'
  assert len(oo)<=1
  if oo:
   d=oo[0]
   if not other:
    if n==113 and d==8:return 'ordinary obstruction; exceptional free H8 pullback relative immersion'
    if n==127 and d==9:strict(n,c,2);return 'ordinary obstruction; exceptional H9 stabilizer'
    if n==137 and d==17:strict(n,c,2);return 'ordinary obstruction; exceptional H17 stabilizer'
    return 'ordinary principal-divisor obstruction'
   if n==73:
    assert(d,tuple(other))in{(v,(('SS',6),))for v in [7,10,11,12,13,14]}|{(7,(('SS',6),('SS',6)))}|{(v,(('NC',9),))for v in [7,10,11]};return 'mixed delta2 obstruction (added divisor is delta2 invariant)'
   if n==89:assert d==9 and other==[('NC',11)];return 'new mixed delta2 obstruction'
   if n==109:assert d==11 and other==[('SS',9)];return 'new mixed delta2 obstruction'
   if n==113:
    assert other==[('SS',7)]and d in [8,11,12,13]
    if d==8:strict(n,c,2);return 'involution invariance, CM exclusion, and even specialization multiplicities'
    return 'mixed delta2 obstruction'
   assert n==127 and other==[('NC',7)]and d in [8,9,10,11,12,13]
   return 'two-pullback relative immersion, 720720 cusp patterns'if d==9 else'mixed delta2 obstruction'
  if n==53:assert s==[('SS',13)];return 'relative H13 pullback plus fixed C7'
  if n==73:
   assert total in [6,9,12,15,18]
   if total==6:return 'tame fixed lifts and relative H9 cusp fibers'
   if total==9:return 'free H9 pullback and relative cusp fibers'
   if total==12:return 'double tame fixed lifts, all 12 normalized translates'
   strict(n,c,1);return 'H9 stabilizer and actual rational 2-torsion control'
  if n==89:assert s==[('NC',11)];strict(n,c,1);return 'H11 stabilizer and odd-degree anti-Jacobian annihilator'
  if n==97:assert s==[('SS',16)];return 'sharper Hecke maps and tame H3 fixed-lift relative immersion'
  if n==109:
   if s==[('SS',9)]:return 'free H9 pullback relative immersion'
   assert total in [12,18];strict(n,c,2);return 'H18 stabilizer'
  if n==113:
   if total==7:return 'free H7 pullback relative immersion'
   assert total==14;strict(n,c,2);return 'H14 stabilizer'
  if n==127:assert total in [7,14];strict(n,c,2);return 'H7 stabilizer'
  assert n==137 and s==[('SS',17)];strict(n,c,2);return 'H34 stabilizer'
 cases=[]
 def walk(start,left,s):
  reason=classify(s,left);r={'p':n,'support':[list(v)for v in s],'cusp_complement':left,'argument':reason};support.append(r);cases.append({k:r[k]for k in ['support','cusp_complement']})
  for j in range(start,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],s+[types[j]])
 walk(0,20,[]);assert cases==inventory[n]['cases']
assert len(support)==370
(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','degree':20,'cases':support},indent=2)+'\n')
local={'status':'PASS','degree':20,'local_levels':Ns,'support_types':370,'ordinary_source_orbits':allOrd,'new_ordinary_sources':newOrd,'new_ordinary_nonprincipal':newOrd,'new_pair_matrices':pairCount,'new_mixed_single_matrices':mixedCount,'new_mixed_pair_matrices':19,'new_independent_matrices':matrixCount,'relative_profiles_independently_checked':105240,'exceptions':['113O8 free H8 relative immersion','127O9 H9 stabilizer','137O17 H17 stabilizer']}
(W/'local_coverage_verified.json').write_text(json.dumps(local,indent=2)+'\n');print('S20_LOCAL_COVERAGE_VERIFIED',local,flush=True)
if '--local-only'in sys.argv:raise SystemExit(0)
g=read(W/'global_bound.json');assert(g['degree'],g['cap'],g['M'],g['coefficient_rank'])==(20,525313,229,40)and g['local_levels']==Ns+[151,163,167]
lower=list(map(int,prime_range(2,48)))+[61];cases={p:'verified occurrence over an exact degree20 field'for p in lower};table={};pending=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if' p&'in line:pending=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif'\\ord(\\chi)&'in line:
  vals=[math.lcm(*map(int,v.split(',')))for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(pending)==len(vals);table.update(zip(pending,vals));pending=None
assert len(table)==74
cm={int(p)for d in divisors(20)if d%2==0 for p in [2*d+1,3*d+1]};assert sorted(p for p in cm if is_prime(p)and p>47)==[61]
for z in g['excluded']:
 p,t=z['p'],z['strangeness'];assert is_prime(p)and 47<p<100000 and p not in cases and t==table.get(p,1)and p not in cm
 if z['reason']=='Corollary7.5':assert p*p>Fraction(2**19,325)*20+1 and 20%((p-1)//(2*t))
 else:
  ell=int(z['reason'].split('=')[1]);assert ell in [2,3]and t==1
  if ell==2:assert p<=157
  assert Fraction(325*(p*p-1),65536)>(2*ell+1)*20;o=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1]);assert all(20%(o//a)for a in [1,2,3]if o%a==0)
 cases[p]=z['reason']
for p in Ns:assert p not in cases;cases[p]='completed degree20 local exclusion at2'
for p in [151,163,167]:assert p not in cases;cases[p]='completed global diamond exclusion with proved rational 2-primary hypothesis'
large=read(W/'large_verified.json');assert large['required']==3020;partial='--pending-global'in sys.argv
if not partial:assert large['status']=='PASS'and large['verified']==3020 and not large['missing']
sel=read(W/'large_selected_orders.json');assert len(sel['primes'])==444 and(len(sel['jobs']),len(sel['reused']))==(1951,1069)
verified={(z['p'],z['order'])for z in large['results']};required={(z['p'],n)for z in sel['primes']for n in z['orders']};assert verified<=required
if not partial:assert verified==required
for z in sel['primes']:
 p,r,v,w,th=[z[k]for k in ['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2;assert is_prime(p)and is_prime(r)and valuation(m,r)==v and valuation(20,r)==w and th==v-w>0
 assert [int(n)for n in divisors(m)if n%(r**th)==0]==z['orders']and p*p>Fraction(2**19,325)*20+1 and p not in cases;cases[p]='selected-order character screen and Corollary7.5 for every divisor of20'
assert sorted(z['p']for z in sel['primes'])==g['large_screen_primes']
ss=[261121,261633,262145,262657,263169,523265,524289,525313,1046529,1047553,1048577,1049601,1050625]
for p in map(int,prime_range(100000,525314)):
 ordinary=False
 for f in [18,19,20]:
  q=2**f;t=math.isqrt(4*q);lo=(q+1-t+p-1)//p;hi=(q+1+t)//p;ordinary|=lo+lo%2<=hi
 goodred=ordinary or any(v%p==0 for v in ss);toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,21))
 if goodred or toric:assert p in g['large_screen_primes']and p in cases
 else:assert p in g['large_dyadic_excluded']and p not in cases;cases[p]='dyadic parity, complete supersingular orders, and single-cusp exclusion'
primes=list(map(int,prime_range(2,525314)));assert set(cases)==set(primes)
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':20,'S':lower,'proved_lower_bound':lower,'proved_upper_bound':lower,'unresolved_primes':[],'dyadic_bound':525313,'dyadic_M':229,'coefficient_rank':40,'audited_primes':len(primes),'large_primes_screened':444,'selected_characters_screened':3020,'new_characters_screened':1951,'inherited_characters':1069,**{k:v for k,v in local.items()if k not in ['status','degree']},'cases':[{'p':p,'reason':cases[p]}for p in primes]}
if partial:
 pending=[z['p']for z in sel['primes']if any((z['p'],n)not in verified for n in z['orders'])];out['status']='PRIME_LEDGER_COMPLETE_PENDING_CHARACTERS';out.pop('S');out['unresolved_primes']=pending;out['proved_upper_bound']=sorted(lower+pending)
 for r in out['cases']:
  if r['p']in pending:r['reason']='pending selected-order character screen'
 (W/'prime_coverage_precheck.json').write_text(json.dumps(out,indent=2)+'\n');print('S20_PRIME_LEDGER_COMPLETE_PENDING_CHARACTERS',len(primes),'primes; unresolved',len(pending),flush=True)
else:
 (W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S20_FULL_COVERAGE_PROVED',len(primes),'primes,370 support types',flush=True)
