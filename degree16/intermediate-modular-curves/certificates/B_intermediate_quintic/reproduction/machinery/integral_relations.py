"""Saturate the relation lattices without changing the canonical coordinates.

Clearing denominators one row at a time need not give the full integral
relation lattice. This distinction matters for reduction at small primes.
Run with Sage's Python, passing a directory containing relations.json.
"""
import hashlib
import json
from pathlib import Path
import sys
from sage.all import Matrix, QQ, ZZ, lcm
from export_canonical import export

directory = Path(sys.argv[1]).resolve()
original = directory/'relations.json'
data = json.loads(original.read_text())
for block in data['relation_blocks']:
    if not block['relations']:
        continue
    matrix = Matrix(QQ,[[QQ(c) for c in row] for row in block['relations']])
    integer = Matrix(ZZ,[[ZZ(c*lcm([x.denominator() for x in row])) for c in row]
                        for row in matrix.rows()])
    saturated = integer.row_module(ZZ).saturation().basis_matrix()
    assert saturated.nrows() == matrix.nrows()
    assert saturated.change_ring(QQ).row_space() == matrix.row_space()
    block['relations'] = [[str(c) for c in row] for row in saturated.rows()]
output = directory/'integral_model'
output.mkdir(exist_ok=True)
(output/'relations.json').write_text(json.dumps(data,indent=2)+'\n')
(output/'canonical_input.m').write_text(export(data))
report = dict(status='SAME_RATIONAL_RELATION_SPACES',
              original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(output/'saturation.json').write_text(json.dumps(report,indent=2)+'\n')
print('SUCCESS saturated integral relations',output)
