"""Replay and hash the canonical genus-three/four existence certificates.

Run with Sage's Python. Full model equations are unnecessary: exact gaps
or the weight-four multiplication rank certify a degree-five function.
"""
import hashlib
import json
from pathlib import Path
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
checked([sys.executable,str(ROOT/'low_genus_certificates.py')],ROOT,
        'low_genus_audit.log','SUCCESS completed low-genus tests')
rows = json.loads((ROOT/'low_genus_certificates.json').read_text())
assert len({r['id'] for r in rows}) == len(rows)
for row in rows:
    assert row['genus'] in [3,4]
    if row['passed']:
        if row['genus']==3:
            assert len(row['gaps'])==3 and 5 not in row['gaps']
        else:
            assert row['quadratic_product_rank']==9
sources = ['run_low_genus_audit.py','run_genus5_batch.py',
           'low_genus_certificates.py','LOW_GENUS.md','RATIONAL_MODELS.md']
artifacts = ['low_genus_certificates.json','low_genus_audit.log']
digest = lambda name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
certificate = dict(status='EXACT_LOW_GENUS_CANONICAL_CERTIFICATES',
                   source_sha256={name:digest(name) for name in sources},
                   artifact_sha256={name:digest(name) for name in artifacts})
(ROOT/'low_genus_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print('SUCCESS low-genus replay and manifest',len(rows),'rows',flush=True)
