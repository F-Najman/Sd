"""Assemble and test the portable code/evidence tree, without old experiments.

Packaging tool: requires Python and strace, but the resulting bundle does
not require strace. Run only when no previous reproduction/ directory exists.
The accepted machinery is copied to a scratch directory before auditing.
Successful file opens identify data dependencies of the complete ledger;
top-level Python/Magma sources are also included for fresh reproduction.
Finally the reduced bundle is audited again and its inventory is compared
byte-for-byte with the accepted one. This is a packaging check, not a CAS run.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = FOLDER/'reproduction'
    if out.exists():
        raise SystemExit('reproduction/ already exists; do not overwrite a tested bundle')
    scratch = Path(tempfile.mkdtemp(prefix='quintic-bundle-'))
    baseline = scratch/'machinery'
    shutil.copytree(ROOT,baseline,ignore=shutil.ignore_patterns('final','__pycache__'))
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    with (scratch/'baseline.log').open('w') as log:
        subprocess.run(['strace','-f','-yy','-e','trace=openat','-o',str(scratch/'opens.log'),
                        sys.executable,str(baseline/'audit_results.py'),'--require-complete'],
                       cwd=baseline,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    needed = set()
    for line in (scratch/'opens.log').read_text().splitlines():
        match = re.search(r'= \d+<([^>]+)>',line)
        if not match:
            continue
        path = Path(match[1])
        if path.is_relative_to(baseline) and path.is_file():
            relative = path.relative_to(baseline)
            if '__pycache__' not in relative.parts:
                needed.add(relative)
    # Certificate verifiers hash their mathematical inputs, so those inputs
    # are observed above even when no CAS is executed. Include source entry
    # points/helpers as well, since a fresh run uses more than the hash audit.
    needed.update(p.relative_to(baseline) for p in baseline.iterdir()
                  if p.is_file() and p.suffix in {'.py','.m','.md'})
    # Supplied witnesses can be inputs to a fresh verifier without being
    # opened by the ledger: its certificate may hash a copied version instead.
    # Retain all Magma input/witness files, but not unreferenced search logs.
    needed.update(p.relative_to(baseline) for p in baseline.rglob('*.m'))
    needed.update(Path(n) for n in ['complete_inventory.json','classification_inventory.json',
                                  'CLASSIFICATION_TABLE.md','final_audit.json'])
    out.mkdir()
    target = out/'machinery'
    for relative in sorted(needed):
        destination = target/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(baseline/relative,destination)
    # Preserve the relative upstream path used by the original documentation.
    upstream = FOLDER/'audit_runs'/'x0'
    assert json.loads((upstream/'receipt.json').read_text())['status']=='FRESH_X0_ALL_36_PASS'
    shutil.copytree(upstream,out/'final')
    with (out/'check.log').open('w') as log:
        subprocess.run([sys.executable,str(target/'audit_results.py'),'--require-complete'],
                       cwd=target,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    assert (target/'complete_inventory.json').read_bytes()==(ROOT/'complete_inventory.json').read_bytes()
    assert (target/'classification_inventory.json').read_bytes()==(ROOT/'classification_inventory.json').read_bytes()
    report = dict(status='PORTABLE_LEDGER_BUNDLE_PASS',
                  scope='Saved-evidence audit and identical inventory; not a fresh CAS replay',
                  machinery_files=len(needed),
                  files={str(p.relative_to(out)):digest(p) for p in sorted(out.rglob('*')) if p.is_file()})
    (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],len(needed),'machinery files',flush=True)


if __name__=='__main__':
    main()
