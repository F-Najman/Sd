"""Replay the full level-40 torsion/class-sieve certificate with Sage Python.

All derived inputs are rebuilt in a separate directory. The only supplied
search data are six rational points, each checked against the curve equations.
No negative search label or home-directory code is imported.
"""
import hashlib
import json
from math import gcd, prod
from pathlib import Path
import shutil
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    parent = ROOT/'hilbert_jobs/82f731393c98cb7c'
    model = json.loads((parent/'result.json').read_text())
    row = json.loads((parent/'curve.json').read_text())
    assert model['model_verified'] and model['id'] == row['id']
    assert row['id'] == '40:1,3,9,13,27,31,37,39'
    for name,value in model['source_sha256'].items():
        assert digest(ROOT/name) == value
    for name,value in model['artifact_sha256'].items():
        assert digest(parent/name) == value
    work = parent/'case40_final_replay'
    work.mkdir(exist_ok=True)
    # Do not overwrite any active exploratory model or its input files.
    shutil.copyfile(parent/'relations.json',work/'relations.json')
    checked([sys.executable,str(ROOT/'integral_relations.py'),str(work)],work,
            'integral_relations.log','SUCCESS saturated integral relations')
    integral = work/'integral_model'
    shutil.copyfile(parent/'integral_model/small_points.m',integral/'small_points.m')
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],integral,
            'geometry_Q.log','SUCCESS: canonical model identified by Hilbert polynomial')
    metadata = ['N:=40','g:=7','delta:='+','.join(map(str,row['delta']))]
    checked(['magma','-b',*metadata,str(ROOT/'intermediate_central_value.m')],integral,
            'rank.log','SUCCESS intermediate central-value test')
    assert 'central_zero=false' in (integral/'rank.log').read_text()
    checked(['magma','-b',*metadata,str(ROOT/'torsion_order_bounds.m')],integral,
            'frobenius_bound.log','SUCCESS prime-to-characteristic torsion-order bound')
    assert 'rational_torsion_order_divides=28224' in (integral/'frobenius_bound.log').read_text()
    checked([sys.executable,str(ROOT/'audit_integral_homology40.py')],integral,
            'homology_audit.log','SUCCESS full integral Manin lattice and exact cusp-boundary kernel')
    checked([sys.executable,str(ROOT/'integral_torsion_probe.py'),str(integral)],integral,
            'hecke_bound.log',"'omit_residue_prime': 13")
    bound = json.loads((integral/'integral_torsion_probe.json').read_text())
    assert bound['level'] == 40 and bound['delta'] == row['delta']
    assert {r['omit_residue_prime'] for r in bound['results']} == {0,3,7,11,13}
    assert all(prod(r['smith']) == 8064 for r in bound['results'])
    assert gcd(8064,28224) == 4032
    checked(['magma','-b','p:=3',str(ROOT/'rational_support_sieve.m')],integral,
            'support_sieve_p3.log','SUCCESS rational-support class sieve')
    sieve = (integral/'support_sieve_p3.log').read_text()
    assert 'rational_support_points=6 subgroup_order=4032' in sieve
    assert 'special_classes=16 rational_support_survivors=12' in sieve
    checked([sys.executable,str(ROOT/'reduce_canonical_basis.py'),str(integral)],integral,
            'coordinate_change.log','SUCCESS exact coordinate isomorphism')
    reduced = integral/'reduced_model'
    checked(['magma','-b','p:=3',str(ROOT/'shorten_signed_support.m')],reduced,
            'short_support.log','SUCCESS shorter representatives with exactly the same reduction classes')

    checked(['magma','-b',str(ROOT/'verify_effective_canonical_classes.m')],reduced,
            'all_classes.log','SUCCESS all 12 classes excluded by exact canonical fat-point conditions')
    sources = ['run_case40_certificate.py','run_genus5_batch.py',
               'integral_relations.py','export_canonical.py',
               'verify_canonical_hilbert.m','intermediate_central_value.m',
               'torsion_order_bounds.m','audit_integral_homology40.py',
               'integral_torsion_probe.py','rational_support_sieve.m',
               'reduce_canonical_basis.py','shorten_signed_support.m','verify_effective_canonical_classes.m',
               'HECKE_TORSION40.md','RATIONAL_MODELS.md']
    artifacts = [parent/'result.json']+[parent/name for name in model['artifact_sha256']]
    artifacts += sorted(p for p in work.rglob('*') if p.is_file())
    certificate = dict(id=row['id'],status='FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE',
                       rational_torsion_order=4032,special_classes_checked=12,
                       source_sha256={name:digest(ROOT/name) for name in sources},
                       artifact_sha256={str(p.relative_to(ROOT)):digest(p) for p in artifacts})
    (parent/'case40_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS complete level-40 rank-zero class-sieve certificate',flush=True)


if __name__ == '__main__':
    run()
