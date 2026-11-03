"""Exact coordinate changes for a small-prime family experiment.

Preserves every original input. Good reduction is a separate Magma check;
LLL or integral coefficients alone never certify it.
"""
import hashlib
import json
from pathlib import Path
import re
import sys
from sage.all import Matrix, QQ, GF
from export_canonical import export
from reduce_canonical_basis import simplify

ROOT = Path(__file__).resolve().parent
key = sys.argv[1]
forgetting = ROOT/'forgetting_jobs'/key
mapping = json.loads((forgetting/'map.json').read_text())
assert mapping['target_level'] == 65 and mapping['degree'] == 2
original_source = ROOT/mapping['source_model']
certificate = json.loads((original_source/'result.json').read_text())
assert certificate['model_verified'] and certificate['id']==mapping['id']
for name,digest in certificate['source_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
for name,digest in certificate['artifact_sha256'].items():
    assert hashlib.sha256((original_source/name).read_bytes()).hexdigest()==digest
assert mapping['source_sha256']==hashlib.sha256((ROOT/'canonical_forgetting.py').read_bytes()).hexdigest()
directory = ROOT/'family3_jobs'/key
directory.mkdir(parents=True,exist_ok=True)
models = []
transforms = []
for label,path in [('source',original_source/'relations.json'),
                   ('target',forgetting/'target_relations.json')]:
    local = directory/label
    local.mkdir(exist_ok=True)
    (local/'relations.json').write_bytes(path.read_bytes())
    simplify(local)
    models.append(json.loads((local/'reduced_model/relations.json').read_text()))
    transforms.append(Matrix(QQ,json.loads((local/'reduced_model/coordinate_change.json').read_text())['transform']))
source,target = models
assert source['invariants']['level'] == target['invariants']['level'] == 65
assert source['invariants']['genus'] in [9,11] and target['invariants']['genus'] == 5
T,U = transforms
L = U*Matrix(QQ,mapping['linear_forms'])*T.inverse()
precision = min(source['precision'],target['precision'])
assert precision > source['invariants']['index']//6
S = Matrix(QQ,[row[:precision] for row in source['basis_coefficients']])
B = Matrix(QQ,[row[:precision] for row in target['basis_coefficients']])
assert L*S==B
assert all(c.denominator()%3 for c in L.list())
assert L.change_ring(GF(3)).rank()==target['invariants']['genus']


def renamed(data,prefix):
    names = {'R':prefix+'R','equations':prefix+'equations',
             'expected_genus':prefix+'genus','cusp_coordinates':prefix+'cusp'}
    return re.sub(r'\b(R|equations|expected_genus|cusp_coordinates)\b',
                  lambda m:names[m.group()],export(data))


text = renamed(source,'source_')+renamed(target,'target_')
text += f'N := 65;\ncover_degree := 2;\nL := Matrix(Rationals(),{L.nrows()},{L.ncols()},['
text += ','.join(str(c) for c in L.list())+']);\n'
text += f'precision := {precision};\ntarget_basis := Matrix(Rationals(),{B.nrows()},{precision-1},['
text += ','.join(str(c) for row in B.rows() for c in row[1:])+']);\n'
(directory/'family_input.m').write_text(text)
(directory/'original_map.json').write_text(json.dumps(mapping,indent=2)+'\n')
print('SUCCESS exact transformed family input',key,flush=True)
