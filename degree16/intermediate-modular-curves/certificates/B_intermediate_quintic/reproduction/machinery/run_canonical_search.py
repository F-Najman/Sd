"""Search completed canonical models without modifying model artifacts.

Genus seven is the default. Search outputs do not change the density ledger
until the exact witness and its source hash have separately been accepted.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(directory):
    model = json.loads((directory/'result.json').read_text())
    assert model['model_verified']
    for filename, digest in model['source_sha256'].items():
        assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest() == digest
    script = ROOT/'search_quintic_canonical.m'
    checked(['magma', '-b', str(script)], directory, 'quintic_search.log', '')
    log = (directory/'quintic_search.log').read_text()
    found = 'SUCCESS EXACT DEGREE FIVE' in log
    assert found or 'SEARCH FINISHED:' in log
    result = dict(id=model['id'], exact_function_found=found,
                  search_source_sha256=hashlib.sha256(script.read_bytes()).hexdigest())
    (directory/'search_result.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-genus', type=int, default=7)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    directories = [p.parent for p in sorted((ROOT/'canonical_jobs').glob('*/result.json'))
                   if json.loads((p.parent/'curve.json').read_text())['genus'] <= args.max_genus]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, d) for d in directories]
        for future in concurrent.futures.as_completed(futures):
            print(future.result(), flush=True)
    print('SUCCESS bounded search batch finished', flush=True)


if __name__ == '__main__':
    main()
