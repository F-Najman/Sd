"""Regenerate the four initial explicit quintic witnesses and hash all inputs.

Run with Sage's Python. Each level has an isolated directory, and equations
are regenerated from q-expansions before geometry and function degrees run.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
CASES = [(33,2),(34,9),(35,4),(41,2)]


def run(case):
    n,generator = case
    directory = ROOT/'positive_replays'/f'N{n}'
    directory.mkdir(parents=True,exist_ok=True)
    checked([sys.executable,str(ROOT/'canonical_relations.py'),str(n),
             '--generators',str(generator),'--output','relations.json'],directory,
            'relations.log','SUCCESS exact relations')
    checked([sys.executable,str(ROOT/'export_genus5.py'),'relations.json'],directory,
            'export.log','')
    shutil.copyfile(directory/'genus5_input.m',directory/f'model_{n}.m')
    checked(['magma','-b',str(ROOT/'verify_genus5.m')],directory,
            'geometry.log','SUCCESS: smooth genus-five complete intersection')
    checked(['magma','-b',str(ROOT/f'quintic_{n}.m')],directory,
            'quintic.log',f'SUCCESS quintic_{n}:')
    data = json.loads((directory/'relations.json').read_text())['invariants']
    assert data['level']==n and data['genus']==5
    sources = ['run_explicit_positive_audit.py','run_genus5_batch.py',
               'canonical_relations.py','enumeration.py','export_genus5.py',
               'verify_genus5.m',f'quintic_{n}.m','RATIONAL_MODELS.md','MODEL_IDENTIFICATION.md']
    artifacts = ['relations.json','relations.log','export.log','genus5_input.m',
                 f'model_{n}.m','geometry.log','quintic.log']
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    certificate = dict(id=str(n)+':'+','.join(map(str,data['delta'])),
                       status='INFINITE_BY_NEW_EXACT_FUNCTION',
                       source_sha256={name:digest(ROOT/name) for name in sources},
                       artifact_sha256={name:digest(directory/name) for name in artifacts})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS independently regenerated explicit quintic',n,flush=True)


if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(run,CASES))
