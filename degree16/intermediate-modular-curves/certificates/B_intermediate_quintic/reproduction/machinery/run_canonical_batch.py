"""Generate and independently verify unresolved canonical models in isolation.

Run with Sage's Python. Full subgroup identity is saved in each job directory;
the short hash is just a directory name. No unsuccessful check is accepted.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(row):
    key = hashlib.sha256(row['id'].encode()).hexdigest()[:16]
    directory = ROOT/'canonical_jobs'/key
    directory.mkdir(parents=True, exist_ok=True)
    metadata = directory/'curve.json'
    if metadata.exists():
        assert json.loads(metadata.read_text())['id'] == row['id']
    metadata.write_text(json.dumps(row, indent=2)+'\n')
    start = time.monotonic()
    checked([sys.executable, str(ROOT/'canonical_relations.py'), str(row['level']),
             '--generators', *map(str, row['delta']), '--output', 'relations.json'],
            directory, 'relations.log', 'SUCCESS exact relations')
    subprocess.run([sys.executable, str(ROOT/'export_canonical.py'), 'relations.json'],
                   cwd=directory, check=True)
    checked(['magma', '-b', str(ROOT/'verify_canonical.m')], directory,
            'geometry.log', 'SUCCESS: geometrically integral canonical model')
    sources = ['enumeration.py', 'canonical_relations.py', 'export_canonical.py',
               'verify_canonical.m', 'RATIONAL_MODELS.md']
    report = dict(id=row['id'], model_verified=True,
                  seconds=round(time.monotonic()-start, 2),
                  source_sha256={f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                                 for f in sources})
    (directory/'result.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-genus', type=int, default=7)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    inventory = json.loads((ROOT/'classification_inventory.json').read_text())
    rows = [r for r in inventory['curves']
            if 6 <= r['genus'] <= args.max_genus and r['quintic_status'] == 'UNRESOLVED']
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, row) for row in rows]
        for future in concurrent.futures.as_completed(futures):
            print(future.result(), flush=True)
    print('SUCCESS canonical batch finished', flush=True)


if __name__ == '__main__':
    main()
