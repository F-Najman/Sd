"""Exact operations on full-rank rational lattices containing Z^r."""
from sage.all import ZZ


def dual(lattice):
    """Vectors pairing integrally with every lattice vector (row convention)."""
    return lattice.basis_matrix().inverse().transpose().row_module(ZZ)


def order(lattice):
    """Order of lattice/Z^r; the caller checks containment of Z^r."""
    value = 1/abs(lattice.basis_matrix().det())
    assert value.denominator() == 1
    return ZZ(value)
