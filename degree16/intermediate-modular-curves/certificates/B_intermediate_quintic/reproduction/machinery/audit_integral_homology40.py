"""Audit the full Manin lattice used for the level-40 Hecke torsion bound.

Uses all integral Manin generators, then the kernel of the cusp boundary;
it does not use a direct sum of character lattices. See HECKE_TORSION40.md.
"""
from sage.all import GammaH, ModularSymbols, QQ, ZZ

delta = [1,3,9,13,27,31,37,39]
A = ModularSymbols(GammaH(40,delta),2,sign=0)
M = A.cuspidal_subspace()
assert A.group().genus() == 7
assert A.group().nu2() == 0 and A.group().nu3() == 0
generators = A.manin_gens_to_basis()
integral = generators.row_module(ZZ)
assert integral == A.integral_structure()
boundary = A.boundary_map().matrix()
cuspidal = boundary.left_kernel()
assert cuspidal == M.free_module()
lattice = integral.intersection(cuspidal)
assert lattice == M.integral_structure() and lattice.rank() == 14
print('SUCCESS full integral Manin lattice and exact cusp-boundary kernel')
