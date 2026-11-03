"""Replay an elliptic-family finiteness certificate with Sage's Python.

Usage: sage -python run_family_certificate.py MODEL_KEY --prime 5
Only new local model data and standard Sage/Magma are used. Each curve has
an isolated directory. An unsuccessful assertion never writes a certificate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from sage.all import Matrix, QQ
from enumeration import units
from export_canonical import export
from published_gonality import at_least_six
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(key, prime):
    directory = ROOT/'family_jobs'/key
    forgetting = ROOT/'forgetting_jobs'/key
    mapping = json.loads((forgetting/'map.json').read_text())
    model_dir = ROOT/mapping['source_model']
    model = json.loads((model_dir/'result.json').read_text())
    row = json.loads((model_dir/'curve.json').read_text())
    assert model['model_verified'] and model['id'] == mapping['id'] == row['id']
    assert mapping['degree'] == row['degree_to_x0'] == 2
    assert at_least_six(row)
    assert mapping['source_sha256'] == digest(ROOT/'canonical_forgetting.py')
    for name, value in model['source_sha256'].items():
        assert digest(ROOT/name) == value
    for name, value in model['artifact_sha256'].items():
        assert digest(model_dir/name) == value
    source = json.loads((model_dir/'relations.json').read_text())
    target = json.loads((forgetting/'target_relations.json').read_text())
    assert tuple(target['invariants']['delta']) == units(row['level'])
    assert target['invariants']['level'] == row['level'] == mapping['target_level']
    assert (forgetting/'canonical_input.m').read_text() == export(target)
    precision = mapping['verified_precision']
    assert precision > row['index']//6
    S = Matrix(QQ,[[QQ(c) for c in v[:precision]] for v in source['basis_coefficients']])
    T = Matrix(QQ,[[QQ(c) for c in v[:precision]] for v in target['basis_coefficients']])
    linear = Matrix(QQ,mapping['linear_forms'])
    assert linear*S == T and linear.rank() == mapping['target_genus']
    subprocess.run([sys.executable,str(ROOT/'export_family_input.py'),key],check=True)
    subprocess.run([sys.executable,str(ROOT/'export_fricke_input.py'),str(forgetting)],check=True)
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],forgetting,
            'target_geometry.log','SUCCESS: canonical model identified by Hilbert polynomial')
    checked(['magma','-b',str(ROOT/'base_elliptic_quotient.m')],forgetting,
            'base_elliptic_quotient.log','SUCCESS degree-two positive-rank elliptic quotient')
    checked(['magma','-b',f'N:={row["level"]}',f'g:={row["genus"]}',
             'delta:='+','.join(map(str,row['delta'])),str(ROOT/'intermediate_factor_profile.m')],
            directory,'factor_profile.log','SUCCESS full intermediate factor profile')
    profile = (directory/'factor_profile.log').read_text()
    factors = re.findall(r'FACTOR dimension=(\d+) multiplicity=(\d+) central_zero=(true|false)',profile)
    assert sum(int(d)*int(m) for d,m,_ in factors) == row['genus']
    assert [(int(d),int(m)) for d,m,z in factors if z=='true'] == [(1,1)]
    orders = re.findall(rf'POTENTIAL_POSITIVE p={prime} polynomial=.* order=(\d+)',profile)
    assert len(orders) == 1
    order = int(orders[0])
    assert prime >= 5 and (4*order*row['level']) % prime != 0
    checked(['magma','-b',f'p:={prime}',str(ROOT/'verify_family_reduction.m')],directory,
            'good_reduction.log','SUCCESS good family models with unchanged Hilbert polynomials')
    checked(['magma','-b',f'p:={prime}',f'expected_order:={order}',
             str(ROOT/'finite_elliptic_families.m')],directory,
            'cosets_and_tangents.log','SUCCESS elliptic-family metadata')
    checked(['magma','-b',f'p:={prime}',str(ROOT/'family_tangent_immersion.m')],directory,
            'immersion.log','SUCCESS immersion at all')
    log = (directory/'cosets_and_tangents.log').read_text()
    assert 'extra_classes=0' in log and 'intersection_tangent_dimension=2' in log
    sources = ['run_family_certificate.py','canonical_forgetting.py',
               'canonical_relations.py','enumeration.py','export_canonical.py',
               'export_family_input.py','export_fricke_input.py',
               'verify_canonical_hilbert.m','base_elliptic_quotient.m',
               'intermediate_factor_profile.m','verify_family_reduction.m',
               'finite_elliptic_families.m','family_tangent_immersion.m',
               'published_gonality.py','ELLIPTIC_FAMILY_CERTIFICATE.md']
    artifacts = [model_dir/name for name in model['artifact_sha256']]
    artifacts += [model_dir/'result.json']
    artifacts += [forgetting/name for name in ['map.json','target_relations.json',
                  'canonical_input.m','target_qseries.m','target_geometry.log',
                  'base_elliptic_quotient.log']]
    artifacts += [directory/name for name in ['family_input.m','map.json','factor_profile.log',
                  'good_reduction.log','cosets_and_tangents.log','immersion.log']]
    certificate = dict(id=row['id'],prime=prime,elliptic_order=order,
                       status='FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES',
                       source_sha256={name:digest(ROOT/name) for name in sources},
                       artifact_sha256={str(path.relative_to(ROOT)):digest(path) for path in artifacts})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS complete elliptic-family finiteness certificate',row['id'],flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('--prime',type=int,required=True)
    args = parser.parse_args()
    run(args.key,args.prime)
