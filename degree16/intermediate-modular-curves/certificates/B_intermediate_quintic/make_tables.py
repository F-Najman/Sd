"""Typeset the checked classification without transcribing subgroup lists.

This exports data; it does not independently prove the classification.
The CSV retains the full subgroup and exact source for every case.
"""
import csv
import json
from pathlib import Path
import sys

folder = Path(__file__).resolve().parent
root = folder/'reproduction'/'machinery'
if not root.exists():
    root = folder.parent  # Development before the portable bundle is built.
sys.path.insert(0,str(root))
from write_classification_report import generators

data = json.loads((root/'complete_inventory.json').read_text())
assert not data['unresolved']
rows = data['curves']
positive = [r for r in rows if r['strict'] and r['quintic_status'].startswith('INFINITE')]
assert len(positive) == 43
codes = {'INFINITE_BY_LOW_GENUS':'L', 'INFINITE_BY_CANONICAL_LOW_GENUS':'C',
         'INFINITE_BY_NEW_EXACT_FUNCTION':'W', 'INFINITE_BY_PUBLISHED_GONALITY_5':'P'}
out = [r'\begin{longtable}{rrrl}',r'\caption{Positive strict intermediate pairs.}\label{tab:positive}\\',r'\toprule',
       r'$N$ & Generators of $\Delta$ & $g$ & Proof \\',r'\midrule\endfirsthead',
       r'\toprule $N$ & Generators of $\Delta$ & $g$ & Proof \\',r'\midrule\endhead']
for row in positive:
    gen = generators(row).replace('⟨',r'\langle ').replace('⟩',r'\rangle')
    out.append(f"{row['level']} & ${gen}$ & {row['genus']} & {codes[row['quintic_status']]} \\\\")
out += [r'\bottomrule',r'\end{longtable}']
(folder/'positive_table.tex').write_text('\n'.join(out)+'\n')
with (folder/'all_cases.csv').open('w',newline='') as stream:
    writer = csv.writer(stream,lineterminator='\n')
    writer.writerow(['id','N','Delta_full','genus','kind','degree5_function','quintic_status','source',
                     'projection_target','proof_metadata_json'])
    for r in rows:
        writer.writerow([r['id'],r['level'],' '.join(map(str,r['delta'])),r['genus'],r['kind'],
                         r.get('degree5_function',''),r['quintic_status'],r.get('source',''),
                         r.get('projection_target',''),json.dumps({k:v for k,v in r.items()
                             if k not in {'level','delta','index','genus','elliptic2','elliptic3',
                                          'cusps','cusp_widths','degree_to_x0','strict','id','kind'}},
                             sort_keys=True)])
print('Exported 43 positive strict pairs and all 1388 proof assignments.')

# The delicate finite-field arguments must be identified by subgroup, not
# merely by level: there are several distinct curves at levels 48 and 65.
special_methods = {
    'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE': 'Rational classes',
    'FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO': 'Petri lifting',
    'FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION': 'Empty cosets',
    'FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES': 'Elliptic families',
}
special = [r for r in rows if r['strict'] and r['quintic_status'] in special_methods]
assert len(special) == 12
out = [r'\begin{table}[!ht]',r'\centering',
       r'\caption{The twelve exceptional negative certificates.}\label{tab:special}',
       r'\begin{tabular}{rrrl}',
       r'\toprule $N$ & Generators of $\Delta$ & $g$ & Method \\',r'\midrule']
for row in special:
    gen = generators(row).replace('⟨', r'\langle ').replace('⟩', r'\rangle')
    out.append(f"{row['level']} & ${gen}$ & {row['genus']} & "
               + special_methods[row['quintic_status']] + r' \\')
out += [r'\bottomrule', r'\end{tabular}',r'\end{table}']
(folder/'special_table.tex').write_text('\n'.join(out)+'\n')

negative_codes = {
    'FINITE_BY_GONALITY_ABOVE_10': 'S',
    'FINITE_BY_RANK_ZERO_AND_GONALITY': 'Z',
    'FINITE_BY_INTERMEDIATE_RANK_ZERO': 'Z',
    'FINITE_BY_BIELLIPTIC_AND_RANK_ZERO': 'B',
    'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE': 'R',
    'FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO': 'T',
    'FINITE_BY_ELLIPTIC_DEGREE_AND_DENSITY': 'E',
    'FINITE_BY_NO_ELLIPTIC_FACTORS_AND_DENSITY': 'E0',
    'FINITE_BY_DEBARRE_FAHLAOUI_OBSTRUCTION': 'D',
    'FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION': 'C',
    'FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES': 'F',
}
direct = [r for r in rows if r['strict'] and r['quintic_status'] in negative_codes]
assert len(direct) == 154
out = [r'\begin{longtable}{rrrrl}',
       r'\caption{All direct negative assignments (excluding projection).}\label{tab:negative}\\',
       r'\toprule $N$ & Generators of $\Delta$ & $g$ & $\mu$ & Proof \\',
       r'\midrule\endfirsthead',
       r'\toprule $N$ & Generators of $\Delta$ & $g$ & $\mu$ & Proof \\',
       r'\midrule\endhead']
for row in direct:
    gen = generators(row).replace('⟨', r'\langle ').replace('⟩', r'\rangle')
    out.append(f"{row['level']} & ${gen}$ & {row['genus']} & {row['index']} & "
               + negative_codes[row['quintic_status']] + r' \\')
out += [r'\bottomrule',r'\end{longtable}']
(folder/'negative_table.tex').write_text('\n'.join(out)+'\n')

by_id = {r['id']:r for r in rows}
projections = [r for r in rows if r['strict'] and
               r['quintic_status']=='FINITE_BY_INTERMEDIATE_PROJECTION']
assert len(projections) == 7
out = [r'\begin{tabular}{rlrl}',
       r'\toprule $N$ & Source generators & $M$ & Target generators \\',r'\midrule']
for row in projections:
    target = by_id[row['projection_target']]
    assert row['level'] % target['level'] == 0 and target['genus'] > 1
    assert {a % target['level'] for a in row['delta']} <= set(target['delta'])
    assert target['quintic_status'].startswith('FINITE')
    source_gen = generators(row).replace('⟨',r'\langle ').replace('⟩',r'\rangle')
    target_gen = generators(target).replace('⟨',r'\langle ').replace('⟩',r'\rangle')
    out.append(f"{row['level']} & ${source_gen}$ & {target['level']} & ${target_gen}$" + r' \\')
out += [r'\bottomrule',r'\end{tabular}']
(folder/'projection_table.tex').write_text('\n'.join(out)+'\n')
