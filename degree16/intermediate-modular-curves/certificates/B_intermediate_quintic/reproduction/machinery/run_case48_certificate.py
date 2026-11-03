"""Full independent level-48 replay; run with Sage's Python and a model key."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent
CASES = {'2fea1fad025e6bab':(663552,2304,4,32),
         'efd0600330b90e51':(204800,12800,24,52)}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(key):
    frobenius_bound,order,count,special = CASES[key]
    parent = ROOT/'hilbert_jobs'/key
    model = json.loads((parent/'result.json').read_text())
    row = json.loads((parent/'curve.json').read_text())
    assert model['model_verified'] and model['id']==row['id']
    assert row['level']==48 and row['genus']==7
    for name,value in model['source_sha256'].items():
        assert digest(ROOT/name)==value
    for name,value in model['artifact_sha256'].items():
        assert digest(parent/name)==value
    work = parent/'case48_replay'
    work.mkdir(exist_ok=True)
    for name in ['result.json',*model['artifact_sha256']]:
        (work/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(parent/name,work/name)
    checked([sys.executable,str(ROOT/'integral_relations.py'),str(work)],work,
            'integral_relations.log','SUCCESS saturated integral relations')
    integral = work/'integral_model'
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],integral,
            'geometry_Q.log','SUCCESS: canonical model identified by Hilbert polynomial')
    metadata = ['N:=48','g:=7','delta:='+','.join(map(str,row['delta']))]
    checked(['magma','-b',*metadata,str(ROOT/'intermediate_central_value.m')],integral,
            'rank.log','SUCCESS intermediate central-value test')
    assert 'central_zero=false' in (integral/'rank.log').read_text()
    checked(['magma','-b',*metadata,str(ROOT/'torsion_order_bounds.m')],integral,
            'frobenius_bound.log','SUCCESS prime-to-characteristic torsion-order bound')
    assert f'rational_torsion_order_divides={frobenius_bound}' in (integral/'frobenius_bound.log').read_text()
    checked([sys.executable,str(ROOT/'pullback_torsion48.py'),str(integral),
             '--torsion-bound',str(frobenius_bound)],integral,
            'pullback_bound.log','SUCCESS exact full-homology pullback torsion bound')
    bound = json.loads((integral/'pullback_torsion48.json').read_text())
    assert bound['level']==48 and bound['delta']==row['delta']
    assert bound['pullback_restricted_bound']==order
    checked([sys.executable,str(ROOT/'canonical_j_map.py'),str(integral)],integral,
            'j_map.log','SUCCESS exact canonical j-map')
    jmap = integral/'j_map'
    checked(['magma','-b',str(ROOT/'export_closed_cusps.m')],jmap,
            'closed_cusps.log','SUCCESS all closed cusp ideals exported')
    checked(['magma','-b','p:=5',str(ROOT/'closed_cusp_support_sieve.m')],jmap,
            'support_sieve.log','SUCCESS closed-cusp sieve')
    sieve = (jmap/'support_sieve.log').read_text()
    assert f'subgroup_order={order} ' in sieve
    assert f'special_classes={special} closed_cusp_survivors={count}' in sieve
    checked(['magma','-b',f'expected_classes:={count}',str(ROOT/'verify_closed_cusp_classes.m')],jmap,
            'rational_classes.log',f'SUCCESS all {count} rational classes have no degree-five pencil')
    sources = ['run_case48_certificate.py','run_genus5_batch.py',
               'integral_relations.py','export_canonical.py','verify_canonical_hilbert.m',
               'intermediate_central_value.m','torsion_order_bounds.m',
               'integer_lattices.py','pullback_torsion48.py','canonical_j_map.py',
               'export_closed_cusps.m','closed_cusp_support_sieve.m',
               'verify_closed_cusp_classes.m','PULLBACK_TORSION48.md','RATIONAL_MODELS.md']
    artifacts = [parent/'result.json']+[parent/name for name in model['artifact_sha256']]
    artifacts += sorted(p for p in work.rglob('*') if p.is_file())
    certificate = dict(id=row['id'],status='FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE',
                       rational_torsion_order=order,special_classes_checked=count,
                       source_sha256={name:digest(ROOT/name) for name in sources},
                       artifact_sha256={str(p.relative_to(ROOT)):digest(p) for p in artifacts})
    (parent/'case48_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS complete level-48 rank-zero class-sieve certificate',row['id'],flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key',choices=CASES)
    run(parser.parse_args().key)
