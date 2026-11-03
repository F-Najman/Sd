"""Fresh low-genus and eleven explicit positive replays in an isolated tree.

Run with Sage Python. Only top-level code/data files are copied into the
temporary tree; previous positive replay directories are NOT copied.
The level-64 witness and four published cases have separate audit gates.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
out = Path(__file__).resolve().parent/'audit_runs'/'positive_batches'
out.mkdir(parents=True,exist_ok=True)
work = Path(tempfile.mkdtemp(prefix='quintic-positive-reaudit-'))
copied = {}
for path in root.iterdir():
    if path.is_file():
        shutil.copy2(path,work/path.name)
        copied[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
(out/'invocation.json').write_text(json.dumps(dict(work=str(work),pid=os.getpid(),
    source_sha256=copied,status='STARTED_NOT_A_CERTIFICATE'),indent=2)+'\n')
jobs = [
    ('run_low_genus_audit.py',['low_genus_certificates.json','low_genus_certificate.json','low_genus_audit.log'],
     'SUCCESS low-genus replay and manifest'),
    ('run_explicit_positive_audit.py',['positive_replays'],'SUCCESS independently regenerated explicit quintic'),
    ('run_batch_positive_audit.py',['batch_positive_replays'],'SUCCESS independently regenerated batch quintic'),
    ('run_last_positive_audit.py',['last_positive_replays'],'SUCCESS final explicit positive replay'),
]
def run(job):
    script,artifacts,expected = job
    with (out/(script+'.log')).open('w') as log:
        result = subprocess.run([sys.executable,str(work/script)],cwd=work,
                                stdout=log,stderr=subprocess.STDOUT)
    text = (out/(script+'.log')).read_text()
    assert result.returncode == 0 and expected in text, text
    assert 'Traceback' not in text and 'Runtime error' not in text, text
    for name in artifacts:
        source = work/name
        if source.is_dir():
            shutil.copytree(source,out/name,dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        else:
            shutil.copy2(source,out/name)
    print('PASS',script,flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(run,jobs))
low = json.loads((out/'low_genus_certificates.json').read_text())
assert len(low)==14 and all(r['passed'] for r in low)
certificates = list(out.glob('*positive_replays/*/certificate.json'))
certificates += list((out/'positive_replays').glob('*/certificate.json'))
# glob '*positive_replays' already includes 'positive_replays'; deduplicate.
certificates = sorted(set(certificates))
assert len(certificates)==11
assert len({json.loads(p.read_text())['id'] for p in certificates})==11
receipt = dict(status='FRESH_POSITIVE_BATCHES_PASS',low_genus_cases=14,
               explicit_cases=11,source_sha256=copied,
               outputs={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(out.rglob('*')) if p.is_file() and p.name!='receipt.json'})
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('FRESH_POSITIVE_BATCHES_PASS 14 low genus + 11 explicit',flush=True)
