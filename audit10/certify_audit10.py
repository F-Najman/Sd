"""Degree-10 closure from the fresh full-curve degree-at-most-11 certificates."""
from pathlib import Path
import json,re,subprocess,sys
W=Path(__file__).resolve().parent;A=W.parent/'audit11';B=W.parents[1]
subprocess.run([sys.executable,str(A/'certify_audit.py')],check=True)
bound=json.loads((W/'prime_bound.json').read_text());assert bound['proved_prime_upper_bound']==101 and bound['oesterle_bound']==59536 and len(bound['large_prime_exclusions'])==5987
for name,marker in [('prime_bound.log','DECIC_PRIME_BOUND_VERIFIED'),('occurrence.log','DECIC_WITNESSES_COMPLETE'),('occurrence37.log','DECIC37_OCCURRENCE_COMPLETE')]:
 s=(W/name).read_text();assert marker in s and not any(x in s for x in ['Runtime error','User error','Traceback'])
s=(W/'occurrence.log').read_text()
for n in [23,29,31]:assert re.search(rf'DECIC_WITNESS N={n}\b',s)
Ns=[41,43,47,53,59,61,67,71,73,79,83,89,97,101];cases=[]
for n in Ns:
 a=json.loads((A/f'full{n}/sieve.json').read_text());ss=[r for r in a['results']if r['degree']<=10];assert all(r['status']=='NONPRINCIPAL' and r['rank']==a['dimension']for r in ss)
 cases.append({'prime':n,'ordinary_orbits_through_degree10':len(ss),'status':'CLOSED'})
assert sum(r['ordinary_orbits_through_degree10']for r in cases)==96
out={'status':'AUDITED COMPUTER-ASSISTED PROOF COMPLETE','degree':10,'S10':[2,3,5,7,11,13,17,19,23,29,31,37],'effective_prime_bound':101,'unresolved_primes':[],'fresh_ordinary_orbits':96,'rational_cusp_argument':'Each degree-10 restriction is contained in a certified degree-11 restriction, obtained by adding one at a cusp of maximal multiplicity.','nonrational_cusps':[{'prime':41,'method':'native non-principality'},{'prime':43,'complement_degree':3,'diamond_order':7,'gonality_lower_bound':16},{'prime':73,'complement_degree':1,'diamond_order':9}],'supersingular_branches':[{'prime':41,'method':'native single and pair non-principality'},{'prime':43,'method':'native non-principality'},{'prime':73,'complement_degree':4,'diamond_order':9}],'cases':cases,'prior_degree9_and_degree10_exclusion_results_required':False,'local_certificate_packet':'work/audit11','mathematical_proof':'outputs/S10_proof_audited.txt'}
(W/'final_result.json').write_text(json.dumps(out,indent=2)+'\n');print('S10_AUDITED_PROOF_ALL_CASES_CLOSED',json.dumps(out,sort_keys=True))
