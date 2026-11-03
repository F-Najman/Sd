"""Export newly computed exact relations for an independent Magma check."""
import json
import argparse
from fractions import Fraction
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', default='genus5_input.m')
    args = parser.parse_args()
    r = json.loads(Path(args.input).read_text())
    assert r['invariants']['genus'] == 5
    block = next(b for b in r['relation_blocks'] if b['degree'] == 2)
    assert block['product_rank'] == 12 and len(block['relations']) == 3
    equations = []
    for row in block['relations']:
        terms = []
        for c, indices in zip(row, block['monomials']):
            c = Fraction(c)
            if c:
                terms.append(f'({c})*'+'*'.join(f'R.{i+1}' for i in indices))
        equations.append('+'.join(terms))
    text = 'R := PolynomialRing(Rationals(),5);\n'
    text += 'equations := [\n'+',\n'.join(equations)+'\n];\n'
    Path(args.output).write_text(text)


if __name__ == '__main__':
    main()
