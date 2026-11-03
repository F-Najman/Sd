from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;B=W.parents[1];a=json.loads((W/'final_coverage.json').read_text());assert a['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'
old=json.loads((W.parent/'degree17/proof_manifest.json').read_text());manifest=dict(old);paths=set()
patterns=['PROOF.txt','REPLAY.txt','final_coverage.json','support_coverage.json','*_verified.json','independent_rank*.json','dyadic_jets.json','global_bound.json','large_selected_orders.json','character_metadata_recovery.json','character_library_provenance.json','occurrences.json','extension_occurrences.json','occurrence23.json','sources*.m','census_sources.m','census_sources.log','verify_*.py','verify_*.m','verify_*.log','check_*.py','check_*.log','relative*.m','relative*.py','relative*.json','relative*.log','relative*.txt','*prefixes.cpp','*prefixes','relation_check*','unit_arithmetic.py','full_sieve.py','pair_sieve.py','pair_low131.py','mixed_sieve.py','large_order*.m','large_order_batch.py','large_order_special_batch.py','strange_primes.magma','bound_ss.m','bound_ss.log','stabilizers*.m','stabilizers*.log','quotient_quadratic.m','quotient_quadratic.log','run_new_ordinary.py','run_ordinary131.py','run_small_sieves.py','pipeline_sieves.py','pipeline131.py','new_ordinary_jobs.json','ordinary131_jobs.json','inherited*.m','inherited*.log','match[0-9]*.m','native_jet_linear_algebra.py','find_occurrence23.py','build_extension_occurrences.py','prepare_bound.py','support_precheck.py','support_precheck.json','package_result.py','build_manifest.py']
for pattern in patterns:paths.update(p for p in W.glob(pattern)if p.is_file())
paths.update(p for p in(W/'FI').iterdir()if p.is_file())
for h in W.glob('full[0-9]*'):
 for p in h.iterdir():
  if p.is_file()and p.suffix in['.m','.log','.json','.gz']:paths.add(p)
for p in(W/'large_orders').glob('p*.log'):paths.add(p);paths.add(p.with_suffix('.json'))
# Exclude the historical launcher progress file; it is not a character result.
paths.discard(W/'large_orders/progress.json')
paths.update([W.parent/'degree17/proof_manifest.json',B/'work/audit11/derickx_stoll_table2.txt',B/'outputs/S13_proof.pdf',B/'outputs/S18_proof.pdf',B/'outputs/S18_proof.txt',B/'outputs/S18_result.json',B/'outputs/S18_status.json'])
lib=Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2');paths.update(p for p in lib.rglob('*')if p.is_file()and p.suffix in['.m','.spec'])
paths.add(Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/models_X1_n/FFFc23.txt'))
for p in sorted(paths):
 assert p.exists(),p;h=hashlib.sha256()
 with p.open('rb')as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 key=str(p.relative_to(B))if p.is_relative_to(B)else str(p);manifest[key]=h.hexdigest()
(W/'proof_manifest.json').write_text(json.dumps(dict(sorted(manifest.items())),indent=2)+'\n')
index={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':18,'S':a['S'],'proof':'S18_proof.pdf','manifest':'../work/degree18/proof_manifest.json','manifest_files':len(manifest),'manifest_sha256':hashlib.sha256((W/'proof_manifest.json').read_bytes()).hexdigest(),'replay':'../work/degree18/REPLAY.txt','coverage':'../work/degree18/final_coverage.json','support_coverage':'../work/degree18/support_coverage.json','new_independent_matrices':11854,'inherited_independent_matrices':9413,'selected_character_orders':615,'unresolved_primes':[]};(B/'outputs/S18_certificate_index.json').write_text(json.dumps(index,indent=2)+'\n');print('S18_MANIFEST_COMPLETE',len(manifest),'files',flush=True)
