"""Exact Gamma_Delta enumeration and signatures, using only Python integers.

No external curve tables or home-directory code are imported.
See AUDIT.md for the coset construction and completeness arguments.
"""
from fractions import Fraction
from math import gcd


def units(n):
    if n < 1:
        raise ValueError("level must be positive")
    return tuple(a for a in range(n) if gcd(a, n) == 1)


def generated(n, generators):
    """Multiplicative subgroup; the level-one identity is residue zero."""
    generators = tuple(a % n for a in generators)
    if any(gcd(a, n) != 1 for a in generators):
        raise ValueError("generators must be units")
    group = {1 % n}
    pending = list(group)
    while pending:
        a = pending.pop()
        for b in generators:
            c = a*b % n
            if c not in group:
                group.add(c)
                pending.append(c)
    return tuple(sorted(group))


def subgroups(n):
    """All subgroups containing -1, ordered from X0 toward X1."""
    ambient = units(n)
    initial = generated(n, [-1])
    seen = {initial}
    pending = [initial]
    while pending:
        group = pending.pop()
        for a in ambient:
            if a not in group:
                larger = generated(n, (*group, a))
                if larger not in seen:
                    seen.add(larger)
                    pending.append(larger)
    return sorted(seen, key=lambda h: (-len(h), h))


def cycles(permutation):
    assert sorted(permutation) == list(range(len(permutation)))
    unseen = set(range(len(permutation)))
    result = []
    while unseen:
        start = min(unseen)
        cycle = []
        i = start
        while i in unseen:
            unseen.remove(i)
            cycle.append(i)
            i = permutation[i]
        assert i == start
        result.append(cycle)
    return result


def signature(n, delta):
    """Signature from the right S,T action on primitive bottom rows / Delta.

    Cusp widths here are geometric widths, NOT arithmetic residue degrees.
    """
    delta = tuple(sorted(delta))
    if generated(n, delta) != delta or (-1) % n not in delta:
        raise ValueError("Delta must be a subgroup containing -1")
    lookup = {}
    representatives = []
    for c in range(n):
        for d in range(n):
            if gcd(gcd(c, d), n) != 1 or (c, d) in lookup:
                continue
            orbit = {(a*c % n, a*d % n) for a in delta}
            assert len(orbit) == len(delta)
            index = len(representatives)
            representatives.append((c, d))
            for pair in orbit:
                assert pair not in lookup
                lookup[pair] = index
    size = len(representatives)
    s = [lookup[d % n, -c % n] for c, d in representatives]
    t = [lookup[c, (c+d) % n] for c, d in representatives]
    st = [t[s[i]] for i in range(size)]
    assert all(s[s[i]] == i for i in range(size))
    assert all(st[st[st[i]]] == i for i in range(size))
    # Transitivity is an independent sanity check on the coset action.
    reached = {0}
    pending = [0]
    while pending:
        i = pending.pop()
        for j in (s[i], t[i]):
            if j not in reached:
                reached.add(j)
                pending.append(j)
    assert len(reached) == size
    widths = sorted(map(len, cycles(t)))
    e2 = sum(i == s[i] for i in range(size))
    e3 = sum(i == st[i] for i in range(size))
    genus = 1+Fraction(size, 12)-Fraction(e2, 4)-Fraction(e3, 3)-Fraction(len(widths), 2)
    assert genus.denominator == 1 and genus >= 0
    # Count primitive pairs independently by the product formula.
    primitive = n*n
    remainder = n
    q = 2
    while q*q <= remainder:
        if remainder % q == 0:
            primitive = primitive//(q*q)*(q*q-1)
            while remainder % q == 0:
                remainder //= q
        q += 1
    if remainder > 1:
        primitive = primitive//(remainder*remainder)*(remainder*remainder-1)
    assert size*len(delta) == primitive
    return dict(level=n, delta=list(delta), index=size, genus=int(genus),
                elliptic2=e2, elliptic3=e3, cusps=len(widths),
                cusp_widths=widths, degree_to_x0=len(units(n))//len(delta),
                strict=len(generated(n, [-1])) < len(delta) < len(units(n)))
