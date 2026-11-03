"""Eichler-Shimura/real-structure bound using genuine GammaH Manin symbols.

This bypasses the JH character-sum constructor. Run with Sage's Python.
Integral-lattice and complex-conjugation conventions are an explicit audit
gate; no classification status is changed by this exploratory calculation.
"""
import json
from pathlib import Path
from sage.all import GammaH, ModularSymbols, QQ, ZZ, Matrix, identity_matrix

delta = [1,7,9,15,17,23,25,31,33,39,41,47,49,55,57,63]
M = ModularSymbols(GammaH(64,delta),2,sign=0).cuspidal_subspace()
assert M.dimension() == 10
embedding = M.basis_matrix()
lattice = M.integral_structure().basis_matrix().change_ring(QQ)
B = embedding.solve_left(lattice)
assert B*embedding == lattice and B.rank() == 10
I = identity_matrix(QQ,10)


def integral_action(T):
    A = B*T*B.inverse()
    assert all(c.denominator() == 1 for c in A.list())
    return A.change_ring(ZZ)


star = integral_action(M.star_involution().matrix())
assert star*star == I and (star-I).rank() == 5
relations = (star-I).change_ring(ZZ).transpose()
results = []
for p in [3,5,7,11,13]:
    T = M.hecke_matrix(p)
    U = M.hecke_matrix(p*p)
    A = integral_action(I-T+T*T-U)
    relations = relations.stack(A.transpose())
    assert relations.rank() == 10
    # Sage includes zero entries for surplus rows of a rectangular matrix.
    diagonal = [a for a in relations.elementary_divisors() if a != 0]
    assert len(diagonal) == 10 and all(a != 0 for a in diagonal)
    invariants = [int(a) for a in diagonal]
    bound = 2**sum(ZZ(a).valuation(2) for a in invariants)
    result = dict(p=p,smith=invariants,two_primary_order_bound=int(bound))
    results.append(result)
    print(result,flush=True)
Path('integral_torsion64.json').write_text(json.dumps(dict(
    status='EXPLORATORY_PENDING_LATTICE_AUDIT',results=results),indent=2)+'\n')
print('SUCCESS GammaH integral-symbol calculation; audit gate remains')
