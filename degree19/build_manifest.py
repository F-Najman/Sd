from pathlib import Path
import json,hashlib,re
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';assert json.loads((W/'final_coverage.json').read_text())['status']=='PROVED_WITH_COMPUTER_ASSISTANCE';assert (O/'S19_certificate_index.json').exists()
# Include every unchanged parent proof input as well as its manifest.
parent=W.parent/'degree18/proof_manifest.json';old=json.loads(parent.read_text());files={Path(p)for p in old};files.add(parent)
Ns={47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137}
root_patterns=['PROOF.txt','REPLAY.txt','sources*.m','census_sources.m','census_sources.log','dyadic_jets.json','global_bound.json','large_selected_orders.json','strange_primes_export.magma','prepare_bound.py','check_sequences.py','check_sequences.log','run_fi.py','run_fi.log','run_relative.py','run_relative.log','large_special_results.json','export_large_sparse.m','finish_cpp.m','krylov','krylov.cpp','character_library_provenance.json','large_verified.json','large_native_results.json','independent_sequence_results.json','occurrences.json','verify_*.py','verify_*.m','verify_*.log','*_verified.json','independent_rank_checks.json','fi_matrices_independent.json','relative73_relation_spaces_independent.json','final_coverage.json','support_coverage.json','local_coverage_verified.json','support_precheck.py','support_precheck.json','unit_arithmetic.py','compact_records.py','full_sieve.py','pair_sieve.py','pair_low137.py','mixed_sieve.py','compress_FI.py','finite_FI_polynomials.m','export_FI_*.m','export_combined_FI.m','check_fi.py','check_fi*_fast.py','check_fi_profiles.py','check_relative*.py','check_relative*.log','check_cusps53.py','check_cusps53.log','relative*.m','relative*.json','relative*.log','full_cusps53.m','full_cusps53_data.m','full_cusps53.log','cusps53*','check_prefixes','check_prefixes.cpp','relation_check','relation_check.cpp','collect_bad_prefixes','collect_bad_prefixes.cpp','stabilizers*.m','stabilizers*.log','stabilizer137_ordinary.m','stabilizer137_ordinary.log','bound_ss.m','bound_ss.log','inherited*.m','match*.m','match*.log','new_ordinary_jobs.json','new_ordinary_job_results.json','run_new_ordinary.py','run_new_ordinary.log','run_characters_final.py','character_worker_adoption_final.json','final_resource_allocation.json','optimize_jet_solver.py','odd_anti163_character_norms.m','odd_anti163_character_norms.log','odd_anti163_character_norms_data.m','odd_anti163_h8.m','odd_anti163_h8.log','odd_anti163_h8_data.m','package_result.py','build_manifest.py','finalize_after_characters.py','progress.py']
exclude={'verify_manifest.log','verify_coverage_precheck.log','verify_two163_characters.py','verify_two163_characters.log','two163_characters_verified.json','manifest_verified.json'}
for pat in root_patterns:
 for p in W.glob(pat):
  if p.is_file()and p.name not in exclude:files.add(p)
for n in Ns:
 H=W/f'full{n}'
 for pat in['units_data.m','stage2*.m','hecke_jets*.m','small_hecke_jets.m','extra13.m','extra13.log','extra_jets*.m','fast_test.m','fast_test.log','fast_jets*.m','chunk_*.log','sieve.json','sieve.log','sieve_extra.log','matrices.json.gz','pair*_sieve.json','pair*_sieve.log','pair*_matrices.json.gz','mixed_sieve.json','mixed_sieve.log','mixed_matrices.json.gz']:
  files.update(p for p in H.glob(pat)if p.is_file())
 if n==137:files.update([H/'build.m',H/'build.log'])
 files.update(p for p in(W/'original_jet_solvers'/f'full{n}').glob('*.m')if p.is_file())
for p in(W/'FI').iterdir():
 m=re.match(r'FI(\d+)',p.name)
 if p.is_file()and m and int(m[1])in Ns:files.add(p)
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs']
for j in jobs:
 stem=f"p{j['p']}_n{j['order']}"
 for suffix in['.json','_sequence.m','_independent_pade.json','_sparse.log','_cpp.log','_bm.log']:
  p=W/'large_orders'/(stem+suffix);assert p.exists(),str(p);files.add(p)
for j in json.loads((W/'large_selected_orders.json').read_text())['reused']:files.add(Path(j['path']))
prov=json.loads((W/'character_library_provenance.json').read_text());files.add(Path(prov['source']));files.update(map(Path,prov['Magma_internal_sources']))
for name in['S19_proof.txt','S19_proof.pdf','S19_result.json','S19_status.json','S19_certificate_index.json']:files.add(O/name)
assert all(p.exists()and p.is_file()for p in files)
manifest={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)}
for p,want in old.items():assert manifest[str(Path(p).resolve())]==want,(p,'inherited input changed')
(W/'proof_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('S19_PROOF_MANIFEST_BUILT',len(manifest),'files',flush=True)
