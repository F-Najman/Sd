"""Parallel positive-witness searches on the new Hilbert-certified models."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(row):
    directory = ROOT/row['model_certificate']
    model = json.loads((directory/'result.json').read_text())
    assert model['id'] == row['id'] and model['model_verified']
    for f,digest in model['source_sha256'].items():
        assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest() == digest
    for f,digest in model['artifact_sha256'].items():
        assert hashlib.sha256((directory/f).read_bytes()).hexdigest() == digest
    script = ROOT/'search_mixed_divisors.m'
    checked(['magma','-b',str(script)],directory,'mixed_divisors.log','')
    log = (directory/'mixed_divisors.log').read_text()
    found = 'SUCCESS EXACT DEGREE FIVE mixed divisor' in log
    assert found or 'SEARCH FINISHED:' in log
    report = dict(id=row['id'],exact_function_found=found,
                  source_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                  log_sha256=hashlib.sha256((directory/'mixed_divisors.log').read_bytes()).hexdigest())
    (directory/'mixed_result.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    rows = [r for r in json.loads((ROOT/'classification_inventory.json').read_text())['curves']
            if r['quintic_status']=='UNRESOLVED' and r['degree5_function']=='UNKNOWN']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run,row) for row in rows]
        for future in concurrent.futures.as_completed(futures):
            print(future.result(),flush=True)
    print('SUCCESS mixed-divisor batch finished',flush=True)
