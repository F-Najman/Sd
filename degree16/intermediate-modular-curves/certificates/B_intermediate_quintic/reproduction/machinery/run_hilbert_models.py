"""Fresh isolated models, using exact relations and Hilbert identification.

Run with Sage's Python. These jobs never modify canonical_jobs, where some
older direct smoothness verifications may still be running.
"""
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
    directory = ROOT/'hilbert_jobs'/key
    directory.mkdir(parents=True,exist_ok=True)
    metadata = directory/'curve.json'
    if metadata.exists():
        assert json.loads(metadata.read_text())['id'] == row['id']
    metadata.write_text(json.dumps(row,indent=2)+'\n')
    start = time.monotonic()
    checked([sys.executable,str(ROOT/'canonical_relations.py'),str(row['level']),
             '--generators',*map(str,row['delta']),'--maximum-degree','2',
             '--output','relations.json'],directory,'relations.log','SUCCESS exact relations')
    subprocess.run([sys.executable,str(ROOT/'export_canonical.py'),'relations.json'],
                   cwd=directory,check=True)
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],directory,
            'geometry.log','SUCCESS: canonical model identified by Hilbert polynomial')
    sources = ['enumeration.py','canonical_relations.py','export_canonical.py',
               'verify_canonical_hilbert.m','MODEL_IDENTIFICATION.md','RATIONAL_MODELS.md']
    artifacts = ['relations.json','canonical_input.m','geometry.log']
    result = dict(id=row['id'],model_verified=True,
                  seconds=round(time.monotonic()-start,2),
                  source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources},
                  artifact_sha256={f:hashlib.sha256((directory/f).read_bytes()).hexdigest() for f in artifacts})
    (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    rows = [r for r in json.loads((ROOT/'classification_inventory.json').read_text())['curves']
            if r['quintic_status']=='UNRESOLVED']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run,row) for row in rows]
        for future in concurrent.futures.as_completed(futures):
            print(future.result(),flush=True)
    print('SUCCESS Hilbert model batch finished',flush=True)
