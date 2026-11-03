"""Fresh cuspidal torsion/Galois lattice experiment using full Manin symbols.

This is not imported by the classification ledger. Analytic Abel--Jacobi
identification and the Galois formula are explicit proof-audit obligations.
All lattice calculations below are exact; no modular-unit database is used.
"""
import argparse
import json
from itertools import product
from math import gcd
from pathlib import Path
from sage.all import (Cusp, GF, GammaH, Matrix, ModularSymbols, QQ, ZZ,
                      identity_matrix, lcm, zero_matrix)


def dual(lattice):
    return lattice.basis_matrix().inverse().transpose().row_module(ZZ)


def order(lattice):
    value = 1/abs(lattice.basis_matrix().det())
    assert value.denominator() == 1
    return ZZ(value)


def experiment(directory,torsion_bound):
    data = json.loads((directory/'relations.json').read_text())['invariants']
    n,g = data['level'],data['genus']
    A = ModularSymbols(GammaH(n,data['delta']),2,sign=0)
    M = A.cuspidal_subspace()
    h = 2*g
    assert M.dimension() == h
    integral_relative = A.manin_gens_to_basis().row_module(ZZ)
    assert integral_relative == A.integral_structure()
    assert integral_relative.intersection(A.boundary_map().matrix().left_kernel()) == M.integral_structure()
    integral = M.integral_structure().basis_matrix().change_ring(QQ)
    change = M.basis_matrix().solve_left(integral)
    assert change*M.basis_matrix() == integral
    split = integral.stack(A.eisenstein_subspace().basis_matrix())
    assert split.is_square() and split.det() != 0
    cusps = list(A.cusps())
    boundary = A.boundary_space()
    assert len(cusps) == data['cusps']
    units = [a for a in range(n) if gcd(a,n)==1]
    permutations = {}
    for a in units:
        permutation = []
        for cusp in cusps:
            y = ZZ(cusp.denominator())
            if y == 0:
                y = ZZ(n)
            x = ZZ(a*cusp.numerator()) % n
            while gcd(x,y) != 1:
                x += n
            j,sign = boundary._cusp_index(Cusp(x,y))
            assert j >= 0 and sign in [-1,1]
            permutation.append(j)
        assert sorted(permutation) == list(range(len(cusps)))
        permutations[a] = permutation
    for a in units:
        for b in units:
            assert [permutations[a][j] for j in permutations[b]] == permutations[a*b % n]
    base = next(i for i in range(len(cusps)) if all(p[i]==i for p in permutations.values()))
    vectors = []
    for cusp in cusps:
        path = A([cusps[base],cusp]).element()
        assert path in integral_relative
        coordinates = split.solve_left(path)
        assert coordinates*split == path
        vectors.append(list(coordinates[:h]))
    V = Matrix(QQ,vectors)
    I = identity_matrix(QQ,h)
    generators = I.stack(V)
    C = generators.row_module(ZZ)
    denominator = lcm(c.denominator() for c in generators.list())
    H,U = (denominator*generators).change_ring(ZZ).hermite_form(
        transformation=True,include_zero_rows=True)
    assert U*(denominator*generators) == H
    nonzero = [i for i,row in enumerate(H.rows()) if row]
    CB = H.matrix_from_rows(nonzero).change_ring(QQ)/denominator
    assert CB.nrows() == h and CB.row_module(ZZ) == C
    lifts = U.matrix_from_rows(nonzero)
    constraints = I
    star = change*M.star_involution().matrix()*change.inverse()
    assert all(c.denominator()==1 for c in star.list())
    for a,permutation in permutations.items():
        image = Matrix(QQ,[V.row(j)-V.row(permutation[base]) for j in permutation])
        image_basis = lifts*(zero_matrix(QQ,h,h).stack(image))
        assert all(row in C for row in image_basis.rows())
        # The lifted action must send the integral period lattice to itself.
        assert all(c.denominator()==1 for c in (CB.inverse()*image_basis).list())
        constraints = constraints.stack((image_basis-CB).transpose())
        if a == n-1:
            assert all(c.denominator()==1 for c in (V*star-image).list())
    fixed = (dual(constraints.row_module(ZZ)).basis_matrix()*CB).row_module(ZZ)
    assert I.row_module(ZZ).is_submodule(fixed) and fixed.is_submodule(C)
    unseen = set(range(len(cusps)))
    rational_generators = I
    orbit_degrees = []
    while unseen:
        i = min(unseen)
        orbit = {p[i] for p in permutations.values()}
        unseen -= orbit
        orbit_degrees.append(len(orbit))
        rational_generators = rational_generators.stack(Matrix(QQ,[sum((V.row(j) for j in orbit),V.row(base))]))
    rational = rational_generators.row_module(ZZ)
    assert rational.is_submodule(fixed)
    print('cusps',len(cusps),'orbit_degrees',sorted(orbit_degrees),flush=True)
    print('geometric_cuspidal_order',order(C),'Galois_fixed_order',order(fixed),
          'rational_cusp_divisor_order',order(rational),flush=True)
    relations = (star-I).transpose().stack(torsion_bound*I)
    primes = [p for p in [7,11,13,17,19] if gcd(p,n*torsion_bound)==1]
    for p in primes:
        T = M.hecke_matrix(p)
        operator = change*(I-T+T*T-M.hecke_matrix(p*p))*change.inverse()
        assert all(c.denominator()==1 for c in operator.list())
        relations = relations.stack(operator.transpose())
    hecke = dual(relations.row_module(ZZ))
    assert fixed.is_submodule(hecke)
    intersection = hecke.intersection(C)
    quotient_order = order(hecke)//order(fixed)
    socle_tests = {}
    diamond_socle_tests = {}
    bad_hecke_socle_tests = {}
    for ell in quotient_order.prime_divisors():
        socle = hecke.intersection(fixed.scale(QQ(1)/ell))
        socle_tests[int(ell)] = socle.is_submodule(intersection)
        # A nonzero module in characteristic ell for an ell-group has a
        # nonzero invariant vector. This strengthens the plain Z-socle test.
        diamond_order = ZZ(len(units)//len(data['delta']))
        if diamond_order.is_power_of(ell):
            invariant_socle = socle
            for d in units:
                diamond = change*M.diamond_bracket_matrix(d)*change.inverse()
                assert all(c.denominator()==1 for c in diamond.list())
                assert all(row in fixed for row in (fixed.basis_matrix()*diamond).rows())
                SB = invariant_socle.basis_matrix()
                congruences = I.stack((SB*(diamond-I)*fixed.basis_matrix().inverse()).transpose())
                invariant_socle = (dual(congruences.row_module(ZZ)).basis_matrix()*SB).row_module(ZZ)
            diamond_socle_tests[int(ell)] = invariant_socle.is_submodule(intersection)
            bad_operators = []
            spectra = []
            for q in ZZ(n).prime_divisors():
                operator = change*M.hecke_matrix(q)*change.inverse()
                assert all(c.denominator()==1 for c in operator.list())
                assert all(row in fixed for row in (fixed.basis_matrix()*operator).rows())
                polynomial = operator.change_ring(GF(ell)).charpoly()
                assert all(f.degree()==1 for f,e in polynomial.factor())
                spectra.append([int(a) for a in polynomial.roots(multiplicities=False)])
                bad_operators.append(operator)
            character_tests = []
            for eigenvalues in product(*spectra):
                simultaneous = invariant_socle
                for operator,eigenvalue in zip(bad_operators,eigenvalues):
                    SB = simultaneous.basis_matrix()
                    congruences = I.stack((SB*(operator-eigenvalue*I)*fixed.basis_matrix().inverse()).transpose())
                    simultaneous = (dual(congruences.row_module(ZZ)).basis_matrix()*SB).row_module(ZZ)
                character_tests.append(dict(eigenvalues=list(eigenvalues),
                    contained=simultaneous.is_submodule(intersection),order=int(order(simultaneous))))
            bad_hecke_socle_tests[int(ell)] = character_tests
    result = dict(status='EXPLORATORY_PENDING_ANALYTIC_AND_GALOIS_AUDIT',
                  level=n,delta=data['delta'],geometric_cuspidal_order=int(order(C)),
                  galois_fixed_order=int(order(fixed)),rational_cusp_divisor_order=int(order(rational)),
                  hecke_order=int(order(hecke)),hecke_cuspidal_intersection_order=int(order(intersection)),
                  quotient_socle_contained=socle_tests,
                  diamond_invariant_socle_contained=diamond_socle_tests,
                  bad_hecke_joint_socle_tests=bad_hecke_socle_tests)
    print(result,flush=True)
    (directory/'cuspidal_torsion_lattice.json').write_text(json.dumps(result,indent=2)+'\n')
    return A,M,integral,change,fixed,hecke


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--torsion-bound',type=int,required=True)
    args = parser.parse_args()
    experiment(args.directory,args.torsion_bound)
