"""Repeat the complete independent census and compare it with the ledger input.

Run with Sage's Python. The old census is only compared after the new
enumeration finishes; it is never an enumeration input or test oracle.
"""
import hashlib
import json
from pathlib import Path
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
directory = ROOT/'enumeration_replay'
directory.mkdir(exist_ok=True)
checked([sys.executable,str(ROOT/'audit_enumeration.py'),'--max-level','191',
         '--output','census.json'],directory,'audit.log','SUCCESS: 1388 curves, 1011 strict')
new = json.loads((directory/'census.json').read_text())
old = json.loads((ROOT/'enumeration_audit_191.json').read_text())
assert new['status']==old['status']=='PASS'
assert new['curves']==old['curves'] and new['max_level']==old['max_level']==191
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
sources = ['run_enumeration_replay.py','audit_enumeration.py','enumeration.py',
           'run_genus5_batch.py','AUDIT.md']
certificate = dict(status='INDEPENDENT_CENSUS_REPLAY',max_level=191,
                   source_sha256={s:digest(ROOT/s) for s in sources},
                   artifact_sha256={str(p.relative_to(ROOT)):digest(p) for p in
                       [directory/'census.json',directory/'audit.log',ROOT/'enumeration_audit_191.json']})
(directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print('SUCCESS full independent census replay',len(new['curves']),flush=True)
