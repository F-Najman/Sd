from pathlib import Path
import json,zipfile,hashlib
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';L=Path('/home/fnajman/degree9_torsion/nonic-torsion');assert json.loads((W/'final_coverage.json').read_text())['status']=='PASS';assert json.loads((W/'large_verified.json').read_text())['status']=='PASS'
files={}
def add(p,arc=None):
 p=Path(p);assert p.is_file(),p;files[arc or str(p.relative_to(B))]=p
names=['unit_arithmetic.py','full_sieve.py','setup_models_new.py','census_sources.m','census_sources.log','ordinary_jobs.json','verify_ranks.py','verify_ranks.log','independent_rank_checks.json','check_fi_final.py','compress_FI.py','check_prefixes.cpp','export_FI.m','export_FI_fast.m','export_combined_FI.m','export_FI_alpha_fast.m','formal_immersion_final.json','fi_final.log','ss_orders.m','ss_orders.log','prepare_bound.py','large_filter.json','large_selected_orders.json','verify_published_bound.py','published_prime_bound.json','verify_large.py','large_verified.json','verify_coverage.py','final_coverage.json','large_order.m','export_large_sparse.m','export_large_sparse_v1.m','export_large_sparse_v2.m','krylov.cpp','finish_cpp.m','run_large_cpp.py','check_sequences.py','independent_sequence_results.json','large_native_results.json','cpp_native_comparison.json','sparse_matrix_comparisons.json','unit_poles.m','unit_poles.log','stabilizers.m','stabilizers.log','occurrence43.m','occurrence43.log','known43_entry.txt','small_witnesses.json','verify_small_witnesses.m','verify_small_witnesses.log','find_small_witnesses.py','find31.py','finalize_result.py']
for n in names:add(W/n)
for n in ['classify_supports.m','classify_supports.log','scheduler_cleanup.json','clean_regeneration_required.json','clean_regenerate.py','krylov_input_guards.json']:add(W/n)
for p in W.glob('sources*.m'):add(p)
for h in W.glob('full*'):
 if h.is_dir():
  for n in ['units_data.m','hecke_jets.m','stage2.m','stage2.log','sieve.json','matrices.json.gz'] :add(h/n)
  for n in ['build.m','build.log']:
   if(h/n).exists():add(h/n)
for n in[41,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109]:
 stem={73:'FI73_i12_combined',89:'FI89_i11',107:'FI107_alpha_fast',109:'FI109_alpha_fast'}.get(n,f'FI{n}')
 for ext in ['.txt','.compressed.txt']:add(W/'FI'/(stem+ext))
 for suffix in ['.log','_export.log']:
  p=W/'FI'/(stem+suffix)
  if p.exists():add(p)
 add(W/'FI'/f'FI{n}_verified.json')
 if n<=103:
  for name in ['build.m','build.log']:add(B/f'work/audit11/full{n}'/name)
sel=json.loads((W/'large_selected_orders.json').read_text())
for rec in sel['jobs']:
 stem=f"p{rec['p']}_n{rec['order']}";meta=json.loads((W/'large_orders'/(stem+'.json')).read_text())
 for suffix in ['.json','_sequence.m','_independent_pade.json']:add(W/'large_orders'/(stem+suffix))
 if 'C++'in meta.get('method',''):
  for suffix in ['_sparse.log','_cpp.log','_bm.log']:add(W/'large_orders'/(stem+suffix))
 else:add(W/'large_orders'/(stem+'.log'))
for rec in sel['reused']:
 stem=f"p{rec['p']}_n{rec['order']}"
 for suffix in ['.json','.log','_sequence.m','_independent_pade.json']:add(B/'work/independent_audit/global_fi/large73'/(stem+suffix))
 add(Path(rec['source']))
add(W/'large_orders/strange_primes_export.magma');add(W/'large_orders/p176797_n29466_sparse.sequence.m')
for stem in ['p176797_n29466','p106129_n2']:add(W/'large_orders'/(stem+'_sparse_v2.log'))
for n in ['prime_good48.m','P41_NC5_clean.m','P41_NC5_clean.log','P41_cusps.m','P41_cusps.log','supersingular41_inputs.m','supersingular41.log','rational_two.m','two73.log','two73_data.m','unit_poles.m','unit_poles.log','unit_poles_last.m','unit_poles_last.log','derickx_stoll_table2.txt']:add(B/'work/audit11'/n)
for n in ['two73.log','two73_data.m','P41_pairs.log','P41_cusps.log','supersingular41.log']:add(B/'work/independent_audit/exceptional'/n)
for p in [O/'S12_proof.txt',O/'S12_proof.pdf',O/'S12_result.json',O/'S11_proof_audited.txt',O/'S10_S11_independent_audit.txt']:add(p)
for sub in ['mdmagma','common']:
 for p in(L/sub).rglob('*'):
  if p.is_file()and not any(x in p.parts for x in['.git','__pycache__']):add(p,'library/nonic-torsion/'+str(p.relative_to(L)))
readme='''S(12) = {2,3,5,7,11,13,17,19,23,29,31,37,43}

This is a computer-assisted proof with exact arithmetic. Start with
outputs/S12_proof.pdf or .txt and outputs/S12_result.json.

Requirements: Sage (the python command used for these computations was
Sage's Python), Magma V2.30-1, a C++17 compiler. The optional compact
Magma exporter imports the installed modular-symbol package. Its import
paths refer to /opt/magma-2.30-1/package on the original computer.
For another installation adjust those imports or use export_large_sparse_v1.m.

First run python relocate.py from the extracted root. It changes only
the original absolute workspace/library paths in source and metadata.
The scalar sequences, Pade certificates, numerical matrices and their
recorded hashes are unchanged by relocation.

Check the stored certificates:
  g++ -O3 -std=c++17 work/degree12/check_prefixes.cpp -o work/degree12/check_prefixes
  python work/degree12/verify_published_bound.py
  python work/degree12/verify_ranks.py
  python work/degree12/check_fi_final.py
  python work/degree12/verify_large.py
  python work/degree12/verify_coverage.py

The last command must print PASS and 44045 / 44045 with no pending primes.
verify_large.py checks every required character order and verifies the
coprime Pade congruence and degree certificate, including 53 reused
independently audited certificates. It checks all arithmetic bounds for
the C++ accumulators. The two sparse-matrix comparisons and one complete
native/C++ sequence comparison are recorded separately.

For full regeneration, work in a copy. The Magma scripts contain all
mathematical assertions and fixed seeds. Run the cusp/ordinary census,
stage2.m in each fullN directory, and full_sieve.py N. New canonical
models at 107 and 109 have build.m; the other build scripts are borrowed
from work/audit11/fullN and their output is copied to fullN/units_data.m.
Run model builders with cwd library/nonic-torsion. FI exporters give
the complete binary operator rows; compress_FI.py reconstructs every raw
row exactly from the compressed coordinates used by the prefix checks.
The selected FI stems are explicit in check_fi_final.py.

The global pipeline is export_large_sparse.m -> krylov.cpp -> finish_cpp.m
-> check_sequences.py. run_large_cpp.py schedules it with native Magma
fallbacks. Stored PASS metadata makes it skip completed jobs, so archive
the per-character metadata in a working copy to force regeneration.
Keep strange_primes_export.magma in place. Global regeneration needs
substantial time and memory; checking stored Pade certificates is faster.

At level 41, native function-field IsPrincipal computations are reused
from the audited degree-11 work; their scripts and logs are included.
The J_1(73) rational 2-torsion bound uses exact JOne integral homology,
not an isogenous factor. Both its audited and independently rerun data
are included. These inherited statements are independent of total
divisor degree. The proof states how each is used in degree 12.

MANIFEST.json records the original bytes. Relocation alters path-bearing
source files; numerical certificate hashes checked by verify_large.py
remain valid. The original source root and library paths are documented
in relocate.py. No failed smaller-quotient experiment is a proof input.
'''
relocate='''from pathlib import Path
root=Path(__file__).resolve().parent
old_root="'''+str(B)+'''"
old_library="'''+str(L)+'''"
changed=[]
for base in [root/'work']:
 for p in base.rglob('*'):
  if p.is_file() and p.suffix in ['.m','.py','.json']:
   s=p.read_text();t=s.replace(old_library,str(root/'library/nonic-torsion')).replace(old_root,str(root))
   if t!=s:p.write_text(t);changed.append(str(p.relative_to(root)))
print('Relocated',len(changed),'path-bearing source/metadata files.')
'''
manifest={arc:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for arc,p in files.items()};out=O/'S12_certificates.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for arc,p in sorted(files.items()):z.write(p,arc)
 z.writestr('README.txt',readme);z.writestr('relocate.py',relocate);z.writestr('MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
print('S12_PACKET_CREATED',len(files),'files',out.stat().st_size,'bytes',flush=True)
with zipfile.ZipFile(out)as z:assert z.testzip()is None
print('S12_PACKET_ZIP_INTEGRITY_PASS',flush=True)
