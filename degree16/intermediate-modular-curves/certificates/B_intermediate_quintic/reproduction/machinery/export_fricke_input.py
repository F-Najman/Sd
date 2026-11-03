"""Export the canonical q-basis for an independent Magma Fricke calculation."""
import json
from pathlib import Path
import sys

directory = Path(sys.argv[1])
data = json.loads((directory/'target_relations.json').read_text())
n = data['invariants']['level']
g = data['invariants']['genus']
precision = data['precision']
coefficients = [c for row in data['basis_coefficients'] for c in row[1:precision]]
(directory/'target_qseries.m').write_text(
    f'N := {n};\nprecision := {precision};\n'
    + f'target_basis := Matrix(Rationals(),{g},{precision-1},['
    + ','.join(coefficients)+']);\n')
