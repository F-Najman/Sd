"""Fresh replays of the level-40 genus-seven and level-48 genus-five positives."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(n):
    g,generators = (7,[7]) if n==40 else (5,[11])
    directory = ROOT/'last_positive_replays'/f'N{n}'
    directory.mkdir(parents=True,exist_ok=True)
    checked([sys.executable,str(ROOT/'canonical_relations.py'),str(n),
             '--generators',*map(str,generators),'--output','relations.json'],
            directory,'relations.log','SUCCESS exact relations')
    checked([sys.executable,str(ROOT/'export_canonical.py'),'relations.json'],
            directory,'export.log','')
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],directory,
            'geometry.log','SUCCESS: canonical model identified by Hilbert polynomial')
    script = 'verify_quintic40_genus7.m' if n==40 else 'search_closed_support.m'
    success = ('SUCCESS fixed genus-seven degree-five witness' if n==40
               else 'SUCCESS EXACT DEGREE FIVE from closed support')
    checked(['magma','-b',str(ROOT/script)],directory,'quintic.log',success)
    data = json.loads((directory/'relations.json').read_text())['invariants']
    assert data['level']==n and data['genus']==g
    sources = ['run_last_positive_audit.py','run_genus5_batch.py','canonical_relations.py',
               'enumeration.py','export_canonical.py','verify_canonical_hilbert.m',script,
               'RATIONAL_MODELS.md','MODEL_IDENTIFICATION.md']
    artifacts = ['relations.json','relations.log','export.log','canonical_input.m',
                 'geometry.log','quintic.log']
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    certificate = dict(id=str(n)+':'+','.join(map(str,data['delta'])),
                       status='INFINITE_BY_NEW_EXACT_FUNCTION',
                       source_sha256={s:digest(ROOT/s) for s in sources},
                       artifact_sha256={s:digest(directory/s) for s in artifacts})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS final explicit positive replay',n,flush=True)


if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run,[40,48]))
