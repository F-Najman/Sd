"""Full level-65 family replay at prime three, including exact rebasing.

Run with Sage's Python and a model key. This uses the smooth-lift version
of the family criterion; no prime-to-#E(F_p) assertion is made. Inputs are
regenerated in the separate family3_jobs directory, never in family_jobs.
"""
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


def run(key):
    directory = ROOT/'family3_jobs'/key
    forgetting = ROOT/'forgetting_jobs'/key
    mapping = json.loads((forgetting/'map.json').read_text())
    model_dir = ROOT/mapping['source_model']
    model = json.loads((model_dir/'result.json').read_text())
    row = json.loads((model_dir/'curve.json').read_text())
    assert model['model_verified'] and model['id']==mapping['id']==row['id']
    assert row['level']==65 and row['genus'] in [9,11]
    assert mapping['degree']==row['degree_to_x0']==2 and at_least_six(row)
    assert mapping['source_sha256']==digest(ROOT/'canonical_forgetting.py')
    for name,value in model['source_sha256'].items():
        assert digest(ROOT/name)==value
    for name,value in model['artifact_sha256'].items():
        assert digest(model_dir/name)==value
    source = json.loads((model_dir/'relations.json').read_text())
    target = json.loads((forgetting/'target_relations.json').read_text())
    assert tuple(target['invariants']['delta'])==units(65)
    assert target['invariants']['level']==mapping['target_level']==65
    assert (forgetting/'canonical_input.m').read_text()==export(target)
    precision = mapping['verified_precision']
    assert precision>row['index']//6
    S = Matrix(QQ,[[QQ(c) for c in v[:precision]] for v in source['basis_coefficients']])
    T = Matrix(QQ,[[QQ(c) for c in v[:precision]] for v in target['basis_coefficients']])
    linear = Matrix(QQ,mapping['linear_forms'])
    assert linear*S==T and linear.rank()==5
    subprocess.run([sys.executable,str(ROOT/'prepare_family3_models.py'),key],check=True)
    subprocess.run([sys.executable,str(ROOT/'export_fricke_input.py'),str(forgetting)],check=True)
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],forgetting,
            'target_geometry.log','SUCCESS: canonical model identified by Hilbert polynomial')
    checked(['magma','-b',str(ROOT/'base_elliptic_quotient.m')],forgetting,
            'base_elliptic_quotient.log','SUCCESS degree-two positive-rank elliptic quotient')
    checked(['magma','-b','N:=65',f'g:={row["genus"]}',
             'delta:='+','.join(map(str,row['delta'])),str(ROOT/'intermediate_factor_profile.m')],
            directory,'factor_profile.log','SUCCESS full intermediate factor profile')
    profile = (directory/'factor_profile.log').read_text()
    factors = re.findall(r'FACTOR dimension=(\d+) multiplicity=(\d+) central_zero=(true|false)',profile)
    assert sum(int(d)*int(m) for d,m,_ in factors)==row['genus']
    assert [(int(d),int(m)) for d,m,z in factors if z=='true']==[(1,1)]
    orders = re.findall(r'POTENTIAL_POSITIVE p=3 polynomial=.* order=(\d+)',profile)
    assert len(orders)==1 and int(orders[0])==6
    checked(['magma','-b','p:=3',str(ROOT/'verify_family_reduction.m')],directory,
            'good_reduction.log','SUCCESS good family models with unchanged Hilbert polynomials')
    checked(['magma','-b','p:=3','expected_order:=6',str(ROOT/'verify_elliptic_family65.m')],
            directory,'cosets_and_tangents.log','SUCCESS elliptic-family metadata')
    checked(['magma','-b','p:=3','expected_order:=6',str(ROOT/'verify_elliptic_immersion65.m')],
            directory,'immersion.log','SUCCESS immersion at all')
    sources = ['run_family3_certificate.py','prepare_family3_models.py','reduce_canonical_basis.py',
               'canonical_forgetting.py','canonical_relations.py','enumeration.py','export_canonical.py',
               'export_fricke_input.py','verify_canonical_hilbert.m','base_elliptic_quotient.m',
               'intermediate_factor_profile.m','verify_family_reduction.m','verify_elliptic_family65.m',
               'verify_elliptic_immersion65.m','published_gonality.py','ELLIPTIC_FAMILY_CERTIFICATE.md',
               'quotient_rational_fibers.m','linear_scheme_divisor.m','canonical_elliptic_fibers.m',
               'ELLIPTIC_FAMILY65_LINEAR.md','ELLIPTIC_FAMILY_SMALL_PRIME.md','run_genus5_batch.py']
    artifacts = [model_dir/name for name in model['artifact_sha256']]+[model_dir/'result.json']
    artifacts += [forgetting/name for name in ['map.json','target_relations.json','canonical_input.m',
                  'target_qseries.m','target_geometry.log','base_elliptic_quotient.log']]
    artifacts += [directory/name for name in ['family_input.m','original_map.json','factor_profile.log',
                  'good_reduction.log','cosets_and_tangents.log','immersion.log']]
    for label in ['source','target']:
        artifacts += [directory/label/'relations.json']
        artifacts += [directory/label/'reduced_model'/name for name in
                      ['relations.json','canonical_input.m','coordinate_change.json']]
    certificate = dict(id=row['id'],prime=3,elliptic_order=6,
                       status='FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES',
                       source_sha256={name:digest(ROOT/name) for name in sources},
                       artifact_sha256={str(path.relative_to(ROOT)):digest(path) for path in artifacts})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS complete small-prime elliptic-family finiteness certificate',row['id'],flush=True)


if __name__=='__main__':
    run(sys.argv[1])
