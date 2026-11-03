"""Fresh, isolated replays of the five original genus-five batch witnesses.

Run with Sage's Python. The subgroup generators below specify the inputs;
no old equations, search outputs, or classification labels are trusted.
The new manifests include artifact hashes, unlike the early batch logs.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
CASES = [(30,[11]),(32,[15]),(39,[4]),(40,[9,11]),(45,[4])]


def run(case):
    n,generators = case
    directory = ROOT/'batch_positive_replays'/f'N{n}'
    directory.mkdir(parents=True,exist_ok=True)
    checked([sys.executable,str(ROOT/'canonical_relations.py'),str(n),
             '--generators',*map(str,generators),'--output','relations.json'],
            directory,'relations.log','SUCCESS exact relations')
    checked([sys.executable,str(ROOT/'export_genus5.py'),'relations.json'],
            directory,'export.log','')
    checked(['magma','-b',str(ROOT/'verify_genus5.m')],directory,
            'geometry.log','SUCCESS: smooth genus-five complete intersection')
    artifacts = ['relations.json','relations.log','export.log',
                 'genus5_input.m','geometry.log']
    found = False
    for script,log in [('search_quintic_genus5.m','effective.log'),
                       ('search_residual_genus5.m','residual.log')]:
        checked(['magma','-b',str(ROOT/script)],directory,log,'')
        artifacts.append(log)
        output = (directory/log).read_text()
        if 'SUCCESS EXACT DEGREE FIVE' in output:
            found = True
            break
        assert 'SEARCH FINISHED:' in output
    assert found, 'No witness: no certificate may be written'
    data = json.loads((directory/'relations.json').read_text())['invariants']
    assert data['level']==n and data['genus']==5
    sources = ['run_batch_positive_audit.py','run_genus5_batch.py',
               'canonical_relations.py','enumeration.py','export_genus5.py',
               'verify_genus5.m','search_quintic_genus5.m',
               'search_residual_genus5.m','RATIONAL_MODELS.md','MODEL_IDENTIFICATION.md']
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    certificate = dict(id=str(n)+':'+','.join(map(str,data['delta'])),
                       status='INFINITE_BY_NEW_EXACT_FUNCTION',
                       source_sha256={name:digest(ROOT/name) for name in sources},
                       artifact_sha256={name:digest(directory/name) for name in artifacts})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS independently regenerated batch quintic',n,flush=True)


if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(run,CASES))
