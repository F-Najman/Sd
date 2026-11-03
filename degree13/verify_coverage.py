from pathlib import Path
import json,re
from sage.all import prime_range
W=Path(__file__).resolve().parent;B=W.parents[1];S={2,3,5,7,11,13,17,19,23,29,31,37}
g=json.load(open(W/'global_bound.json'));assert g['status']=='PASS'and g['degree']==13 and g['cap']==8374
local=set(g['local_levels']);assert len(local)==18
fi=json.load(open(W/'formal_immersion_final.json'));assert fi['status']=='PASS'and{r['N']for r in fi['results']}==local and all(r['status']=='PASS'for r in fi['results'])
rr=json.load(open(W/'formal_immersion_rechecked.json'));assert rr['status']=='PASS'and {r['N']for r in rr['results']}==local
ri=json.load(open(W/'independent_rank_checks.json'));assert ri['status']=='PASS'and{r['N']for r in ri['results']}==local and sum(r['matrices']for r in ri['results'])==663
orbits=0
for N in sorted(local):
 a=json.load(open(W/f'full{N}/sieve.json'));orbits+=a['source_orbits']
 if N==43:assert [(r['source'],r['degree'],r['orbit'])for r in a['exceptions']]==[(29,12,7)]and a['nonprincipal']==61
 elif N==113:assert [(r['source'],r['degree'],r['orbit'])for r in a['exceptions']]==[(2,8,7)]and a['nonprincipal']==34
 else:assert a['status']=='PASS'and not a['exceptions']and a['nonprincipal']==a['source_orbits']
assert orbits==665
for N,count in[(41,2),(73,1)]:
 a=json.load(open(W/f'full{N}/mixed_sieve.json'));assert a['status']=='PASS'and a['nonprincipal']==count and not a['exceptions']
assert json.load(open(W/'mixed_ranks_verified.json'))['status']=='PASS'
assert json.load(open(W/'two53_verified.json'))['rational_two_torsion_upper_dimension']==0
checks=[(W/'verify_occurrences.log','S13_ALL_EXPLICIT_OCCURRENCES_COMPLETE'),(W/'classify_supports.log','S13_SUPPORTS_COMPLETE'),(W/'stabilizers_new.log','S13_NEW_STABILIZERS_COMPLETE'),(W/'mixed43_lifting.log','S13_MIXED43_KNOWN_LIFT_AND_FI_COMPLETE'),(W/'mixed43_lifting.log','S13_KNOWN43_DIRECT_TATE_REDUCTION_MATCH_VERIFIED'),(W/'cusp43.log','S13_CUSP43_ALPHA_A3 principal=false'),(W/'unit_poles.log','AUDIT_ALL_UNIT_POLE_BOUNDS_COMPLETE'),(W/'full113/build.log','AUDIT_FULL_MODEL_COMPLETE N=113'),(B/'work/audit11/P41_NC5_clean.log','principal=false'),(B/'work/audit11/P41_cusps.log','DECIC41_NONRATIONAL_CUSP_COMPLETE'),(B/'work/audit11/supersingular41.log','NONIC_PRIME_GOOD_BRANCHES_COMPLETED'),(B/'work/audit11/supersingular43.log','NONIC_PRIME_GOOD_BRANCHES_COMPLETED'),(B/'work/degree12/stabilizers.log','S12_EXCEPTIONAL_STABILIZERS_COMPLETE')]
for path,mark in checks:
 s=path.read_text();assert mark in s,(path,mark);assert not any(v in s for v in['Runtime error','User error','Assertion failed']),(path,'error in proof input')
# Gonality comparisons and the small stabilizer divisibilities in the proof.
from fractions import Fraction
for N,c,m,factor in[(73,7,9,1),(73,1,9,1),(73,4,9,1),(89,2,11,2),(109,4,18,2),(109,1,18,2),(113,6,7,2),(113,5,8,2)]:
 assert Fraction(325*(N*N-1),65536)>factor*(13+c)and c%m!=0
assert Fraction(325*(53*53-1),65536)>13
cases={p:'occurrence'for p in S}
for a in g['excluded']:
 p=a['p'];assert p not in cases;cases[p]=a['reason']
for p in local:assert p not in cases;cases[p]='complete local exclusion at 2'
primes=set(map(int,prime_range(2,8375)));assert set(cases)==primes
out={'status':'PASS','degree':13,'S13':sorted(S),'dyadic_bound':8374,'coefficient_rank':26,'dyadic_M':157,'covered_primes':len(cases),'published_exclusions':len(g['excluded']),'local_exclusions':len(local),'ordinary_source_orbits':orbits,'ordinary_nonprincipal_orbits':663,'known_degree12_orbit_at43':'excluded by known lift and formal immersion','ordinary_degree8_orbit_at113':'excluded by order-8 diamond stabilizer','cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]}
(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S13_FINAL_COVERAGE PASS',len(cases),'/',len(primes),'S13',sorted(S))
