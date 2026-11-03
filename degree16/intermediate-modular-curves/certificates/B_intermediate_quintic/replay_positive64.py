"""Rebuild the level-64 model and test its fixed quadratic-point witness."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = Path(__file__).resolve().parent/'audit_runs'/'positive64'
out.mkdir(parents=True,exist_ok=True)
commands = [
    ([sys.executable,str(root/'canonical_relations.py'),'64','--generators','7',
      '--output','relations.json'],'relations.log','SUCCESS exact relations'),
    ([sys.executable,str(root/'export_canonical.py'),'relations.json'],'export.log',''),
    (['magma','-b',str(root/'verify_canonical_hilbert.m')],'geometry.log','SUCCESS'),
    (['magma','-b',str(root/'case64_quintic.m')],'quintic.log','SUCCESS exact degree five at level 64'),
]
for command,name,expected in commands:
    with (out/name).open('w') as log:
        result = subprocess.run(command,cwd=out,stdout=log,stderr=subprocess.STDOUT)
    text = (out/name).read_text()
    assert result.returncode==0 and expected in text,text
    assert 'Runtime error' not in text and 'User error' not in text and 'Traceback' not in text,text
row = json.loads((out/'relations.json').read_text())['invariants']
assert row['genus']==5 and row['level']==64
receipt = dict(status='FRESH_POSITIVE64_PASS',row=row,
    source_sha256={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in
                  ['canonical_relations.py','enumeration.py','export_canonical.py',
                   'verify_canonical_hilbert.m','case64_quintic.m']},
    outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()
             if p.is_file() and p.name!='receipt.json'})
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('FRESH_POSITIVE64_PASS',flush=True)
