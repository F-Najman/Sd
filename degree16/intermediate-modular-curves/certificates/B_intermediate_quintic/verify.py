"""Check the presentation package using only standard Python and local files.

This verifies integrity, case assignments and completed replay records.
It does not replace the mathematical arguments or rerun Sage/Magma.
The saved-ledger audit runs in a temporary copy, preserving the package.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

FOLDER = Path(__file__).resolve().parent
REQUIRED = {
    'census':'FRESH_CENSUS_REPLAY_PASS',
    'rankzero':'FRESH_RANKZERO_REPLAY_PASS',
    'positive_batches':'FRESH_POSITIVE_BATCHES_PASS',
    'positive64':'FRESH_POSITIVE64_PASS',
    'special_models':'FRESH_ALL_12_SPECIAL_MODELS_PASS',
    'special':'FRESH_ALL_12_SPECIAL_CERTIFICATES_PASS',
    'arithmetic_inputs':'FRESH_ALL_6_ARITHMETIC_INPUTS_PASS',
    'density_hypotheses':'PUBLISHED_MINIMUM_DENSITY_HYPOTHESES_PASS',
    'x0':'FRESH_X0_ALL_36_PASS',
    'portable_special':'PORTABLE_ALL_12_SPECIAL_REPLAYS_PASS',
    'portable_positive':'PORTABLE_ALL_POSITIVE_BATCHES_PASS',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_files(base, entries):
    for relative, value in entries.items():
        path = (base/relative).resolve()
        assert path.is_relative_to(base.resolve()),('nonlocal manifest path',relative)
        assert path.is_file() and digest(path)==value,('file hash mismatch',relative)


def subgroup_id(level, tex):
    generators = [int(x) for x in re.findall(r'-?\d+',tex)]
    subgroup = {1}
    while True:
        enlarged = subgroup | {(a*b)%level for a in subgroup for b in generators}
        if enlarged==subgroup:
            return str(level)+':'+','.join(map(str,sorted(subgroup)))
        subgroup = enlarged


def check_typeset_tables(by_id):
    negative_codes = {
        'FINITE_BY_GONALITY_ABOVE_10':'S',
        'FINITE_BY_RANK_ZERO_AND_GONALITY':'Z',
        'FINITE_BY_INTERMEDIATE_RANK_ZERO':'Z',
        'FINITE_BY_BIELLIPTIC_AND_RANK_ZERO':'B',
        'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE':'R',
        'FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO':'T',
        'FINITE_BY_ELLIPTIC_DEGREE_AND_DENSITY':'E',
        'FINITE_BY_NO_ELLIPTIC_FACTORS_AND_DENSITY':'E0',
        'FINITE_BY_DEBARRE_FAHLAOUI_OBSTRUCTION':'D',
        'FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION':'C',
        'FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES':'F',
    }
    positive_codes = {'INFINITE_BY_LOW_GENUS':'L','INFINITE_BY_CANONICAL_LOW_GENUS':'C',
                      'INFINITE_BY_NEW_EXACT_FUNCTION':'W','INFINITE_BY_PUBLISHED_GONALITY_5':'P'}
    for filename,codes in [('positive_table.tex',positive_codes),('negative_table.tex',negative_codes)]:
        found = set()
        for line in (FOLDER/filename).read_text().splitlines():
            if not re.match(r'^\d+ &',line):
                continue
            parts = [s.strip().rstrip('\\').strip() for s in line.split('&')]
            identifier = subgroup_id(int(parts[0]),parts[1])
            assert identifier not in found,('duplicate typeset row',identifier)
            found.add(identifier)
            row = by_id[identifier]
            assert row['strict'] and int(parts[2])==row['genus']
            assert parts[-1]==codes[row['quintic_status']]
            if filename=='negative_table.tex':
                assert int(parts[3])==row['index']
        assert found=={r['id'] for r in by_id.values() if r['strict'] and r['quintic_status'] in codes}
    projected = {}
    for line in (FOLDER/'projection_table.tex').read_text().splitlines():
        if re.match(r'^\d+ &',line):
            parts = line.split('&')
            projected[subgroup_id(int(parts[0]),parts[1])] = subgroup_id(int(parts[2]),parts[3])
    assert projected=={r['id']:r['projection_target'] for r in by_id.values()
                       if r['strict'] and r['quintic_status']=='FINITE_BY_INTERMEDIATE_PROJECTION'}


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O or PYTHONOPTIMIZE: verification requires assertions')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--development',action='store_true',
                        help='Permit an unsealed draft; missing replay records still fail')
    args = parser.parse_args()
    seal = FOLDER/'PACKAGE_MANIFEST.json'
    if seal.exists():
        check_files(FOLDER,json.loads(seal.read_text())['files'])
    elif not args.development:
        raise SystemExit('INCOMPLETE: final package manifest has not been sealed')
    bundle = FOLDER/'reproduction'
    check_files(bundle,json.loads((bundle/'manifest.json').read_text())['files'])
    expected = json.loads((bundle/'machinery'/'complete_inventory.json').read_text())
    assert len(expected['curves'])==1388 and not expected['unresolved']
    by_id = {r['id']:r for r in expected['curves']}
    with (FOLDER/'all_cases.csv').open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows)==1388 and {r['id'] for r in rows}==set(by_id)
    for row in rows:
        model = by_id[row['id']]
        assert [int(x) for x in row['Delta_full'].split()]==model['delta']
        assert int(row['N'])==model['level'] and int(row['genus'])==model['genus']
        assert row['quintic_status']==model['quintic_status']
        assert row['projection_target']==model.get('projection_target','')
        assert row['source']==model.get('source','')
    for name,count in [('positive_table.tex',43),('negative_table.tex',154),
                       ('special_table.tex',12),('projection_table.tex',7)]:
        assert len(re.findall(r'^\d+ &', (FOLDER/name).read_text(),re.M))==count,name
    check_typeset_tables(by_id)
    # Recompute the accepted classifications without modifying distributed files.
    with tempfile.TemporaryDirectory(prefix='quintic-verify-') as temporary:
        work = Path(temporary)/'machinery'
        shutil.copytree(bundle/'machinery',work)
        result = subprocess.run([sys.executable,str(work/'audit_results.py'),'--require-complete'],
                                cwd=work,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),
                                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        assert result.returncode==0,result.stdout
        assert (work/'complete_inventory.json').read_bytes()==(bundle/'machinery'/'complete_inventory.json').read_bytes()
    missing = []
    for name,status in REQUIRED.items():
        path = FOLDER/'audit_runs'/name/'receipt.json'
        if not path.exists():
            missing.append(name)
            continue
        receipt = json.loads(path.read_text())
        assert receipt['status']==status,(name,receipt['status'])
        for key,value in receipt.get('receipts',{}).items():
            assert digest(path.parent/key/'receipt.json')==value,(name,key)
    if missing:
        print('INCOMPLETE: pending replay receipts:',', '.join(missing))
        return 2
    print('PASS: package integrity, 1388 case assignments, and all required replay records')
    print('Scope: computational evidence checks; mathematical deductions are in the proof.')
    return 0


if __name__=='__main__':
    sys.exit(main())
