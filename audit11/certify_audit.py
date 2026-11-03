"""Check closure of the audited case ledger; native replay is replay_all.py."""
from pathlib import Path
import json,re,sys
from unit_arithmetic import lit
W=Path(__file__).resolve().parent
Ns=[37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
def need(name,*terms):
    s=(W/name).read_text()
    assert not any(t in s for t in ['Runtime error','User error','Traceback','Assertion failed']),name
    for t in terms:assert t in s,(name,t)
    return s
pb=json.loads((W/'prime_bound.json').read_text())
assert pb['status']=='PASS' and pb['proved_prime_upper_bound']==103
assert len(pb['midrange_exclusions'])==9560 and pb['selected_character_count']==73
need('prime_bound.log','S11_UNCONDITIONAL_PRIME_BOUND_PASS p<=103')
ch=json.loads((W/'large_orders/all_results.json').read_text())
assert ch['status']=='PASS' and len(ch['results'])==73
for rec in ch['results']:
    assert rec['status']=='PASS' and not rec.get('reused',False)
    need(f"large_orders/p{rec['p']}_n{rec['order']}.log",f"S11_SELECTED_CHARACTER_NONSTRANGE p={rec['p']} order={rec['order']} ")
oc=need('occurrence.log','S11_ALL_OCCURRENCE_WITNESSES_COMPLETE')
for n in [11,13,17,19,23,29,31]:assert re.search(rf'prime={n} field_degree=11\b',oc),n
need('decic_witness.log','DECIC37_OCCURRENCE_COMPLETE')
fi=json.loads((W/'formal_immersion.json').read_text())
assert fi['status']=='PASS' and {r['N'] for r in fi['results']}==set(Ns)
assert fi['total_checked']==2717157222
for r in fi['results']:
    assert r['checked']==r['independent_expected']
    need(f"FI/FI{r['N']}_export.log",'DECIC_FI_EXPORT_COMPLETE')
    need(f"FI/FI{r['N']}_prefix.log",f"checked={r['checked']} status=PASS")
need('census_sources.log','AUDIT_ALL_FINITE_SOURCE_ORBITS_COMPLETE')
need('unit_poles.log','AUDIT_ALL_UNIT_POLE_BOUNDS_COMPLETE')
need('unit_poles_last.log','AUDIT_ALL_UNIT_POLE_BOUNDS_COMPLETE')
nm=need('native_models.log','AUDIT_ALL_NATIVE_MODEL_IDENTIFICATIONS_COMPLETE')
for n in [37,41,43]:assert f'AUDIT_NATIVE_MODEL_CERTIFIED N={n} ' in nm
rows=[];ss=[];ordinary=0;excluded=0
for n in Ns:
    sources=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
    md=lit((W/f'full{n}/hecke_jets.m').read_text(),'SourceMetadata')
    expected=[(i+1,r[0],r[5],r[4]) for i,r in enumerate(sources) if r[6]]
    assert md==expected,(n,md,expected)
    ordinary+=len(md)
    ss +=[(n,i+1,r[0],r[5]) for i,r in enumerate(sources) if not r[6]]
    a=json.loads((W/f'full{n}/sieve.json').read_text())
    assert a['source_orbits']==len(md) and len(a['results'])==len(md)
    assert [r['source'] for r in a['results']]==[r[0] for r in md]
    if n==37:
        assert [(r['source'],r['degree'],r['orbit']) for r in a['exceptions']]==[(1,6,3),(5,9,2),(12,10,18),(13,10,9)]
    else:assert not a['exceptions'],n
    assert all(r['rank']==a['dimension'] for r in a['results'] if r['status']=='NONPRINCIPAL')
    excluded+=a['nonprincipal']
    need(f'full{n}/build.log',f'AUDIT_FULL_MODEL_COMPLETE N={n} ')
    need(f'full{n}/stage2.log',f'AUDIT_ACTUAL_HECKE_JETS_COMPLETE N={n} ')
    rows.append({'prime':n,'canonical_genus':a['canonical_genus'],'ordinary_orbits':len(md),'fresh_Hecke_exclusions':a['nonprincipal'],'remaining_ordinary_branches':'stabilizers and decic-plus-cusp formal immersion' if n==37 else 'none','all_branches_closed':True})
assert ordinary==206 and excluded==202
assert sorted((n,d,o)for n,i,d,o in ss)==[(37,9,1),(41,5,2),(43,7,3),(73,6,4)]
need('supersingular41.log','surviving_indices=[]','NONIC_PRIME_GOOD_BRANCHES_COMPLETED N=41')
need('supersingular43.log','surviving_indices=[]','NONIC_PRIME_GOOD_BRANCHES_COMPLETED N=43')
need('P41_NC5_clean.log','pair=[ 1, 1 ] principal=false','pair=[ 1, 2 ] principal=false','DECIC41_NC5_COMPLETE')
need('P41_cusps.log','A3_principal=false','DECIC41_NONRATIONAL_CUSP_COMPLETE')
need('stabilizers.log','AUDIT_ALL_STABILIZERS_AND_WITNESS_MATCH_COMPLETE','AUDIT37_DECIC_WITNESS_MATCH source=12 verified=true')
need('decic37.log','AUDIT37_DECIC_PLUS_CUSP_COMPLETE all18cusps=true cotangent_dimension38=true rank11=true')
rk=json.loads((W/'independent_matrices.json').read_text())
assert rk['status']=='PASS' and rk['ordinary_obstruction_matrices']==202 and rk['decic_cusp_matrices']==18 and rk['decic_cusp_rank']==11
for n,log,dim in [(37,'two37.log',0),(43,'two43.log',6),(67,'two67_correct.log',2),(71,'two71.log',0),(73,'two73.log',6)]:
    need(log,f'RATIONAL_TWO_DONE N={n} kernel_dimension={dim} diamond_trivial=true')
gon=json.loads((W/'gonality43.json').read_text())
assert gon['status']=='PASS' and gon['envelopes']==234 and gon['partitions_15_with_length_at_least_7']==66 and gon['largest_principal_part_dimension']==4
need('gon43_qjets.log','AUDIT_GON43_ALL_RATIONAL_CUSP_DIFFERENTIAL_JETS_COMPLETE')
need('gon43_check.log','AUDIT_GON43_RIGOROUS_LOWER_BOUND_16_COMPLETE')
for k in range(1,9):need(f'gon43_nonrat_{k}.log',f'AUDIT_GON43_NONRATIONAL_COMPLETE case={k} RR_dimension=1')
control=json.loads((W/'gon43_native_control.json').read_text());assert control['status']=='PASS'
out={'status':'AUDITED COMPUTER-ASSISTED PROOF COMPLETE','degree':11,'S11':[2,3,5,7,11,13,17,19,23,29,31],'effective_prime_bound':103,'unresolved_primes':[],'fresh_ordinary_orbits':206,'fresh_supersingular_orbits':4,'fresh_ordinary_obstruction_matrices':202,'independent_decic_cusp_ranks':18,'rational_cusp_configurations':fi['total_checked'],'fresh_large_character_tests':73,'gonality43_proved_lower_bound':16,'cases':rows,'prior_degree9_and_degree10_exclusion_results_required':False,'software':['Magma V2.30-1','Sage Python','mdmagma (bundled)'],'mathematical_proof':'outputs/S11_proof_audited.txt'}
(W/'final_result.json').write_text(json.dumps(out,indent=2)+'\n')
print('S11_AUDITED_PROOF_ALL_CASES_CLOSED',json.dumps({k:v for k,v in out.items()if k!='cases'},sort_keys=True))
