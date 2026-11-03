"""Exact, reversible coordinate simplification; run with Sage's Python.

LLL is only a performance heuristic. Correctness comes from checking an
invertible rational matrix and transforming every defining equation by its
inverse. This does not establish good reduction or any gonality assertion.
The input directory and its certificates are never changed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from sage.all import Matrix, PolynomialRing, QQ, ZZ, lcm, prod
from export_canonical import export


def simplify(directory):
    source = directory / 'relations.json'
    data = json.loads(source.read_text())
    old = Matrix(QQ, data['basis_coefficients'])
    g = old.nrows()
    denominator = lcm(c.denominator() for c in old.list())
    lattice = (denominator * old).change_ring(ZZ).row_module().saturation()
    reduced = lattice.basis_matrix().LLL().change_ring(QQ)
    transform = old.solve_left(reduced)
    assert transform.det() != 0 and transform * old == reduced
    inverse = transform.inverse()
    ring = PolynomialRing(QQ, g, 'y')
    variables = ring.gens()
    substitutions = [sum(inverse[i,j]*variables[j] for j in range(g))
                     for i in range(g)]
    forward = [sum(transform[i,j]*variables[j] for j in range(g))
               for i in range(g)]
    for block in data['relation_blocks']:
        monomials = [prod(variables[j] for j in indices)
                     for indices in block['monomials']]
        rows = []
        for row in block['relations']:
            original = sum(QQ(c)*m for c,m in zip(row,monomials))
            changed = original(*substitutions)
            assert changed(*forward) == original
            rows.append([changed.monomial_coefficient(m) for m in monomials])
        if rows:
            matrix = Matrix(QQ, rows)
            integer = Matrix(ZZ, [list(lcm(c.denominator() for c in row)*row)
                                  for row in matrix.rows()])
            short = integer.row_module().saturation().basis_matrix().LLL()
            assert short.change_ring(QQ).row_space() == matrix.row_space()
            block['relations'] = [[str(c) for c in row] for row in short.rows()]
    data['basis_coefficients'] = [[str(c) for c in row] for row in reduced.rows()]
    output = directory / 'reduced_model'
    output.mkdir(exist_ok=True)
    (output/'relations.json').write_text(json.dumps(data,indent=2)+'\n')
    (output/'canonical_input.m').write_text(export(data))
    report = dict(status='EXACT_RATIONAL_COORDINATE_ISOMORPHISM',
                  convention='new_coordinates = transform * old_coordinates',
                  transform=[[str(c) for c in row] for row in transform.rows()],
                  inverse=[[str(c) for c in row] for row in inverse.rows()],
                  input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (output/'coordinate_change.json').write_text(json.dumps(report,indent=2)+'\n')
    magma_matrix = ('coordinate_transform := Matrix(Rationals(),'+str(g)+','+str(g)
                    +',['+','.join(str(c) for c in transform.list())+']);\n')
    for filename, variable in [('small_points.m','small_points'),
                               ('signed_support_candidates.m','support_points')]:
        if (directory/filename).exists():
            # Copy the supplied data, not a runtime dependency on another model.
            text = (directory/filename).read_text()
            text += '\n'+magma_matrix
            text += (variable+' := [Eltseq(Vector(Rationals(),v)*'
                     'Transpose(coordinate_transform)):v in '+variable+'];\n')
            (output/filename).write_text(text)
    print('SUCCESS exact coordinate isomorphism',output,flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    simplify(parser.parse_args().directory.resolve())
