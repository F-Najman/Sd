"""Regenerate the canonical models underlying all twelve special negatives.

Run with Sage's Python. Unlike replay_special.py, this starts from the
level and full subgroup, not saved Fourier coefficients. It then checks
exact equality with the model data used by the negative certificates.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent/'audit_runs'/'special_models'
METHODS = {'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE',
           'FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO',
           'FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION',
           'FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES'}
sys.path.insert(0,str(ROOT))
from run_genus5_batch import checked


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(row):
    key = hashlib.sha256(row['id'].encode()).hexdigest()[:16]
    accepted = ROOT/'hilbert_jobs'/key
    old = json.loads((accepted/'relations.json').read_text())
    degree = max(block['degree'] for block in old['relation_blocks'])
    directory = OUT/key
    directory.mkdir()  # Do not silently replace a previous or live replay.
    checked([sys.executable,str(ROOT/'canonical_relations.py'),str(row['level']),
             '--generators',*map(str,row['delta']),'--maximum-degree',str(degree),
             '--output','relations.json'],directory,'relations.log','SUCCESS exact relations')
    checked([sys.executable,str(ROOT/'export_canonical.py'),'relations.json'],
            directory,'export.log','')
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],directory,
            'geometry.log','SUCCESS: canonical model identified by Hilbert polynomial')
    fresh = json.loads((directory/'relations.json').read_text())
    # Exact equality includes the full basis, all Sturm relations, precision,
    # subgroup signature and the generating source hash; timing is not stored.
    assert fresh == old, (key,'fresh canonical data differ from certificate input')
    assert (directory/'canonical_input.m').read_bytes() == (accepted/'canonical_input.m').read_bytes()
    sources = ['canonical_relations.py','enumeration.py','export_canonical.py',
               'verify_canonical_hilbert.m','run_genus5_batch.py']
    receipt = dict(status='FRESH_SPECIAL_MODEL_PASS',id=row['id'],
                   accepted_input=str(accepted.relative_to(ROOT)),
                   source_sha256={name:digest(ROOT/name) for name in sources},
                   outputs={p.name:digest(p) for p in sorted(directory.iterdir()) if p.is_file()})
    (directory/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS fresh model',row['id'],flush=True)
    return key


if __name__ == '__main__':
    rows = [r for r in json.loads((ROOT/'complete_inventory.json').read_text())['curves']
            if r['strict'] and r['quintic_status'] in METHODS]
    assert len(rows) == 12
    OUT.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        keys = list(pool.map(run,rows))
    receipt = dict(status='FRESH_ALL_12_SPECIAL_MODELS_PASS',
                   receipts={key:digest(OUT/key/'receipt.json') for key in keys})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(receipt['status'],flush=True)
