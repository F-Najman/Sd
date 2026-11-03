"""Explicit theorem inputs, freshly transcribed from the primary paper.

Orlic, arXiv:2407.14512v1, Theorems 1.3–1.5.
https://arxiv.org/html/2407.14512v1
Full subgroup elements are constructed locally, never copied from a database.
"""
from enumeration import generated

TETRAGONAL_GENERATORS = [
    (25,[-1,7]), (30,[-1,11]), (32,[-1,15]), (33,[-1,2]),
    (34,[-1,9,13,15]), (35,[-1,6,8,13]), (35,[-1,4,6]),
    (36,[-1,17]), (39,[-1,5,8,14]), (39,[-1,4]),
    (40,[-1,3,9,13]), (40,[-1,7,9,17]), (40,[-1,9,11,19]),
    (41,[-1,2]), (45,[-1,4]), (48,[-1,5,19,23]),
    (48,[-1,7,17,23]), (48,[-1,11,13,23]),
    (55,[-1,4]), (64,[-1,9]), (75,[-1,4]),
]
TETRAGONAL = {(n,generated(n,g)) for n,g in TETRAGONAL_GENERATORS}
assert len(TETRAGONAL) == 21
PENTAGONAL = {(31,generated(31,[-1,5,6])),
              (31,generated(31,[-1,2,4,8,15])),
              (44,generated(44,[-1,5,7,9,19])),
              (125,generated(125,[-1,4]))}


def at_least_six(row):
    # The hyperelliptic/trigonal classifications cited and summarized in
    # Orlic Section 1 imply none of the strict curves of genus >=5 has
    # gonality <=3. We deliberately do not apply this to lower genus.
    key = (row['level'],tuple(row['delta']))
    return row['strict'] and row['genus'] >= 5 and key not in TETRAGONAL | PENTAGONAL
