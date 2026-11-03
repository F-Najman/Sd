"""Readable tables generated from the checked inventory, never search labels."""
from itertools import combinations
import json
from pathlib import Path
from enumeration import generated

ROOT = Path(__file__).resolve().parent


def generators(row):
    n,delta = row['level'],tuple(row['delta'])
    choices = sorted({min(a,n-a) for a in delta if a not in [1,n-1]})
    for size in range(len(choices)+1):
        for choice in combinations(choices,size):
            if generated(n,[-1,*choice])==delta:
                return '⟨'+', '.join(map(str,[-1,*choice]))+'⟩'
    raise AssertionError('subgroup generators not found')


def main():
    data = json.loads((ROOT/'complete_inventory.json').read_text())
    rows = data['curves']
    positives = [r for r in rows if r['strict'] and r['quintic_status'].startswith('INFINITE')]
    unresolved = [r for r in rows if r['quintic_status']=='UNRESOLVED']
    labels = {'INFINITE_BY_LOW_GENUS':'Riemann–Roch, genus ≤2',
              'INFINITE_BY_CANONICAL_LOW_GENUS':'Exact canonical low-genus check',
              'INFINITE_BY_NEW_EXACT_FUNCTION':'Verified degree-five function',
              'INFINITE_BY_PUBLISHED_GONALITY_5':'Published gonality-five theorem'}
    lines = ['# Intermediate modular curves: checked classification table','',
             '**Status: '+('incomplete' if unresolved else 'all listed cases classified')+'.**',
             f'There are {len(rows):,} subgroup-defined curves through level 191, '
             f'including the X0 and X1 endpoints. {len(unresolved)} entries remain unresolved.',
             'The all-level exclusion beyond 191 is recorded in [ENDPOINTS.md](ENDPOINTS.md).',
             'Rows distinguish subgroups, not Q-isomorphism classes of curves.','',
             '## Proved positive strict intermediate curves','',
             f'All {len(positives)} curves below have a function of exactly degree five over Q,',
             'hence infinitely many closed points of exactly degree five.',
             'Here Δ=⟨−1,a,…⟩ denotes the subgroup generated modulo N.','',
             '| N | Δ generators | Genus | Existence proof |',
             '|---:|---|---:|---|']
    for row in positives:
        lines.append(f"| {row['level']} | {generators(row)} | {row['genus']} | {labels[row['quintic_status']]} |")
    lines += ['','## Remaining cases','']
    if unresolved:
        lines += ['These are not included in either a positive or a negative classification.',
                  'No failed or unfinished search is being used as a nonexistence proof.','',
                  '| N | Δ generators | Genus | Degree-five function |',
                  '|---:|---|---:|---|']
        for row in unresolved:
            function = 'Excluded' if row['degree5_function']=='DOES_NOT_EXIST' else 'Unresolved'
            lines.append(f"| {row['level']} | {generators(row)} | {row['genus']} | {function} |")
    else:
        lines += ['None.']
    groups = {
        'Projection and gonality filters': {
            'FINITE_BY_PROJECTION','FINITE_BY_INTERMEDIATE_PROJECTION','FINITE_BY_GONALITY_ABOVE_10'},
        'Rank-zero Jacobian arguments': {
            'FINITE_BY_RANK_ZERO_AND_GONALITY','FINITE_BY_INTERMEDIATE_RANK_ZERO',
            'FINITE_BY_BIELLIPTIC_AND_RANK_ZERO','FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO',
            'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE'},
        'Positive-rank density and elliptic-family arguments': {
            'FINITE_BY_ELLIPTIC_DEGREE_AND_DENSITY','FINITE_BY_NO_ELLIPTIC_FACTORS_AND_DENSITY',
            'FINITE_BY_DEBARRE_FAHLAOUI_OBSTRUCTION','FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION',
            'FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES'},
        'Degree-five function constructions': set(labels),
        'Awaiting a complete certificate': {'UNRESOLVED'},
    }
    strict = [r for r in rows if r['strict']]
    assert all(sum(r['quintic_status'] in values for values in groups.values())==1 for r in strict)
    lines += ['','## Four groups of arguments cover the strict curves','',
              '| Argument | Number of curves |','|---|---:|']
    for label,values in groups.items():
        count = sum(r['quintic_status'] in values for r in strict)
        if count:
            lines.append(f'| {label} | {count} |')
    lines += ['','The proof structure is explained in [PROOF_OVERVIEW.md](PROOF_OVERVIEW.md).']
    lines += ['','## Endpoints and negative certificates','',
              'The X0 and X1 endpoints, including their source statements, are described',
              'in [ENDPOINTS.md](ENDPOINTS.md). Every other classified strict row is finite',
              'for degree-five points; the machine-readable inventory records its proof source.','',
              'The main new certificate explanations are:', '',
              '- [Canonical model identification](MODEL_IDENTIFICATION.md).',
              '- [Genus-three/four function existence](LOW_GENUS.md).',
              '- [Level-40 exhaustive rational class sieve](HECKE_TORSION40.md).',
              '- [Level-48 pullback torsion and exhaustive class sieves](PULLBACK_TORSION48.md).',
              '- [Rank-zero Petri lifting](PETRI_LIFTING_CERTIFICATE.md).',
              '- [Elliptic-family finiteness](ELLIPTIC_FAMILY_CERTIFICATE.md).',
              '- [Level-65 exact fiber construction](ELLIPTIC_FAMILY65_LINEAR.md).',
              '- [Elliptic map-degree exclusions](ELLIPTIC_DEGREE_EXCLUSIONS.md).','',
              'Regenerate after running `build_inventory.py` and `build_complete_inventory.py`:',
              '`python3 write_classification_report.py`.','']
    (ROOT/'CLASSIFICATION_TABLE.md').write_text('\n'.join(lines))
    print('SUCCESS readable classification table',len(positives),'positive strict curves;',
          len(unresolved),'unresolved')


if __name__=='__main__':
    main()
