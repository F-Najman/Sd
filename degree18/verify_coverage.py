from pathlib import Path
import sys,json,re,math,gzip,hashlib
from fractions import Fraction
from sage.all import prime_range,divisors,factor,valuation,is_prime
W=Path(__file__).resolve().parent;B=W.parents[1];O=W.parent/'degree17';sys.path.insert(0,str(W));from unit_arithmetic import lit
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131];lower=list(map(int,prime_range(2,44)))
def read(p):return json.loads(p.read_text())
def mark(p,v):
 s=p.read_text();assert v in s and not any(a in s for a in['Runtime error','User error','Assertion failed','Traceback','System Error']),p

def sources(d,n):return lit((d/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
for p,v in[(W/'verify_occurrences.log','S18_ALL_OCCURRENCES_COMPLETE'),(W/'census_sources.log','S18_ALL_FINITE_SOURCE_ORBITS_COMPLETE'),(W/'bound_ss.log','S18_SS18_ORDERS_COMPLETE'),(W/'quotient_quadratic.log','S18_ALL_QUADRATIC_QUOTIENT_AND_BRANCH_CM_EXCLUSIONS_COMPLETE'),(W/'stabilizers.log','S18_ALL_STABILIZERS_COMPLETE'),(W/'stabilizers127.log','S18_ALL_STABILIZERS_COMPLETE')]:mark(p,v)
mark(W/'verify_extension_occurrences.log','S18_EXTENSION_OCCURRENCES_COMPLETE')
assert [(v['N'],v['field_degree'])for v in read(W/'extension_occurrences.json')]==[(23,18),(29,9),(31,9),(37,6)]
old=read(O/'final_coverage.json');assert old['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'and old['ordinary_source_orbits']==7200 and old['ordinary_nonprincipal']==7198 and old['independent_obstruction_matrices']==9413
assert read(O/'operator_annihilation_verified.json')['status']=='PASS'and read(O/'operator97_verified.json')['status']=='PASS'
assert read(W/'inherited_manifest_verified.json')['status']=='PASS'
assert read(W/'auxiliary_verified.json')['status']=='PASS'and read(W/'native_jet_replay_verified.json')['status']=='PASS'
assert read(W/'relative_cusps_intrinsic_verified.json')['status']=='PASS'and read(W/'relative127_intrinsic_verified.json')['status']=='PASS'and read(W/'relative73_nc_intrinsic_verified.json')['status']=='PASS'
for p in[53,61,73,127]:assert read(W/f'relative{p}_verified.json')['status']=='PASS'
assert read(W/'relative73_nc_verified.json')['status']=='PASS'
for p,cnt in[(103,17),(131,6188)]:
 a=read(W/f'relative{p}_cusps_verified.json');assert a['status']=='PASS'and a['relative_rank']==17 and a['patterns_checked']==cnt
for name,total in[('new_ordinary_jobs.json',795),('ordinary131_jobs.json',64)]:
 js=read(W/name);assert len(js)==total
 for j in js:mark(W/f"full{j['N']}/chunk_{j['start']}.log",'AUDIT_ACTUAL_HECKE_JETS_COMPLETE')
rs={};ordinary=0;newordinary=0;oldordinary=0;pairtotal=0;pairnp=0;mixed=0
for n in ns:
 rs[n]=sources(W,n);H=W/f'full{n}';expected=[(i+1,r[0],r[5],r[4])for i,r in enumerate(rs[n])if r[6]and(n==131 or r[0]==18)];a=read(H/'sieve.json');assert not a['exceptions']and a['nonprincipal']==a['source_orbits']==len(expected)
 assert sorted(lit((H/'hecke_jets.m').read_text(),'SourceMetadata'))==sorted(expected)
 assert sorted((v['source'],v['degree'],v['orbit'])for v in a['results'])==sorted((u[0],u[1],u[2])for u in expected)
 mark(H/'sieve.log','AUDIT_FULL_SIEVE_COMPLETE');newordinary+=len(expected)
 if n!=131:
  before=sources(O,n);matches=lit((W/f'inherited{n}.m').read_text(),'InheritedOrbitMatches');oe=[i+1 for i,r in enumerate(before)if r[6]];ne=[i+1 for i,r in enumerate(rs[n])if r[6]and r[0]<=17];assert sorted(v[1]for v in matches)==oe and sorted(v[0]for v in matches)==ne
  for ni,oi,d,orb,k in matches:
   u,v=rs[n][ni-1],before[oi-1];assert u[0]==v[0]==d and u[5]==v[5]==orb and u[4]==v[4]and 1<=k<=(n-1)//2
  mark(W/f'inherited{n}.log','S18_INHERITED_ORBITS_MATCHED');oa=read(O/f'full{n}/sieve.json');assert oa['source_orbits']==len(oe);ex=[(v['source'],v['degree'],v['orbit'])for v in oa['exceptions']];assert ex=={113:[(2,8,7)],127:[(3,9,7)]}.get(n,[]);oldordinary+=len(oe)
 ordinary+=sum(r[6]for r in rs[n]);fi=read(W/f'FI/FI{n}_verified.json');assert not fi['exceptional_failures']and fi['status']==('FAIL'if n in[103,131]else'PASS')
 if n in[47,53,59,61,67,71,73,79,83,89,127,131]:
  pa=read(H/'pair_sieve.json')
  if n==131:
   lowpa=read(H/'pair_low_sieve.json');assert not lowpa['exceptions']and len(lowpa['results'])==lowpa['nonprincipal']==1042;pa=pa|{'results':pa['results']+lowpa['results'],'nonprincipal':pa['nonprincipal']+lowpa['nonprincipal'],'exceptions':pa['exceptions']+lowpa['exceptions']};mark(H/'pair_low_sieve.log','AUDIT_FULL_SIEVE_COMPLETE')
  md=[v for v in lit((H/'small_hecke_jets.m').read_text(),'SourceMetadata')if v[1]in[7,8,9,10,11]];tasks=set()
  for i,u in enumerate(md):
   for j in range(i,len(md)):
    v=md[j]
    if u[1]+v[1]not in([16,17,18]if n==131 else[18]):continue
    for off in range(math.gcd(u[2],v[2])):
     if i==j and off>u[2]//2:continue
     tasks.add((u[0],v[0],off))
  assert{tuple(v['source'])for v in pa['results']}==tasks and len(pa['results'])==len(tasks)==pa['nonprincipal']+len(pa['exceptions']);ex=[v['source']for v in pa['exceptions']];assert ex==([[3,3,1],[3,3,2],[3,3,3]]if n==127 else[])
  if n==127:assert rs[n][2][0]==9 and rs[n][2][5]==7
  pairtotal+=len(tasks);pairnp+=pa['nonprincipal'];mark(H/'pair_sieve.log','AUDIT_FULL_SIEVE_COMPLETE')
 if n in[73,113,127]:
  a=read(H/'mixed_sieve.json');d=12 if n==73 else 11;ids={i+1 for i,r in enumerate(rs[n])if r[6]and r[0]==d};assert len(ids)==4 and{v['source']for v in a['results']}==ids and not a['exceptions']and a['nonprincipal']==4;mixed+=4;mark(H/'mixed_sieve.log','AUDIT_FULL_SIEVE_COMPLETE')
assert(newordinary,oldordinary,ordinary,pairtotal,pairnp,mixed)==(6824,7200,14024,5021,5018,12)
# Verify the only new annihilator choices, and retain corrected earlier97 inputs.
for n,alpha in[(61,{6:1,0:-1}),(97,{12:1,0:-1}),(101,{6:1,5:-1,1:1,0:-1})]:assert{int(k):v for k,v in read(W/f'full{n}/sieve.json')['alpha_coefficients'].items()}==alpha
r=read(W/'independent_rank_checks.json');assert r['status']=='PASS'and r['matrices']==10812 and r['matrices']+1042==newordinary+pairnp+mixed==11854
for v in r['results']:
 a=read(W/f"full{v['N']}/{''if v['kind']=='ordinary'else v['kind']}sieve.json");assert v['status']=='PASS'and v['matrices']==a['nonprincipal']and v['rank']==a['dimension']
lr=read(W/'independent_rank_low131.json');assert lr['status']=='PASS'and lr['matrices']==1042 and lr['rank']==651
# Exact gonality inequalities used after local stabilizer control.
for n,c,fac in[(73,6,1),(73,3,1),(73,0,1),(89,7,1),(97,2,2),(109,9,2),(109,6,2),(109,0,2),(113,11,2),(113,4,2),(113,10,2),(113,2,2),(113,3,2),(127,11,2),(127,4,2),(127,9,2),(127,0,2)]:assert Fraction(325*(n*n-1),65536)>fac*(18+c)
# The support enumerator is exhaustive and checked all actual support degrees.
pre=read(W/'support_precheck.json');assert len(pre['cases'])==284
ledger=[{'p':v['p'],'support':v['support'],'rational_cusp_complement':v['rational_cusp_complement'],'reason':v['planned_or_verified_argument']}for v in pre['cases']]
# Rebuild the published prime ledger, preserving the table's proven range.
assert all(not is_prime(k*d+1)or k*d+1<=43 for d in[2,6,18]for k in[2,3])
g=read(W/'global_bound.json');assert(g['degree'],g['cap'],g['M'],g['coefficient_rank'])==(18,263169,181,36)and g['local_levels']==ns
cases={p:'verified occurrence in exact degree18'for p in lower}
# Parse the table transcription by adjacent rows, independently of prepare_bound.
table={};pending=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if ' p&'in line:
  tail=line.split(' p&',1)[1].split('\\\\',1)[0];pending=[int(v)for v in tail.split('&')if v]
 elif '\\ord(\\chi)&'in line:
  tail=line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0];values=[math.lcm(*map(int,v.split(',')))for v in tail.split('&')if v];assert pending is not None and len(pending)==len(values);table.update(zip(pending,values));pending=None
assert len(table)==74
for v in g['excluded']:
 p,t=v['p'],v['strangeness'];assert t==table.get(p,1);assert 43<p<100000 and p not in cases
 if v['reason']=='Corollary7.5':assert p*p>Fraction(2**19,325)*18+1 and 18%((p-1)//(2*t))and p not in[37,55]
 else:
  ell=int(v['reason'].split('=')[1]);assert ell in[2,3]and t==1
  if ell==2:assert p<=157
  assert Fraction(325*(p*p-1),65536)>(2*ell+1)*18;o=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1]);assert all(18%(o//a)for a in[1,2,3]if o%a==0)
 cases[p]=v['reason']
for p in ns:assert p not in cases;cases[p]='complete local exclusion at2'
selected=read(W/'large_selected_orders.json');assert len(selected['primes'])==81 and len(selected['jobs'])==615;large=set()
for v in selected['primes']:
 p,r,vv,ww,threshold=v['p'],v['r'],v['valuation_m'],v['valuation_degree'],v['threshold'];m=(p-1)//2;assert is_prime(p)and is_prime(r)and int(valuation(m,r))==vv and int(valuation(18,r))==ww and threshold==vv-ww>0;orders=[int(n)for n in divisors(m)if n%(r**threshold)==0];assert sorted(orders)==sorted(v['orders'])
 for n in orders:
  fp=W/f'large_orders/p{p}_n{n}.log';mark(fp,'S18_SELECTED_CHARACTER_NONSTRANGE');s=fp.read_text();a=re.findall(r'S18_SELECTED_CHARACTER_NONSTRANGE p=(\d+) order=(\d+) auxiliary_prime=(\d+) rigorously_verified=true',s);assert len(a)==1 and tuple(map(int,a[0][:2]))==(p,n);assert is_prime(int(a[0][2]));rec=read(fp.with_suffix('.json'));assert rec['status']=='PASS'and(rec['exit_code']==0 or(rec['exit_code']is None and rec.get('bookkeeping_reconstructed_from_completed_log')and rec['log_sha256']==hashlib.sha256(fp.read_bytes()).hexdigest()))
 assert p*p>Fraction(2**19,325)*18+1 and p not in[37,55];large.add(p);cases[p]='selected-order character certificate and Corollary7.5'
assert sorted(large)==g['large_screen_primes']
(W/'large_order_coverage_verified.json').write_text(json.dumps({'status':'PASS','primes':81,'character_orders':615,'selected_prime_data':selected['primes']},indent=2)+'\n')
for p in map(int,prime_range(100000,263170)):
 good=261121<=2*p<=263169 or any(a%p==0 for a in[261121,261633,262145,262657,263169]);toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,19))
 if good or toric:assert p in large
 else:assert p in g['large_dyadic_excluded'];cases[p]='dyadic parity, twist orders, and single-cusp exclusion'
assert set(cases)==set(map(int,prime_range(2,263170)))
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':18,'S':lower,'proved_lower_bound':lower,'proved_upper_bound':lower,'unresolved_primes':[],'dyadic_bound':263169,'dyadic_M':181,'coefficient_rank':36,'audited_primes':len(cases),'local_levels':ns,'ordinary_source_orbits':ordinary,'ordinary_nonprincipal':ordinary-2,'inherited_ordinary':oldordinary,'new_ordinary':newordinary,'new_pair_configurations':pairtotal,'new_pair_nonprincipal':pairnp,'new_mixed_nonprincipal':mixed,'new_independent_matrices':11854,'inherited_independent_matrices':9413,'support_types_checked':284,'large_primes_screened':81,'selected_characters_screened':615,'relative_levels':[53,61,73,103,127,131],'cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]}
(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','cases':ledger},indent=2)+'\n');(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S18_FINAL_COVERAGE_PASS',len(cases),'primes,284 support types,unresolved=[]',flush=True)
