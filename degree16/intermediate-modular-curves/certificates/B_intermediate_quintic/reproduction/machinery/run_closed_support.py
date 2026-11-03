"""Reproducible closed-support searches on the two remaining genus-five models."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
from export_canonical import export
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(name):
    directory = ROOT/'genus5_jobs'/name
    model = json.loads((directory/'result.json').read_text())
    assert model['model_verified']
    for filename, digest in model['source_sha256'].items():
        assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest() == digest
    relations = json.loads((directory/'relations.json').read_text())
    assert (directory/'canonical_input.m').read_text() == export(relations)
    script = ROOT/'search_closed_support.m'
    checked(['magma', '-b', str(script)], directory, 'closed_support.log', '')
    log = (directory/'closed_support.log').read_text()
    found = 'SUCCESS EXACT DEGREE FIVE from closed support' in log
    assert found or 'SEARCH FINISHED:' in log
    report = dict(id=model['id'], exact_function_found=found,
                  source_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                  artifact_sha256={f:hashlib.sha256((directory/f).read_bytes()).hexdigest()
                                   for f in ['relations.json','canonical_input.m','closed_support.log']})
    (directory/'closed_support_result.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(run, ['N48_d2','N64_d2']):
            print(result, flush=True)
    print('SUCCESS closed-support batch; negative searches are inconclusive.')
