"""Freeze every fresh premise and the complete inherited proof closure."""
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';assert json.loads((W/'final_coverage.json').read_text())['status']=='PROVED_WITH_COMPUTER_ASSISTANCE';assert(O/'S21_certificate_index.json').exists()
parent=W.parent/'degree20/proof_manifest.json';old=json.loads(parent.read_text());files={Path(p).resolve()for p in old};files.add(parent.resolve())
# The proof PDF formatter is reused directly, rather than copied into this packet.
files.add((W.parent/'degree17/finalize_result.py').resolve())
exclude={'STATE.txt','STOP_RESOURCE_WATCH','proof_manifest.json','manifest_verified.json','build_manifest.log','verify_manifest.log','finalize_when_ready.log','resource_allocation.json','resource_watch.log','independent_rank_progress.json','large_verification_progress.json','coverage_plan.json','verify_coverage_plan.log'}
for p in W.rglob('*'):
 if not p.is_file()or p.name in exclude or '__pycache__'in p.parts or p.suffix in['.lock','.tmp','.pyc']:continue
 # Capture sources, actual binary engines, all static per-job certificates,
 # exact native records, matrices, witnesses, and completed logs. Volatile
 # progress and resource files have been explicitly excluded above.
 if p.suffix in['.py','.m','.magma','.cpp','.json','.log','.gz','.txt']or p.name in['krylov','krylov_blocked','krylov_blocked_v2','krylov_free','finish_fast','prepare_graph','check_prefixes','relation_check','collect_bad_prefixes']:files.add(p.resolve())
for r in json.loads((W/'large_selected_orders.json').read_text())['reused']:files.add(Path(r['path']).resolve())
# The graph exporter loads the frozen degree20 character library, already in
# the inherited manifest. Every fresh archive is required, not just globbed.
J=W/'large_orders'
for r in json.loads((W/'large_selected_orders.json').read_text())['jobs']:
 stem=f"p{r['p']}_n{r['order']}";a=json.loads((J/(stem+'.json')).read_text());suffixes=['.json','_sequence.m','_independent_pade.json','_cpp.log','_bm.log','_graph.txt.gz','_prepared.txt.gz','_graph_rank.json','_graph_verified.json','_graph.log','_graph_prep.log','_graph_check.log','_native_prefix.log']
 if a.get('recurrence_engine')=='NTL_half_gcd':suffixes+=['_fast_pade.json']
 if a['cpp_implementation']=='free_dual_graph_v1':suffixes+=['_free.txt.gz','_free_verified.json','_free_prep.log','_free_check.log']
 for suf in suffixes:p=J/(stem+suf);assert p.is_file(),str(p);files.add(p.resolve())
for f in['S21_proof.txt','S21_proof.pdf','S21_result.json','S21_status.json','S21_certificate_index.json','S21_certificate_index.txt']:p=O/f;assert p.is_file();files.add(p.resolve())
assert all(p.is_file()for p in files)
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest={}
for i,p in enumerate(sorted(files)):
 manifest[str(p)]=sha(p)
 if(i+1)%10000==0:print('S21_MANIFEST_HASH_PROGRESS',i+1,'/',len(files),flush=True)
for p,want in old.items():assert manifest[str(Path(p).resolve())]==want,(p,'frozen inherited input changed')
(W/'proof_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('S21_PROOF_MANIFEST_BUILT',len(manifest),flush=True)
