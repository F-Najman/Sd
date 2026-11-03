"""Export a verified forgetting map with saturated integral equations.

Run with Sage's Python. Saturation changes relation bases, not coordinates.
"""
import json
from pathlib import Path
import re
import sys
from export_canonical import export
from sage.all import Matrix, QQ, ZZ, lcm

ROOT = Path(__file__).resolve().parent
key = sys.argv[1]
forgetting = ROOT/'forgetting_jobs'/key
mapping = json.loads((forgetting/'map.json').read_text())
source = json.loads((ROOT/mapping['source_model']/'relations.json').read_text())
target = json.loads((forgetting/'target_relations.json').read_text())
directory = ROOT/'family_jobs'/key
directory.mkdir(parents=True,exist_ok=True)


def model_text(data,prefix):
    for block in data['relation_blocks']:
        if not block['relations']:
            continue
        matrix = Matrix(QQ,[[QQ(c) for c in row] for row in block['relations']])
        integer = Matrix(ZZ,[[ZZ(c*lcm([x.denominator() for x in row])) for c in row]
                            for row in matrix.rows()])
        lattice = integer.row_module(ZZ).saturation().basis_matrix()
        assert lattice.change_ring(QQ).row_space() == matrix.row_space()
        block['relations'] = [[str(c) for c in row] for row in lattice.rows()]
    replacements = {'R':prefix+'R','equations':prefix+'equations',
                    'expected_genus':prefix+'genus','cusp_coordinates':prefix+'cusp'}
    return re.sub(r'\b(R|equations|expected_genus|cusp_coordinates)\b',
                  lambda match:replacements[match.group()],export(data))


text = model_text(source,'source_')+model_text(target,'target_')
text += f'N := {mapping["target_level"]};\ncover_degree := {mapping["degree"]};\n'
text += f'L := Matrix(Rationals(),{mapping["target_genus"]},{source["invariants"]["genus"]},['
text += ','.join(c for row in mapping['linear_forms'] for c in row)+']);\n'
precision = target['precision']
text += f'precision := {precision};\ntarget_basis := Matrix(Rationals(),{mapping["target_genus"]},{precision-1},['
text += ','.join(c for row in target['basis_coefficients'] for c in row[1:precision])+']);\n'
(directory/'family_input.m').write_text(text)
(directory/'map.json').write_text(json.dumps(mapping,indent=2)+'\n')
print('SUCCESS family input',directory)
