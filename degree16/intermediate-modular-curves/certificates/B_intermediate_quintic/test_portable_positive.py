"""Run every new positive-case batch using only the portable machinery.

Run with Sage's Python. Computations use isolated temporary copies, so the
distribution's accepted evidence is never overwritten.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER/'reproduction'/'machinery'
OUT = FOLDER/'audit_runs'/'portable_positive'
TASKS = [
    ('canonical_low_genus','run_low_genus_audit.py','SUCCESS low-genus replay and manifest'),
    ('explicit','run_explicit_positive_audit.py','SUCCESS independently regenerated explicit quintic'),
    ('batch','run_batch_positive_audit.py','SUCCESS independently regenerated batch quintic'),
    ('last','run_last_positive_audit.py','SUCCESS final explicit positive replay'),
    ('level64','run_case64_certificate.py','SUCCESS complete level-64 quintic certificate'),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(task):
    name,script,marker = task
    directory = OUT/name
    directory.mkdir()
    work = Path(tempfile.mkdtemp(prefix=f'quintic-portable-{name}-'))/'machinery'
    shutil.copytree(ROOT,work)
    with (directory/'run.log').open('w') as stream:
        process = subprocess.Popen([sys.executable,str(work/script)],cwd=work,
                                   stdout=stream,stderr=subprocess.STDOUT)
        invocation = dict(pid=process.pid,snapshot=str(work),script=script)
        (directory/'invocation.json').write_text(json.dumps(invocation,indent=2)+'\n')
        returncode = process.wait()
    output = (directory/'run.log').read_text()
    assert returncode==0 and marker in output,(name,output[-2000:])
    assert 'Traceback' not in output and 'Runtime error' not in output,name
    if name=='canonical_low_genus':
        cases=json.loads((work/'low_genus_certificates.json').read_text())
        assert len(cases)==14 and all(r['passed'] for r in cases)
    # Preserve the verifier's regenerated certificates; their artifact hashes
    # identify the detailed outputs retained in each isolated working copy.
    patterns = {
        'canonical_low_genus':['low_genus_certificate.json','low_genus_certificates.json'],
        'explicit':['positive_replays/*/certificate.json'],
        'batch':['batch_positive_replays/*/certificate.json'],
        'last':['last_positive_replays/*/certificate.json'],
        'level64':['hilbert_jobs/d6111b7c56067f5a/case64_certificate.json'],
    }
    for pattern in patterns[name]:
        for path in work.glob(pattern):
            target = directory/'certificates'/path.relative_to(work)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,target)
    receipt = dict(status='PORTABLE_POSITIVE_BATCH_PASS',name=name,
                   script_sha256=digest(ROOT/script),
                   files={str(p.relative_to(directory)):digest(p) for p in directory.rglob('*') if p.is_file()})
    (directory/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS portable positive',name,flush=True)
    return name


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        names=list(pool.map(run,TASKS))
    receipt=dict(status='PORTABLE_ALL_POSITIVE_BATCHES_PASS',
                 receipts={name:digest(OUT/name/'receipt.json') for name in names},
                 bundle_manifest_sha256=digest(FOLDER/'reproduction'/'manifest.json'))
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(receipt['status'],flush=True)
