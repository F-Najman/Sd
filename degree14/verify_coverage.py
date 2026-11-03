from pathlib import Path
import json,hashlib,re
from fractions import Fraction
from sage.all import prime_range
W=Path(__file__).resolve().parent;B=W.parents[1];S=set(map(int,prime_range(2,44)));ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
g=json.load(open(W/'global_bound.json'));assert g['status']=='PASS'and g['degree']==14 and g['cap']==16641 and set(g['local_levels'])==set(ns)|{127}
assert json.load(open(W/'auxiliary_verified.json'))['status']=='PASS'
fi=json.load(open(W/'formal_immersion.json'));assert fi['status']=='PASS'and {v['N']for v in fi['results']}==set(ns)and all(v['status']=='PASS'for v in fi['results'])
r=json.load(open(W/'independent_rank_checks.json'));assert r['status']=='PASS';assert sum(v['matrices']for v in r['results']if v['kind']=='ordinary')==1018;assert sum(v['matrices']for v in r['results']if v['kind']=='pair_')==137;assert sum(v['matrices']for v in r['results']if v['kind']=='mixed_')==1
orbits=0
for n in ns:
 H=W/f'full{n}';a=json.load(open(H/'sieve.json'));orbits+=a['source_orbits']
 if n==113:assert [(v['source'],v['degree'],v['orbit'])for v in a['exceptions']]==[(2,8,7)]and a['nonprincipal']==54
 else:assert a['status']=='PASS'and not a['exceptions']and a['source_orbits']==a['nonprincipal']
 assert hashlib.sha256((H/'units_data.m').read_bytes()).hexdigest()==hashlib.sha256((B/f'work/degree13/full{n}/units_data.m').read_bytes()).hexdigest()
for n,c in[(59,59),(61,16),(67,17),(71,26),(73,19)]:
 a=json.load(open(W/f'full{n}/pair_sieve.json'));assert a['status']=='PASS'and a['nonprincipal']==c and not a['exceptions']
assert json.load(open(W/'full73/mixed_sieve.json'))['status']=='PASS'
assert orbits==1019
checks=[(W/'verify_occurrences.log','S14_ALL_OCCURRENCES_COMPLETE'),(W/'census_sources.log','S12_ALL_FINITE_SOURCE_ORBITS_COMPLETE'),(W/'census_sources.log','S14_FULL_N_TORSION N=127 degree=14 cyclic_subgroups=128'),(W/'classify_supports.log','S14_SUPPORTS_COMPLETE'),(W/'quotient127.log','S14_QUOTIENT127_COMPLETE H_order=7 quotient_diamond_order=9 closed_degree2_points=48 F4_point_lower_bound=96 gonality_lower_bound=20'),(W/'stabilizers.log','S14_NEW_STABILIZERS_COMPLETE'),(B/'work/degree12/stabilizers.log','S12_EXCEPTIONAL_STABILIZERS_COMPLETE')]
for p,mark in checks:
 s=p.read_text();assert mark in s,(p,mark);assert not any(v in s for v in['Runtime error','User error','Assertion failed']),(p,'error')
for n in ns:
 s=(W/f'full{n}/stage2.log').read_text();assert 'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and 'S14_OLD_ORBIT_REUSE_VERIFIED'in s and not any(v in s for v in['Runtime error','User error','Assertion failed'])
a=json.load(open(W/'gonality53.json'));assert a['status']=='PASS'and a['gonality_lower_bound']==16 and a['base_rank']==26 and a['extra_rank']==66 and 'checked=76256 status=PASS'in a['prefix_result']
# Verify that no noncuspidal place of degrees2..6 was missed in the gonality argument.
for d in range(2,7):
 assert re.search(rf'N=53 degree={d} closed_points=0 diamond_orbits=0', (W/'census_sources.log').read_text())
for n,c,m,f in[(73,8,9,1),(73,2,9,1),(73,5,9,1),(89,3,11,2),(109,5,18,2),(109,2,18,2),(113,7,14,2),(113,6,8,2)]:assert Fraction(325*(n*n-1),65536)>f*(14+c)and c%m
assert 16>14+1 and Fraction(325*(113**2-1),65536)>28 and 112>2*14
assert Fraction(325*(127**2-1),65536)>5*14 and (96+4)//5==20>7*2
cases={p:'occurrence'for p in S}
for a in g['excluded']:
 p=a['p'];assert p not in cases;cases[p]=a['reason']
assert 127 not in cases;cases[127]='two orbit criteria and an intermediate-curve gonality bound'
for n in ns:assert n not in cases;cases[n]='complete local exclusion at 2'
primes=set(map(int,prime_range(2,16642)));assert set(cases)==primes
out={'status':'PASS','degree':14,'S14':sorted(S),'dyadic_bound':16641,'coefficient_rank':28,'dyadic_M':157,'covered_primes':len(cases),'published_exclusions':len(g['excluded']),'quotient_exclusion':127,'local_exclusions':len(ns),'ordinary_source_orbits':1019,'ordinary_nonprincipal':1018,'ordinary_pair_orbits':137,'mixed_obstructions':1,'cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]};(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S14_FINAL_COVERAGE PASS',len(cases),'/',len(primes),'S14',sorted(S))
