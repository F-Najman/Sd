"""Replay the complete new level-43 translate obstruction (Sage's Python)."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
directory = ROOT/'hilbert_jobs/d0a49dd94f1144df'
model = json.loads((directory/'result.json').read_text())
assert model['model_verified']
assert model['id'] == '43:1,2,4,8,11,16,21,22,27,32,35,39,41,42'
for filename,digest in model['source_sha256'].items():
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest() == digest
for filename,digest in model['artifact_sha256'].items():
    assert hashlib.sha256((directory/filename).read_bytes()).hexdigest() == digest
subprocess.run([sys.executable,str(ROOT/'integral_relations.py'),str(directory)],check=True)
integral = directory/'integral_model'
checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],integral,
        'geometry_Q.log','SUCCESS: canonical model identified by Hilbert polynomial')
checked(['magma','-b',str(ROOT/'case43_factors.m')],integral,
        'factors.log','SUCCESS: unique elliptic Mordell-Weil direction')
checked(['magma','-b','p:=2','ell:=5',str(ROOT/'test_translate_cosets.m')],integral,
        'translate_p2_ell5.log','SUCCESS exhaustive translate-coset test')
log = (integral/'translate_p2_ell5.log').read_text()
assert 'tested_subgroups=1' in log and 'COMPLETE_COSETS_TOTAL=0' in log
sources = ['case43_factors.m','test_translate_cosets.m','integral_relations.py',
           'export_canonical.py','verify_canonical_hilbert.m','CASE43.md']
artifacts = ['relations.json','canonical_input.m','saturation.json',
             'geometry_Q.log','factors.log','translate_p2_ell5.log']
report = dict(id=model['id'],status='FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION',
              source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources},
              artifact_sha256={f:hashlib.sha256((integral/f).read_bytes()).hexdigest() for f in artifacts})
(integral/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print('SUCCESS complete level-43 finiteness certificate',flush=True)
