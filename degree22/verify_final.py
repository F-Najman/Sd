"""Guard the exact S22 claim by every finite and local proof certificate."""
from pathlib import Path
import json,hashlib,math,sys,re
from unit_arithmetic import lit
W=Path(__file__).resolve().parent
required=['symmetric_supports_independent.json','occurrences_verified.json','inherited_manifest_verified.json','inherited_hypotheses_verified.json','source_prefixes_verified.json','dyadic_independent.json','census_counts_independent.json','frobenius89_verified.json','global173_verified.json','extended97_verified.json','model163_independent.json','fi_matrices_independent.json','intrinsic_relative_independent.json','intrinsic_full_cusps_extra.json','intrinsic_full_new_verified.json','intrinsic_multiple_independent.json','relative61_o20_independent.json','relative127_verified.json','relative127_intrinsic_verified.json','relative_cusps_intrinsic_verified.json','profile_coverage_independent.json','profile_spaces_independent.json','relative73_multiple_verified.json','quotient89_verified.json','quotient89_point_count_bound.json','quotient89_intrinsic_verified.json','quotient89_fixed_points_verified.json','resolution89_verified.json','new113_verified.json','generic113_mixed_verified.json','nc113_jets_independent.json','ss113_jets_independent.json','polynomial_arithmetic_verified.json','ss_jets_independent.json','support_inputs_verified.json','independent_rank_checks.json','native_chunk_archives.json']
local_only='--local'in sys.argv
if not local_only:required+=['large_verified.json','independent_sequence_results.json','large_native_results.json']
read=lambda p:json.loads(p.read_text())
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def good(name):a=read(W/name);assert a['status']=='PASS',name;return a
if'--pending'in sys.argv:
 missing=[]
 for f in required:
  try:ready=read(W/f).get('status')=='PASS'
  except(FileNotFoundError,json.JSONDecodeError):ready=False
  if not ready:missing.append(f)
 print(json.dumps({'status':'PENDING'if missing else'CERTIFICATES_PRESENT','missing':missing},indent=2));raise SystemExit(0)
for f in required:good(f)
new113=good('new113_verified.json');assert new113['SS7_closed_points_independently_complete']==4 and new113['SS7_unordered_pair_offsets_complete']==[0,1,2]and new113['SS113_independent_jet_certificate_sha256']==sha(W/'ss113_jets_independent.json')
generic113=good('generic113_mixed_verified.json');assert generic113['cases']==generic113['matrices']==14 and generic113['independent_rank']==477
assert generic113['matrix_archive_sha256']==sha(W/'generic113_mixed/matrices.json.gz')and generic113['sieve_sha256']==sha(W/'generic113_mixed/sieve.json')and generic113['NC_independent_certificate_sha256']==sha(W/'nc113_jets_independent.json')and generic113['producer_source_sha256']==sha(W/'generic113_mixed_sieve.py')and generic113['verifier_source_sha256']==sha(W/'verify_generic113_mixed.py')
for f,h in generic113['native_input_sha256'].items():assert sha(W/f)==h
assert new113['SS_pair_matrix_archive_sha256']==sha(W/'ss_pair113/pair_matrices.json.gz')and new113['NC_data_sha256']==sha(W/'relative113_nc_data.m')
plan=read(W/'prime_coverage_plan.json');assert(plan['degree'],plan['prime_count'],plan['cap'])==(22,155750,2099200)
assert plan['verifier_sha256']==sha(W/'verify_prime_coverage.py')
for f,h in plan['input_sha256'].items():assert sha(W/f)==h,f
support=read(W/'support_coverage_plan.json');assert support['support_types']==len(support['records'])==514 and not support['odd_degree_real_diamond_lemma_used']
Ns=read(W/'local_levels.json')['levels'];sets=read(W/'small_jet_jobs.json')['degree_sets'];ranktasks={(f'full{n}','')for n in Ns+[163]}|{(f'full{n}','pair_')for n in list(map(int,sets))+[163]}|{(f'full{n}','mixed_')for n in[73,89,109,113,127]}|{(tag,'')for tag in['ss89','ss5_89','ss7_89']};assert len(ranktasks)==44
ranks=good('independent_rank_checks.json');assert{(v['folder'],''if v['kind']=='ordinary'else v['kind'])for v in ranks['results']}==ranktasks
for r in ranks['results']:
 kind=''if r['kind']=='ordinary'else r['kind'];H=W/r['folder'];a=read(H/(kind+'sieve.json'));p=H/(kind+'matrices.json.gz');assert sha(p)==r['matrix_archive_sha256']and a['nonprincipal']==r['matrices']and a['dimension']==r['rank']
 sec,g,pr=a['section_degree'],a['canonical_genus'],a['precision'];assert sec in[1,2]and pr-2*sec>4*sec*(g-1)and pr>a['Sturm_bound'];assert a['dimension']==(g if sec==1 else 3*g-3)and a['product_dimension']==(3*g-3 if sec==1 else 7*g-7)
 if H.name=='full97':assert sec==2 and pr==3500
assert sum(v['matrices']for v in ranks['results'])==ranks['matrices']
assert len(read(W/'new_ordinary_job_results.json'))==8910 and all(v['status']=='PASS'for v in read(W/'new_ordinary_job_results.json'))
assert len(read(W/'ordinary163_job_results.json'))==621 and all(v['status']=='PASS'for v in read(W/'ordinary163_job_results.json'))
assert{v['N']for v in read(W/'new_ordinary_sieve_jobs.json')}==set(Ns)and all(v['status']=='PASS'for v in read(W/'new_ordinary_sieve_jobs.json'))
count=0
for n in Ns+[163]:
 H=W/f'full{n}';a=read(H/'sieve.json');assert a['status']=='PASS'and not a['exceptions'],(n,a['exceptions'])
 src=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');expect=[(i+1,v[0],v[5],v[4])for i,v in enumerate(src)if v[6]and(n==163 or v[0]==22)];md=lit((H/'hecke_jets.m').read_text(),'SourceMetadata');assert sorted(md)==sorted(expect)
 assert sorted((v['source'],v['degree'],v['orbit'])for v in a['results'])==sorted(v[:3]for v in expect)and a['nonprincipal']==len(expect);count+=len(expect)
for n in list(map(int,sets))+[163]:a=read(W/f'full{n}/pair_sieve.json');assert a['status']=='PASS'and not a['exceptions']
for n in[73,89,109,113,127]:a=read(W/f'full{n}/mixed_sieve.json');assert a['status']=='PASS'and not a['exceptions']
for name in['relative61_o20','full_cusps61_sharp','full_cusps89','full_cusps97_sharp','full_cusps71','full_cusps127','relative61','relative61_ss20','relative73','relative73_nc','relative109','relative113_ordinary','relative97_sharp','full_cusps101_sharp']:good(name+'_profiles_verified.json')
for n in[59,73,79,83,103,107,109,113,131,137,139]:assert read(W/f'FI/FI{n}_verified.json')['status']in['PASS','PASS_RELATIVE']
good('FI/cusps163_verified.json')
archive=good('native_chunk_archives.json');assert archive['chunks']==archive['required']==len(archive['records'])==9531;seen=set()
for r in archive['records']:
 assert r['path']not in seen and r['decompressed_bytes_independently_rehashed'];seen.add(r['path']);assert sha(W/r['archive'])==r['archive_sha256'];H=W/f"full{r['N']}";assert sha(H/f"chunk_{r['start']}.log")==r['native_log_sha256']and sha(H/'stage2_chunk.m')==r['native_source_sha256']
for name,h in good('polynomial_arithmetic_verified.json')['source_sha256'].items():assert sha(W/name)==h
occ=good('occurrences_verified.json');assert len(occ['records'])==3
for v in occ['records']:assert sha(W/v['source'])==v['source_sha256']and sha(W/v['log'])==v['log_sha256']and v['absolute_degree']==22
lower=occ['proved_lower_bound'];assert lower==[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,67]
local={'status':'PASS','degree':22,'levels':Ns+[163],'support_types':514,'new_ordinary_sources':count,'independently_ranked_matrices':ranks['matrices']+17,'extra_SS_pair113_matrices':3,'extra_generic_O8_mixed113_matrices':14,'odd_degree_real_diamond_lemma_used':False,'evidence_sha256':{f:sha(W/f)for f in required if not f.startswith(('large_','independent_sequence'))}};(W/'local_coverage_verified.json').write_text(json.dumps(local,indent=2)+'\n');(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','degree':22,'cases':support['records']},indent=2)+'\n')
if local_only:print('S22_ALL_LOCAL_EXCLUSIONS_PROVED',514,count,local['independently_ranked_matrices'],flush=True);raise SystemExit(0)
large=good('large_verified.json');assert large['verified']==10065 and len(large['results'])==10065;fresh=[r for r in large['results']if not r['inherited']];assert len(fresh)==5018 and all(math.gcd(r['q'],6*r['p']*(r['p']-1))==1 for r in fresh)
assert good('independent_sequence_results.json')['checked']==5018;native=good('large_native_results.json');assert native['characters']==len(native['results'])==5018 and all(r['status']=='PASS'for r in native['results'])
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':22,'S':lower,'proved_lower_bound':lower,'proved_upper_bound':lower,'unresolved_primes':[],'dyadic_M':229,'coefficient_rank':44,'dyadic_cusp_threshold':20152,'dyadic_cap':2099200,'audited_primes':155750,'large_primes_screened':1488,'selected_character_orders':10065,'new_character_orders':5018,'inherited_character_orders':5047,'support_types':514,'new_ordinary_sources':count,'new_independent_matrices':local['independently_ranked_matrices'],'cases':plan['cases'],'evidence_sha256':{f:sha(W/f)for f in required}};(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_EXACT_SET_PROVED',lower,flush=True)
