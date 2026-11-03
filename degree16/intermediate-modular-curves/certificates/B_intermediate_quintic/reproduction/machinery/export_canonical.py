"""Export canonical relations and the rational q-expansion cusp to Magma.

This exporter does not certify a model: run verify_canonical.m afterwards.
Both quadratic and cubic relations are included, so the geometric check does
not depend on an assumed Petri exception classification.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def export(data):
    assert data['relation_status'] == 'EXACT_RELATIONS'
    g = data['invariants']['genus']
    assert g >= 3
    quadratic = next(b for b in data['relation_blocks'] if b['degree'] == 2)
    # This is the dimension of the quadratic canonical image for a
    # nonhyperelliptic curve. For a hyperelliptic curve it is 2*g-1.
    assert quadratic['product_rank'] == 3*g-3
    assert 3*g-3 != 2*g-1
    equations = []
    for block in data['relation_blocks']:
        for row in block['relations']:
            assert len(row) == len(block['monomials'])
            terms = []
            for coefficient, indices in zip(row, block['monomials']):
                c = Fraction(coefficient)
                if c:
                    terms.append(f'({c})*' + '*'.join(f'R.{j+1}' for j in indices))
            assert terms
            equations.append('+'.join(terms))
    coefficients = [[Fraction(c) for c in row] for row in data['basis_coefficients']]
    first = next(i for i in range(data['precision']) if any(row[i] for row in coefficients))
    cusp = [row[first] for row in coefficients]
    return (f'expected_genus := {g};\nR := PolynomialRing(Rationals(),{g});\n'
            + 'equations := [R |\n' + ',\n'.join(equations) + '\n];\n'
            + 'cusp_coordinates := [Rationals() | ' + ','.join(map(str, cusp)) + '];\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', default='canonical_input.m')
    args = parser.parse_args()
    Path(args.output).write_text(export(json.loads(Path(args.input).read_text())))


if __name__ == '__main__':
    main()
