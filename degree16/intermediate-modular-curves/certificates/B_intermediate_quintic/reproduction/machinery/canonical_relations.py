"""Construct exact canonical relations from weight-two cusp forms.

This certifies relations, NOT yet that their zero locus is the modular curve.
The rational convention is justified in RATIONAL_MODELS.md; geometric model
identification remains a separate mandatory gate.
Run in Sage's Python: canonical_relations.py 33 --generators 32 2
"""
import argparse
import hashlib
import json
from itertools import combinations_with_replacement
from pathlib import Path
from sage.all import CuspForms, GammaH, Matrix, QQ
from enumeration import generated, signature


def construct(n, generators, maximum_degree=3):
    delta = generated(n, [-1, *generators])
    invariants = signature(n, delta)
    gamma = GammaH(n, list(delta))
    space = CuspForms(gamma, 2, base_ring=QQ)
    g = invariants['genus']
    assert space.dimension() == g
    if g < 3:
        raise ValueError('canonical relations require genus >= 3; use a separate low-genus model')
    # Weight 2*d products: vanishing through floor(2*d*index/12)
    # implies identical zero by the Sturm/valence bound. Include coefficient
    # at that bound, and compute extra terms as a separate precision check.
    bound = (2*maximum_degree*invariants['index'])//12
    precision = bound+12
    basis = list(space.q_expansion_basis(precision))
    assert len(basis) == g and all(f[0] == 0 for f in basis)
    assert Matrix(QQ, [[f[i] for i in range(precision)] for f in basis]).rank() == g
    blocks = []
    for degree in range(2, maximum_degree+1):
        monomials = list(combinations_with_replacement(range(g), degree))
        series = []
        for monomial in monomials:
            product = basis[monomial[0]]
            for j in monomial[1:]:
                product *= basis[j]
            series.append(product)
        cutoff = (2*degree*invariants['index'])//12
        matrix = Matrix(QQ, [[f[i] for i in range(cutoff+1)] for f in series])
        kernel = matrix.left_kernel().basis_matrix()
        extra = Matrix(QQ, [[f[i] for i in range(precision)] for f in series])
        assert kernel*extra == 0
        assert extra.rank() == matrix.rank()
        blocks.append(dict(degree=degree, sturm_bound=cutoff,
                           monomials=[list(m) for m in monomials],
                           product_rank=int(matrix.rank()),
                           relations=[[str(c) for c in row] for row in kernel.rows()]))
    return dict(invariants=invariants, precision=precision,
                basis_coefficients=[[str(f[i]) for i in range(precision)] for f in basis],
                relation_blocks=blocks, relation_status='EXACT_RELATIONS',
                model_status='UNVERIFIED', rational_descent_status='MU_MODEL_DUALITY',
                rational_descent_reference='RATIONAL_MODELS.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('level', type=int)
    parser.add_argument('--generators', nargs='*', type=int, default=[])
    parser.add_argument('--maximum-degree', type=int, default=3)
    parser.add_argument('--output', default='relations.json')
    args = parser.parse_args()
    if args.maximum_degree < 2:
        parser.error('maximum degree must be at least two')
    result = construct(args.level, args.generators, args.maximum_degree)
    result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('SUCCESS exact relations:', result['invariants'], flush=True)
    print('Rational convention: mu-model duality. Geometric model check still required.')


if __name__ == '__main__':
    main()
