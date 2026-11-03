"""Re-execute twelve exceptional negative certificates in isolated snapshots.

Run with Sage's Python. Each task gets its own copy of the frozen inputs,
so parallel runs cannot overwrite one another or the accepted certificates.
These are fresh *certificate computations on supplied models*, not fresh
modular-form model generation. Model generation is a separate audit gate.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / 'audit_runs' / 'special'

# name, command arguments, regenerated certificate, terminal success marker
TASKS = [
    ('torsion40', ['run_case40_certificate.py'],
     'hilbert_jobs/82f731393c98cb7c/case40_certificate.json',
     'SUCCESS complete level-40 rank-zero class-sieve certificate'),
    ('translate43', ['run_43_certificate.py'],
     'hilbert_jobs/d0a49dd94f1144df/integral_model/certificate.json',
     'SUCCESS complete level-43 finiteness certificate'),
]
for key in ['2fea1fad025e6bab', 'efd0600330b90e51']:
    TASKS.append((f'torsion48_{key}', ['run_case48_certificate.py', key],
                  f'hilbert_jobs/{key}/case48_certificate.json',
                  'SUCCESS complete level-48 rank-zero class-sieve certificate'))
for key, prime in [('1459e19c781c9c0f', 5), ('4517e2b49cc674e5', 2),
                   ('577694554b43283f', 2)]:
    TASKS.append((f'petri_{key}', ['run_petri_certificate.py', key, '--prime', str(prime)],
                  f'hilbert_jobs/{key}/integral_model/petri_certificate.json',
                  'SUCCESS complete Petri rank-zero finiteness certificate'))
for key, prime, script in [('4a0a750d72e5ecf2', 5, 'run_family_certificate.py'),
                            ('dc8a04ecdc10f967', 5, 'run_family_certificate.py'),
                            ('ef93d63ca2b377a8', 7, 'run_family65_certificate.py')]:
    TASKS.append((f'family_{key}', [script, key, '--prime', str(prime)],
                  f'family_jobs/{key}/certificate.json',
                  'SUCCESS complete elliptic-family finiteness certificate'))
for key in ['5fa08fafc8523084', 'bd67dfd630eb6c1b']:
    TASKS.append((f'family3_{key}', ['run_family3_certificate.py', key],
                  f'family3_jobs/{key}/certificate.json',
                  'SUCCESS complete small-prime elliptic-family finiteness certificate'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(task, baseline):
    name, args, certificate, marker = task
    destination = OUT / name
    # Refuse to overwrite either an earlier receipt or a running invocation.
    destination.mkdir()
    work = Path(tempfile.mkdtemp(prefix=f'quintic-{name}-')) / 'machinery'
    shutil.copytree(baseline, work)
    expected = work / certificate
    if expected.exists():
        expected.unlink()  # Only the disposable snapshot's old certificate.
    invocation = dict(command=[sys.executable, *args], snapshot=str(work))
    (destination / 'invocation.json').write_text(json.dumps(invocation, indent=2) + '\n')
    started = time.monotonic()
    with (destination / 'run.log').open('w') as log:
        process = subprocess.Popen([sys.executable, *args], cwd=work,
                                   stdout=log, stderr=subprocess.STDOUT)
        invocation['pid'] = process.pid
        (destination / 'invocation.json').write_text(json.dumps(invocation, indent=2) + '\n')
        returncode = process.wait()
    assert returncode == 0, (name, returncode)
    assert marker in (destination / 'run.log').read_text(), name
    assert expected.exists(), (name, 'no new certificate')
    report = json.loads(expected.read_text())
    for relative, value in report['source_sha256'].items():
        assert digest(work / relative) == value, (name, relative)
        assert digest(ROOT / relative) == value, ('source changed during replay', relative)
    # Most certificates use paths relative to the machinery root. The level-43
    # certificate instead stores artifact paths relative to its own directory.
    artifact_root = expected.parent if name == 'translate43' else work
    artifacts = [expected]
    for relative, value in report['artifact_sha256'].items():
        path = artifact_root / relative
        assert digest(path) == value, (name, relative)
        artifacts.append(path)
    for path in artifacts:
        target = destination / 'evidence' / path.relative_to(work)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    receipt = dict(status='FRESH_SPECIAL_CERTIFICATE_PASS', name=name,
                   id=report['id'], seconds=round(time.monotonic()-started, 2),
                   scope='Fresh certificate computation on supplied canonical model data',
                   certificate=certificate, source_sha256=report['source_sha256'],
                   outputs={str(p.relative_to(destination)): digest(p)
                            for p in sorted(destination.rglob('*')) if p.is_file()})
    (destination / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS', name, receipt['seconds'], flush=True)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=6)
    args = parser.parse_args()
    assert args.jobs > 0
    OUT.mkdir(parents=True, exist_ok=True)
    # Freeze the whole input tree once, excluding only the presentation folder
    # and Python caches. No files in the accepted machinery are modified.
    baseline = Path(tempfile.mkdtemp(prefix='quintic-special-baseline-')) / 'machinery'
    shutil.copytree(ROOT, baseline, ignore=shutil.ignore_patterns('final', '__pycache__'))
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(replay, task, baseline) for task in TASKS]
        for future in as_completed(futures):
            results.append(future.result())
    assert len(results) == 12
    receipt = dict(status='FRESH_ALL_12_SPECIAL_CERTIFICATES_PASS',
                   cases=sorted(r['name'] for r in results),
                   receipts={r['name']: digest(OUT/r['name']/'receipt.json') for r in results})
    (OUT/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(receipt['status'], flush=True)


if __name__ == '__main__':
    main()
