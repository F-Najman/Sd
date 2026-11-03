"""Replay the short exact quintic witness on the independently certified model."""
import hashlib
import json
from pathlib import Path
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
directory = ROOT/'hilbert_jobs/d6111b7c56067f5a'
model = json.loads((directory/'result.json').read_text())
assert model['model_verified']
assert model['id']=='64:1,7,9,15,17,23,25,31,33,39,41,47,49,55,57,63'
for name,digest in model['source_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
for name,digest in model['artifact_sha256'].items():
    assert hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest
checked(['magma','-b',str(ROOT/'case64_quintic.m')],directory,
        'case64_quintic.log','SUCCESS exact degree five at level 64')
sources = ['case64_quintic.m','run_case64_certificate.py','CASE64.md']
artifacts = ['result.json','canonical_input.m','relations.json','case64_quintic.log']
certificate = dict(id=model['id'],status='INFINITE_BY_NEW_EXACT_FUNCTION',
                   source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in sources},
                   artifact_sha256={n:hashlib.sha256((directory/n).read_bytes()).hexdigest() for n in artifacts})
(directory/'case64_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print('SUCCESS complete level-64 quintic certificate',flush=True)
