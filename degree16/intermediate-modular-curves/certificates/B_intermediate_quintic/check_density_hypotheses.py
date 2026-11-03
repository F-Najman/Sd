"""Check the minimum-density hypothesis in every density-theorem assignment.

The source data below are independently transcribed from Derickx--Orlic,
arXiv:2504.15937v1, Theorems 1.4--1.6. Only the levels used by these
assignments are in scope. This is a source/application consistency check,
not an independent proof of the cited published classification.
"""
import hashlib
import json
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
INVENTORY = FOLDER.parent / 'complete_inventory.json'
SCOPE = {37,43,53,55,57,58,61,65,67,73,91,109,121,125}


def group(n, generators):
    # Independent elementary closure, without importing the production census.
    result = {1}
    while True:
        larger = result | {(a*b) % n for a in result for b in generators}
        if larger == result:
            return tuple(sorted(result))
        result = larger


# All quartic-positive entries in Theorem 1.6 at levels in SCOPE.
# Negative one is explicit even where the paper's generator already contains it.
QUARTIC = {
    (37,group(37,[-1,3,4,7,9,10,11,12,16])),
    (37,group(37,[-1,6,8,10,11,14])),
    (53,group(53,[-1,4])),
    (55,group(55,[-1,4])),
    (61,group(61,[-1,4])),
    (65,group(65,[-1,2,12**2])),
    (65,group(65,[-1,4,12])),
    (65,group(65,[-1,4,24])),
}
assert len(QUARTIC) == 8
METHODS = {'FINITE_BY_ELLIPTIC_DEGREE_AND_DENSITY',
           'FINITE_BY_NO_ELLIPTIC_FACTORS_AND_DENSITY',
           'FINITE_BY_DEBARRE_FAHLAOUI_OBSTRUCTION'}
data = json.loads(INVENTORY.read_text())
checked = []
for row in data['curves']:
    if row['quintic_status'] not in METHODS:
        continue
    assert row['strict'] and row['level'] in SCOPE
    # Degree one: Faltings. Degree two: Theorem 1.4 has only the level-21
    # genus-three exception. Degree three: Theorem 1.5 has no genus >=5 case.
    assert row['genus'] >= 9 and row['level'] != 21
    assert (row['level'],tuple(row['delta'])) not in QUARTIC
    if row['quintic_status'] != 'FINITE_BY_DEBARRE_FAHLAOUI_OBSTRUCTION':
        assert row['genus'] >= 12
    checked.append(row['id'])
assert len(checked) == 51
out = FOLDER / 'audit_runs' / 'density_hypotheses'
out.mkdir(parents=True,exist_ok=True)
receipt = dict(status='PUBLISHED_MINIMUM_DENSITY_HYPOTHESES_PASS',
               scope='All 51 density-theorem assignments; degrees one through four',
               source='https://arxiv.org/html/2504.15937v1, Theorems 1.4--1.6',
               ids=checked,
               inventory_sha256=hashlib.sha256(INVENTORY.read_bytes()).hexdigest(),
               script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['status'],len(checked))
