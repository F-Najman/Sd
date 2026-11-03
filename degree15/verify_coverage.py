from pathlib import Path
import json,hashlib,re
from fractions import Fraction
from sage.all import prime_range
W=Path(__file__).resolve().parent;B=W.parents[1];S=set(map(int,prime_range(2,38)))|{43};ns=[41,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
g=json.load(open(W/'global_bound.json'));assert g['status']=='PASS'and g['degree']==15 and g['cap']==33131 and set(g['local_levels'])==set(ns)|{43,151,181}
assert json.load(open(W/'auxiliary_verified.json'))['status']=='PASS'
fi=json.load(open(W/'formal_immersion.json'));assert fi['status']=='PASS'and {v['N']for v in fi['results']}==set(ns)and all(v['status']=='PASS'for v in fi['results'])
r=json.load(open(W/'independent_rank_checks.json'));assert r['status']=='PASS'
counts={k:sum(v['matrices']for v in r['results']if v['kind']==k)for k in['ordinary','pair_','mixed_','borrowed_7plus7']};assert counts=={'ordinary':2173,'pair_':254,'mixed_':14,'borrowed_7plus7':137}
orbits=0
for n in ns:
 H=W/f'full{n}';a=json.load(open(H/'sieve.json'));orbits+=a['source_orbits']
 if n==41:assert [(v['source'],v['degree'],v['orbit'])for v in a['exceptions']]==[(79,14,10)]
 elif n==113:assert [(v['source'],v['degree'],v['orbit'])for v in a['exceptions']]==[(2,8,7)]
 else:assert a['status']=='PASS'and not a['exceptions']and a['source_orbits']==a['nonprincipal']
 old='degree13'if n==41 else'degree14';assert hashlib.sha256((H/'units_data.m').read_bytes()).digest()==hashlib.sha256((B/f'work/{old}/full{n}/units_data.m').read_bytes()).digest()
assert orbits==2175
for n,c in[(59,58),(61,90),(67,66),(71,40)]:
 a=json.load(open(W/f'full{n}/pair_sieve.json'));assert a['status']=='PASS'and a['nonprincipal']==c and not a['exceptions']
for n,c in[(41,13),(73,1)]:
 a=json.load(open(W/f'full{n}/mixed_sieve.json'));assert a['status']=='PASS'and a['nonprincipal']==c and not a['exceptions']
def check(p,marker):
 s=p.read_text();assert marker in s,(p,marker);assert not any(v in s for v in['Runtime error','User error','Assertion failed','Traceback']),(p,'error')
for p,mark in[(W/'verify_occurrences.log','S15_ALL_OCCURRENCES_COMPLETE'),(W/'census_sources.log','S12_ALL_FINITE_SOURCE_ORBITS_COMPLETE'),(W/'classify_supports.log','S15_SUPPORTS_COMPLETE'),(W/'stabilizers.log','S15_ALL_EXCEPTIONAL_STABILIZERS_COMPLETE'),(W/'exceptional41.log','S15_NATIVE41_EXCEPTIONAL_COMPLETE'),(W/'known41_lifting.log','S15_KNOWN41_LIFT_AND_FI_COMPLETE'),(W/'lift41_charzero.log','S15_KNOWN41_CHARACTERISTIC_ZERO_LIFT_VERIFIED'),(W/'verify_finite_FI_final.log','S15_ALL_SELECTED_FI_FINITE_IMAGE_CERTIFICATES_COMPLETE'),(W/'two61.log','RATIONAL_TWO_DONE N=61 kernel_dimension=0 diamond_trivial=true'),(B/'work/independent_audit/exceptional/P41_cusps.log','DECIC41_NONRATIONAL_CUSP_COMPLETE'),(B/'work/independent_audit/exceptional/P41_pairs.log','DECIC41_NC5_COMPLETE'),(B/'work/independent_audit/exceptional/supersingular41.log','NONIC_PRIME_GOOD_BRANCHES_COMPLETED')]:check(p,mark)
for n in ns:
 s=(W/f'full{n}/stage2.log').read_text();assert 'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and 'S15_OLD_ORBIT_REUSE_VERIFIED'in s and not any(v in s for v in['Runtime error','User error','Assertion failed'])
a=json.load(open(W/'gonality53.json'));assert a['status']=='PASS'and a['gonality_lower_bound']==18 and a['base_rank']==26 and a['extra_rank']==66 and 'checked=1143531 status=PASS'in a['prefix_result']
for d in range(2,9):assert re.search(rf'N=53 degree={d} closed_points=0 diamond_orbits=0',(W/'census_sources.log').read_text())
# The gonality comparisons used by the stabilizer lemma.
for n,c,m,f in[(73,9,9,1),(73,3,9,1),(73,6,9,1),(89,4,11,2),(109,6,18,2),(109,3,18,2),(113,8,14,2),(113,1,14,2),(113,7,8,2)]:
 assert Fraction(325*(n*n-1),65536)>f*(15+c)
 if (n,c)!=(73,9):assert c%m
assert 18>17 and Fraction(325*(61**2-1),65536)>15 and Fraction(325*(113**2-1),65536)>30
assert Fraction(325*(151**2-1),65536)>6*15 and min(75,25)>15
assert 181**2>Fraction(2**19,325)*15+1 and (181-1)//(2*6)==15
# All support mixtures: ordinary-pair minima; the only new mixed SS+ordinary
# configurations are 41:(5+8/9/10),73:(6+7),113:(7+8).
checks={(41,5,8),(41,5,9),(41,5,10),(73,6,7),(113,7,8)}
supports=set()
for n in ns:
 text=(W/f'sources{n}.m').read_text();import sys;sys.path.insert(0,str(W));from unit_arithmetic import lit
 rs=lit(text.replace('true','True').replace('false','False'),'AuditSources');ordinary=sorted({v[0]for v in rs if v[6]});ss=sorted({v[0]for v in rs if not v[6]})
 supports.update((n,a,b)for a in ss for b in ordinary if a+b<=15)
assert supports==checks
# The genus-8 quotient closes the last supersingular case at 61.
h=W/'quotient61';q=json.load(open(h/'independent_checks.json'))
assert q['status']=='PASS' and q['rational_two_torsion_dimension']==0
assert q['genera_X_Y_Z_X0']==[126,26,8,4] and q['geometric_fixed_points']==2
assert q['quadric_determinant']=='-1/4'
assert q['finite_images']==[{'index':30,'genus':126,'winding_rank':123},{'index':2,'genus':8,'winding_rank':7}]
for name,marker in [('finite_diamonds.log','S15_DIAMOND_FINITE_IMAGES_COMPLETE'),('verify_small_quotient.log','S15_SMALL_QUOTIENT61_CHECKS_COMPLETE'),('verify_reduction.log','S15_SS61_REDUCTION_AND_TRANSITIVE_H15_ACTION_COMPLETE'),('verify_sage.log','S15_QUOTIENT61_INDEPENDENT_CHECKS_PASS')]:check(h/name,marker)
# Every prime is accounted for, with matching lower and upper sets.
cases={p:'occurrence'for p in S}
for a in g['excluded']:
 p=a['p'];assert p not in cases;cases[p]=a['reason']
cases[151]='Proposition 4.1 with a full-order diamond, ell=2, n=6'
cases[181]='Corollary 7.5 and no rational noncuspidal point on X0(181)'
for n in ns:
 assert n not in cases;cases[n]='local exclusion at 2 completed by the genus-8 quotient and involution'if n==61 else'complete local exclusion at 2'
primes=set(map(int,prime_range(2,33132)));assert set(cases)==primes
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':15,'S':sorted(S),'proved_lower_bound':sorted(S),'proved_upper_bound':sorted(S),'unresolved_primes':[],'dyadic_bound':33131,'coefficient_rank':30,'dyadic_M':157,'audited_primes':len(cases),'resolved_primes':len(cases),'published_exclusions':len(g['excluded'])+2,'complete_local_exclusions':17,'ordinary_source_orbits':2175,'ordinary_nonprincipal':2173,'new_7plus8_pair_orbits':254,'borrowed_7plus7_pair_orbits':137,'mixed_obstructions':14,'independent_matrix_ranks':2578,'prime61_certificate':'quotient61/independent_checks.json','prime61_argument':'A hypothetical point descends to an irreducible cubic divisor on the genus-8 quotient. Torsion reduction and rational gonality >=4 force invariance under its involution, requiring three fixed points although Riemann-Hurwitz gives only two.','cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]}
(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S15_FINAL_COVERAGE_PASS',len(cases),'resolved of',len(cases),'unresolved=[]',flush=True)
