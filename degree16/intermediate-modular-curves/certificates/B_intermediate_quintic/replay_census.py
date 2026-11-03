"""Fresh independent enumeration, preserving the previously accepted run."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = Path(__file__).resolve().parent/'audit_runs'/'census'
out.mkdir(parents=True,exist_ok=True)
command = [sys.executable,str(root/'audit_enumeration.py'),
           '--max-level','191','--output',str(out/'census.json')]
with (out/'run.log').open('w') as log:
    subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
fresh = json.loads((out/'census.json').read_text())
old = json.loads((root/'enumeration_audit_191.json').read_text())
assert fresh['status'] == 'PASS'
assert fresh['curves'] == old['curves']
assert fresh['total'] == 1388 and fresh['strict'] == 1011
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = dict(status='FRESH_CENSUS_REPLAY_PASS',command=command,
               total=1388,strict=1011,
               inputs={str(p.relative_to(root)):digest(p) for p in
                       [root/'enumeration.py',root/'audit_enumeration.py',Path(__file__)]},
               outputs={p.name:digest(p) for p in [out/'census.json',out/'run.log']})
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('FRESH_CENSUS_REPLAY_PASS',flush=True)
