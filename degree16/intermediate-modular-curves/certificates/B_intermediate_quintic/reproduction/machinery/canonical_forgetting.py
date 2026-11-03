"""Construct exact rational forgetting maps using full canonical q-expansions.

The output linear systems describe rational projective maps (ramification
can give basepoints). They extend uniquely to morphisms of smooth curves.
Their modular interpretation and degree follow from the subgroup inclusion,
not from treating the displayed projective linear system as basepoint-free.
Run with Sage's Python. All input models come from the new Hilbert jobs.
"""
import hashlib
import json
from pathlib import Path
import subprocess
from sage.all import Matrix, QQ, vector
from canonical_relations import construct
from enumeration import units, signature
from export_canonical import export
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(row):
    n = row['level']
    source_dir = ROOT/row['model_certificate']
    source = json.loads((source_dir/'relations.json').read_text())
    model = json.loads((source_dir/'result.json').read_text())
    assert model['id'] == row['id'] and model['model_verified']
    for f,digest in model['source_sha256'].items():
        assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest() == digest
    for f,digest in model['artifact_sha256'].items():
        assert hashlib.sha256((source_dir/f).read_bytes()).hexdigest() == digest
    target_genus = signature(n,units(n))['genus']
    target = construct(n,list(units(n)),4 if target_genus == 3 else 3)
    key = hashlib.sha256(row['id'].encode()).hexdigest()[:16]
    directory = ROOT/'forgetting_jobs'/key
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'target_relations.json').write_text(json.dumps(target,indent=2)+'\n')
    (directory/'canonical_input.m').write_text(export(target))
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],directory,
            'target_geometry.log','SUCCESS: canonical model identified by Hilbert polynomial')
    precision = min(source['precision'],target['precision'])
    # Agreement of weight-two forms is certified on the smaller subgroup.
    assert precision > source['invariants']['index']//6
    S = Matrix(QQ,[[QQ(c) for c in f[:precision]] for f in source['basis_coefficients']])
    T = Matrix(QQ,[[QQ(c) for c in f[:precision]] for f in target['basis_coefficients']])
    assert S.rank() == row['genus']
    linear = Matrix(QQ,[S.solve_left(vector(QQ,v)) for v in T.rows()])
    assert linear*S == T and linear.rank() == target_genus
    # Since Gamma_Delta is a subgroup of Gamma_0, these are the actual
    # pullbacks of target differentials. A complete canonical target system
    # separates its points, so this identifies the forgetting map itself.
    degree = row['index']//target['invariants']['index']
    assert degree == row['degree_to_x0'] and degree > 1
    report = dict(id=row['id'],source_model=row['model_certificate'],
                  target_level=n,target_delta=list(units(n)),target_genus=target_genus,
                  degree=degree,verified_precision=precision,
                  linear_forms=[[str(c) for c in v] for v in linear.rows()],
                  status='EXACT_CANONICAL_FORGETTING_MAP',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (directory/'map.json').write_text(json.dumps(report,indent=2)+'\n')
    return row['id'],degree,target_genus


if __name__ == '__main__':
    rows = [r for r in json.loads((ROOT/'classification_inventory.json').read_text())['curves']
            if r['quintic_status']=='UNRESOLVED' and r['degree5_function']=='DOES_NOT_EXIST']
    for row in rows:
        print(run(row),flush=True)
    print('SUCCESS exact canonical forgetting maps',flush=True)
