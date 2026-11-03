"""Freeze the complete degree22 proof and its inherited proof closure."""
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs'
assert json.loads((W/'final_coverage.json').read_text())['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'
assert (O/'S22_certificate_index.json').is_file()
assert (W/'STOP_RESOURCE_WATCH').exists(), 'Stop the resource watcher after all mathematical jobs complete.'
parent=W.parent/'degree21/proof_manifest.json';old=json.loads(parent.read_text());files={Path(p).resolve()for p in old};files.add(parent.resolve())
exclude={'STATE.txt','STOP_RESOURCE_WATCH','proof_manifest.json','manifest_verified.json','build_manifest.log','verify_manifest.log','finalize_when_ready.log','resource_allocation.json','resource_watch.log','independent_rank_progress.json','large_verification_progress.json','health.json','finalizer_status.json'}
for p in W.rglob('*'):
 if not p.is_file()or p.name in exclude or '__pycache__'in p.parts or p.suffix in ['.lock','.tmp','.pyc']:continue
 files.add(p.resolve())
# Require every fresh character's actual complete provenance, not just a glob.
J=W/'large_orders';sel=json.loads((W/'large_selected_orders.json').read_text())
for r in sel['reused']:files.add(Path(r['path']).resolve())
for r in sel['jobs']:
 stem=f"p{r['p']}_n{r['order']}";a=json.loads((J/(stem+'.json')).read_text());assert a['status']=='PASS'
 suffixes=['.json','_sequence.m','_independent_pade.json','_cpp.log','_bm.log','_graph.txt.gz','_prepared.txt.gz','_graph_rank.json','_graph_verified.json','_graph.log','_graph_prep.log','_graph_check.log','_native_prefix.log','_free.txt.gz','_free_verified.json','_free_prep.log','_free_check.log','_fast_pade.json']
 for suf in suffixes:
  p=J/(stem+suf);assert p.is_file(),str(p);files.add(p.resolve())
 for p in [W/a['cpp_binary_name'],W/(a['cpp_binary_name']+'.cpp')]:assert p.is_file();files.add(p.resolve())
# Require all byte-verified native chunk archives and their source/log records.
a=json.loads((W/'native_chunk_archives.json').read_text());assert a['status']=='PASS'and a['chunks']==9531
for r in a['records']:
 for p in [W/r['archive'],W/f"full{r['N']}/chunk_{r['start']}.log",W/f"full{r['N']}/stage2_chunk.m"]:
  assert p.is_file();files.add(p.resolve())
for f in ['S22_proof.txt','S22_proof.pdf','S22_result.json','S22_status.json','S22_certificate_index.json','S22_certificate_index.txt']:
 p=O/f;assert p.is_file();files.add(p.resolve())
assert all(p.is_file()for p in files)
manifest={}
for i,p in enumerate(sorted(files)):
 with p.open('rb')as f:manifest[str(p)]=hashlib.file_digest(f,'sha256').hexdigest()
 if(i+1)%10000==0:print('S22_MANIFEST_HASH_PROGRESS',i+1,'/',len(files),flush=True)
for p,want in old.items():assert manifest[str(Path(p).resolve())]==want,(p,'frozen inherited input changed')
(W/'proof_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('S22_PROOF_MANIFEST_BUILT',len(manifest),flush=True)
