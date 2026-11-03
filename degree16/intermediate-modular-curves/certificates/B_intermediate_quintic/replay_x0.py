"""Fresh execution of all 36 upstream X0 certificates, in a separate package."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

folder = Path(__file__).resolve().parent
source = folder.parents[1]/'final'
out = folder/'audit_runs'/'x0'
out.mkdir(parents=True,exist_ok=True)
shutil.copytree(source/'code',out/'code',dirs_exist_ok=True)
for name in ['run.py','README.md','quintic_points.tex']:
    shutil.copy2(source/name,out/name)
with (out/'replay.log').open('w') as log:
    result = subprocess.run([sys.executable,str(out/'run.py'),'--jobs','8'],
                            cwd=out,stdout=log,stderr=subprocess.STDOUT)
assert result.returncode==0,(out/'replay.log').read_text()
report = json.loads((out/'verification.json').read_text())
assert report['mode']=='fresh run' and len(report['tasks'])==36
assert all(r['passed'] for r in report['tasks'].values())
for path in (source/'code').glob('*.m'):
    assert path.read_bytes()==(out/'code'/path.name).read_bytes()
receipt = dict(status='FRESH_X0_ALL_36_PASS',
               source_sha256={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in [source/'run.py',source/'quintic_points.tex',*(source/'code').glob('*.m')]},
               verification_sha256=hashlib.sha256((out/'verification.json').read_bytes()).hexdigest())
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('FRESH_X0_ALL_36_PASS',flush=True)
