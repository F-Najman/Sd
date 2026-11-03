"""Galois orbits of cusps on the point-marked X_Delta(N), using integers.

Primitive columns (x,y) modulo N are divided by the upper triangular
Gamma_Delta action. Galois sigma sends (x,y) to (sigma*x,y).
See Jeon--Kim--Schweizer, arXiv:1709.00510, Section 1 and Lemma 1.1.
This computes residue degrees, not cusp widths, and does not produce
coordinates on our separately constructed canonical mu-model.
"""
from collections import Counter
from math import gcd
from enumeration import generated, signature, units


def cusp_degrees(n, delta):
    delta = tuple(sorted(delta))
    assert generated(n,delta)==delta and (-1)%n in delta
    vectors = [(x,y) for x in range(n) for y in range(n) if gcd(gcd(x,y),n)==1]
    index = {v:i for i,v in enumerate(vectors)}
    parent = list(range(len(vectors)))

    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i

    def join(i,j):
        i,j=root(i),root(j)
        if i!=j:
            parent[max(i,j)]=min(i,j)

    for i,(x,y) in enumerate(vectors):
        join(i,index[((x+y)%n,y)])
        for a in delta:
            join(i,index[(a*x%n,pow(a,-1,n)*y%n)])
    representatives = {root(i):v for i,v in enumerate(vectors)}
    assert len(representatives)==signature(n,delta)['cusps']
    geometric_parent = [root(i) for i in range(len(vectors))]
    # Merge geometric cusps under all cyclotomic Galois automorphisms.
    for i,(x,y) in representatives.items():
        for a in units(n):
            join(i,geometric_parent[index[(a*x%n,y)]])
    orbit_sizes = Counter(root(i) for i in representatives)
    return sorted(orbit_sizes.values())


if __name__=='__main__':
    import json
    from pathlib import Path
    path = Path(__file__).resolve().parent/'classification_inventory.json'
    for row in json.loads(path.read_text())['curves']:
        if row['quintic_status']=='UNRESOLVED':
            print(row['id'],cusp_degrees(row['level'],row['delta']))
