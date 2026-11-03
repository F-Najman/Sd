from pathlib import Path
import hashlib,json,zipfile,shutil
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';L=Path('/home/fnajman/degree9_torsion/nonic-torsion');out=json.loads((W/'final_result.json').read_text());assert out['status']=='AUDITED COMPUTER-ASSISTED PROOF COMPLETE'and not out['unresolved_primes']
files={}
def add(p,name=None):
 assert p.is_file(),p;files[name or str(p.relative_to(B))]=p
roots=['portability_verified.json','certify_audit.py','replay_all.py','replay_sieves.py','relocate.py','render_proof.py','package_audit.py','final_result.json','final_audit.log','replay_verify.log','census_sources.m','census_sources.log','unit_arithmetic.py','full_sieve.py','check_matrices.py','independent_matrices.json','independent_matrices.log','sieve_results_final.json','sieve_batch_final.log','unit_poles.m','unit_poles.log','unit_poles_last.m','unit_poles_last.log','native_models.m','native_models.log','verify_occurrence.m','occurrence.log','verify37_witness.m','decic_witness.log','supersingular3.m','supersingular3.log','verify_large_odd_bound.py','prime_bound.json','prime_bound.log','large_odd_filter_verified.json','large_selected_orders.json','large_order.m','large_order_batch.py','large_character_batch.log','derickx_stoll_table2.txt','audit_fi.py','formal_immersion.json','fi_batch.log','export_FI.m','export_combined_FI.m','compress_FI.py','check_prefixes.cpp','rational_two.m','two37.log','two43.log','two67_correct.log','two71.log','two73.log','decic37.m','decic37.log','decic37_jets.m','stabilizers.m','stabilizers.log','prime_good48.m','supersingular41.log','supersingular41_inputs.m','supersingular43.log','supersingular43_inputs.m','P41_NC5_clean.m','P41_NC5_clean.log','P41_cusps.m','P41_cusps.log','gon43_qjets.py','gon43_qjets.log','gon43_dual_data.m','check_gon43.py','gon43_check.log','gonality43.json','gon43_nonrational.m','gon43_nonrat_results.json','gon43_native_control.m','gon43_native_control.json']
for name in roots:add(W/name)
add(B/'work/degree11/certify_S11.py')
for n in[37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]:
 add(W/f'sources{n}.m')
 for name in['build.m','build.log','units_data.m','stage2.m','stage2.log','hecke_jets.m','sieve.log','sieve.json','matrices.json.gz']:add(W/f'full{n}'/name)
 for tail in['.txt','.compressed.txt','_export.log','_compression.log','_prefix.log']:add(W/f'FI/FI{n}{tail}')
for n in[37,43,67,71,73]:add(W/f'two{n}_data.m')
for k in range(1,9):add(W/f'gon43_nonrat_{k}.log')
for p in(W/'large_orders').iterdir():
 if p.name!='progress.json' and p.suffix in['.log','.json','.magma']:add(p)
# Keep the completed native control record and its producing source.
add(W/'gonality43.m','work/audit11/gon43_original_native_control_source.m')
add(W/'gon43_1.m','work/audit11/gon43_original_native_control_data.m')
for ext in['txt','pdf']:add(O/f'S11_proof_audited.{ext}')
add(O/'S11_result.json')
for p in(L/'mdmagma').rglob('*'):
 if p.is_file()and not any(x.startswith('.git')or x=='__pycache__'for x in p.relative_to(L).parts):add(p,'vendor/nonic/'+str(p.relative_to(L)))
for name in['fast_hecke.m','dt_expansions_local.m']:add(L/'common'/name,'vendor/nonic/common/'+name)
add(Path('/usr/share/common-licenses/GPL-3'),'vendor/nonic/common/GPL-3.txt')
for p in files.values():
 if p.suffix=='.log':
  s=p.read_text();assert not any(t in s for t in['Runtime error','User error','Traceback','Assertion failed']),p
readme='''S(11) = {2,3,5,7,11,13,17,19,23,29,31}
Audited computer-assisted proof, 28 October 2026

Read outputs/S11_proof_audited.pdf or its text version.
The final case ledger is work/audit11/final_result.json.

This packet supersedes the earlier proposed S(11) packet. Its proof does
not assume the old degree-9 or degree-10 exclusion results. It includes
fresh full-curve computations for every ordinary finite-field branch,
the exceptional native calculations, all cusp checks, all 73 new character
tests, the level-43 gonality certificate, and the modular-curve library.

202 ordinary obstruction matrices and 18 decic-plus-cusp restriction
matrices have independent Sage/M4RI rank checks. The census has 206
ordinary and 4 supersingular diamond orbits through degree 11. All
2,717,157,222 normalized rational-cusp cases were checked, with independent
combinatorial counts. There are no unresolved prime cases.

Required software: Magma V2.30-1 (licensed separately), Sage's Python,
and a C++17 compiler for rebuilding the exhaustive cusp checker.
The bundled mdmagma source has its own LICENSE. The local differential
expansion helper is derived from CurveArith under GPL-3.0; the source
header and a GPL copy are included. Absolute paths in sources refer to
the original computer. Verify SHA256.json before modifying them.

After extraction into a new directory:
  python work/audit11/relocate.py

To replay the arithmetic and independent linear-algebra verification
against the retained native calculations:
  python work/audit11/replay_all.py

To regenerate the native calculations and all final certificates:
  python work/audit11/replay_all.py --fresh

To check only the final case closure:
  python work/audit11/certify_audit.py

The closure checker is a case ledger, not a replacement for the proof or
native computations. The --fresh replay is the regeneration path.
The selected character tests are exact finite-field Krylov certificates;
random choices cannot give false full-dimension or full-rank certificates.

Some generic routines retain historical NONIC83 log labels. The actual
level, genus, dimensions and final AUDIT markers identify each computation.
The earlier quotient/lifting certificates and abandoned experiments are
not proof dependencies and are not included. The completed first native
Riemann--Roch control at 43 is preserved with its original producing source;
the standalone gon43_native_control.m regenerates just that control.
'''
manifest={name:hashlib.sha256(p.read_bytes()).hexdigest()for name,p in sorted(files.items())};manifest['README.txt']=hashlib.sha256(readme.encode()).hexdigest()
p=O/'S11_audited_certificates.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 z.writestr('README.txt',readme);z.writestr('SHA256.json',json.dumps(manifest,indent=2)+'\n')
 for name,path in sorted(files.items()):z.write(path,name)
with zipfile.ZipFile(p)as z:
 assert z.testzip()is None
 for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
shutil.copy2(p,O/'S11_certificates.zip')
print('S11_AUDITED_ARCHIVE_VERIFIED','files',len(files),'bytes',p.stat().st_size,'all_SHA256_match=true')
