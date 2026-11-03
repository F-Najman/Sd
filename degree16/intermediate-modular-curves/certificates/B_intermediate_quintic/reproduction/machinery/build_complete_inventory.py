"""Merge the audited strict ledger and independently sourced endpoints.

This does not declare the global goal complete: unresolved strict cases
remain visible, and the report explicitly labels that incompleteness.
"""
import hashlib
import json
from pathlib import Path
from build_inventory import X0_POSITIVE
from enumeration import units

ROOT = Path(__file__).resolve().parent
X1_POSITIVE = set(range(1,26))-{23}


def main():
    census_path = ROOT/'enumeration_audit_191.json'
    strict_path = ROOT/'classification_inventory.json'
    census = json.loads(census_path.read_text())
    strict = json.loads(strict_path.read_text())
    assert census['status']=='PASS' and census['max_level']==191
    assert strict['census_sha256']==hashlib.sha256(census_path.read_bytes()).hexdigest()
    by_id = {r['id']:r for r in strict['curves']}
    rows = []
    for curve in census['curves']:
        n = curve['level']
        identifier = f'{n}:'+','.join(map(str,curve['delta']))
        if curve['strict']:
            rows.append(dict(by_id[identifier],kind='STRICT'))
            continue
        is_x0 = tuple(curve['delta'])==units(n)
        is_x1 = set(curve['delta'])=={1%n,(-1)%n}
        assert is_x0 or is_x1
        answers = ([n in X0_POSITIVE] if is_x0 else [])+([n in X1_POSITIVE] if is_x1 else [])
        assert len(set(answers))==1
        positive = answers[0]
        kind = 'X0_AND_X1' if is_x0 and is_x1 else ('X0' if is_x0 else 'X1')
        row = dict(curve,id=identifier,kind=kind,
                   quintic_status=('INFINITE' if positive else 'FINITE')+'_BY_ENDPOINT_CLASSIFICATION',
                   source='ENDPOINTS.md',degree5_function='NOT_IMPORTED')
        if not positive:
            row['degree5_function']='DOES_NOT_EXIST'
        elif is_x1:
            row['degree5_function']='EXISTS_BY_PUBLISHED_THEOREM'
        rows.append(row)
    assert len(rows)==1388 and len({r['id'] for r in rows})==len(rows)
    unresolved = [r['id'] for r in rows if r['quintic_status']=='UNRESOLVED']
    report = dict(status='INCOMPLETE' if unresolved else 'ALL_CASES_CLASSIFIED_PENDING_FINAL_AUDIT',
                  max_enumerated_level=191,all_level_boundary=strict['all_level_boundary'],
                  strict_inventory_sha256=hashlib.sha256(strict_path.read_bytes()).hexdigest(),
                  endpoint_source='ENDPOINTS.md',unresolved=unresolved,curves=rows)
    (ROOT/'complete_inventory.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Combined curves:',len(rows),'Unresolved:',len(unresolved),report['status'])


if __name__=='__main__':
    main()
