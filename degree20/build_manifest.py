from pathlib import Path
import json,hashlib,re
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';assert json.loads((W/'final_coverage.json').read_text())['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'and(O/'S20_certificate_index.json').exists()
parent=W.parent/'degree19/proof_manifest.json';old=json.loads(parent.read_text());files={Path(p).resolve()for p in old};files.add(parent.resolve())
exclude={'STATE.txt','proof_manifest.json','build_manifest.log','finalize_when_ready.log','verify_manifest.log','verify_coverage_precheck.log','verify_large_partial.log','manifest_verified.json','prime_coverage_precheck.json','resource_allocation.json','independent_rank_progress.json'}
patterns=['*.json','*.log','*.py','*.m','*.magma','*.cpp','PROOF.txt','REPLAY.txt','*_verified.json','*independent.json','global_bound.json','dyadic_jets.json','large_selected_orders.json','large_verified.json','large_native_results.json','independent_sequence_results.json','independent_rank_checks.json','extra_rank_checks.json','local_coverage_verified.json','support_coverage.json','final_coverage.json','occurrences.json','local_levels.json','new_ordinary_jobs.json','new_ordinary_job_results.json','small_jet_jobs.json','small_jet_results.json','small_sieve_results.json','character_library_provenance.json','verify*.log','relative*.log','full_cusps*.log','sharp*.log','strange_eigenvalues.log','ss73*.log','stabilizers.log','bound_ss*.log','match*.log','run_characters_graph24.log','run_characters_graph24_bm4.log','check_sequences_parallel.log','character_worker_adoption_graph24.json','character_worker_adoption_graph24_bm4.json','character_checkpoint_bm4.json','krylov','krylov_hybrid','check_prefixes','relation_check','collect_bad_prefixes']
for pat in patterns:files.update(p.resolve()for p in W.glob(pat)if p.is_file()and p.name not in exclude)
for n in [53,59,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139]:
 H=W/f'full{n}'
 for pat in ['units_data.m','stage2*.m','hecke_jets*.m','small_jets*.m','small_hecke_jets.m','chunk_*.log','small_chunk_*.log','*sieve.json','*sieve.log','*matrices.json.gz']:
  files.update(p.resolve()for p in H.glob(pat)if p.is_file())
 if n==139:files.update([(H/'build.m').resolve(),(H/'build.log').resolve()])
for folder in ['FI','ss73','optimization']:
 files.update(p.resolve()for p in(W/folder).rglob('*')if p.is_file()and not p.name.endswith('.tmp'))
jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs']
for j in jobs:
 stem=f"p{j['p']}_n{j['order']}";a=json.loads((W/'large_orders'/f'{stem}.json').read_text());suffixes=['.json','_sequence.m','_independent_pade.json','_cpp.log','_bm.log']
 if a.get('cpp_implementation')=='raw_manin_graph_v1':suffixes+=['_graph.txt.gz','_prepared.txt.gz','_graph_rank.json','_graph_verified.json','_graph.log','_graph_prep.log','_graph_check.log','_native_prefix.log']
 else:suffixes+=['_sparse.log']
 for suffix in suffixes:
  p=W/'large_orders'/(stem+suffix);assert p.is_file(),str(p);files.add(p.resolve())
for j in json.loads((W/'large_selected_orders.json').read_text())['reused']:files.add(Path(j['path']).resolve())
prov=json.loads((W/'character_library_provenance.json').read_text());files.add(Path(prov['source']).resolve());files.update(Path(p).resolve()for p in prov['Magma_internal_sources'])
for name in ['S20_proof.txt','S20_proof.pdf','S20_result.json','S20_status.json','S20_certificate_index.json']:files.add((O/name).resolve())
assert all(p.is_file()for p in files)
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest={str(p):sha(p)for p in sorted(files)}
for p,want in old.items():assert manifest[str(Path(p).resolve())]==want,(p,'inherited input changed')
(W/'proof_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('S20_PROOF_MANIFEST_BUILT',len(manifest),'files',flush=True)
