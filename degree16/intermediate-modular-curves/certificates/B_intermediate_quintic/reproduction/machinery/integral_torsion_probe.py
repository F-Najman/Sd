"""Exploratory full-GammaH homology bounds, with prime exclusions explicit.

No characterwise lattice is used. No classification imports this output:
identification with integral Jacobian homology remains a separate audit gate.
Run with Sage's Python and a model directory containing relations.json.
"""
import argparse
import json
from pathlib import Path
from sage.all import GammaH, ModularSymbols, QQ, ZZ, Matrix, identity_matrix

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('directory',type=Path)
args = parser.parse_args()
data = json.loads((args.directory/'relations.json').read_text())['invariants']
n, g = data['level'], data['genus']
M = ModularSymbols(GammaH(n,data['delta']),2,sign=0).cuspidal_subspace()
assert M.dimension() == 2*g
embedding = M.basis_matrix()
lattice = M.integral_structure().basis_matrix().change_ring(QQ)
B = embedding.solve_left(lattice)
assert B*embedding == lattice and B.rank() == 2*g
I = identity_matrix(QQ,2*g)


def integral_action(T):
    A = B*T*B.inverse()
    assert all(c.denominator() == 1 for c in A.list())
    return A.change_ring(ZZ)


star = integral_action(M.star_involution().matrix())
assert star*star == I and (star-I).rank() == g
primes = [p for p in [3,5,7,11,13] if n % p]
operators = {}
for p in primes:
    T = M.hecke_matrix(p)
    operators[p] = integral_action(I-T+T*T-M.hecke_matrix(p*p))
    print('integral Eichler-Shimura operator',p,flush=True)
results = []
# Only use a prime-p reduction constraint on prime-to-p torsion. Separate
# exclusion runs prevent inadvertently imposing it on p-primary torsion.
for omitted in [0]+primes:
    relations = (star-I).change_ring(ZZ).transpose()
    for p,A in operators.items():
        if p != omitted:
            relations = relations.stack(A.transpose())
    assert relations.rank() == 2*g
    invariants = [int(a) for a in relations.elementary_divisors() if a != 0]
    result = dict(omit_residue_prime=omitted,smith=invariants)
    results.append(result)
    print(result,flush=True)
(args.directory/'integral_torsion_probe.json').write_text(json.dumps(dict(
    status='EXPLORATORY_PENDING_LATTICE_AUDIT',level=n,delta=data['delta'],
    results=results),indent=2)+'\n')
