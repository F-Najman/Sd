"""Fast consistency audit of the checked ledger; no expensive CAS replay.

Pass --require-complete to fail if any curve remains unresolved. The full
replay commands and the distinction between checking and recomputing a
certificate are documented in REPRODUCING.md.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete',action='store_true')
    args = parser.parse_args()
    subprocess.run([sys.executable,'-m','unittest','-v'],cwd=ROOT,check=True)
    for script in ['build_inventory.py','build_complete_inventory.py','write_classification_report.py']:
        subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
    data = json.loads((ROOT/'complete_inventory.json').read_text())
    unresolved = data['unresolved']
    print(f'CONSISTENT checked inventory; {len(unresolved)} unresolved curves.',flush=True)
    if args.require_complete and unresolved:
        print('NOT COMPLETE: no global classification certificate is asserted.',flush=True)
        return 2
    if args.require_complete:
        data['status'] = 'ALL_CASES_CLASSIFIED_AND_AUDITED'
        (ROOT/'complete_inventory.json').write_text(json.dumps(data,indent=2)+'\n')
        notes = ['AUDIT.md','ENDPOINTS.md','RATIONAL_MODELS.md','MODEL_IDENTIFICATION.md',
                 'LOW_GENUS.md','UNIFORM_EXCLUSIONS.md','BIELLIPTIC_OBSTRUCTION.md',
                 'HECKE_TORSION40.md','PULLBACK_TORSION48.md','PETRI_LIFTING_CERTIFICATE.md',
                 'ELLIPTIC_DEGREE_EXCLUSIONS.md','DEBARRE_FAHLAOUI_OBSTRUCTION.md',
                 'ELLIPTIC_FAMILY_CERTIFICATE.md','ELLIPTIC_FAMILY65_LINEAR.md',
                 'ELLIPTIC_FAMILY_SMALL_PRIME.md','CASE43.md','CASE64.md','PROOF_OVERVIEW.md']
        files = notes+['audit_results.py','build_inventory.py','build_complete_inventory.py',
                       'write_classification_report.py','classification_inventory.json',
                       'complete_inventory.json','CLASSIFICATION_TABLE.md']
        digest = lambda name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        receipt = dict(status='PASS',scope='All X_Delta(N), with the stated published and X0 inputs',
                       enumerated_pairs=len(data['curves']),strict_pairs=sum(r['strict'] for r in data['curves']),
                       positive_strict_pairs=sum(r['strict'] and r['quintic_status'].startswith('INFINITE')
                                                 for r in data['curves']),unresolved=0,
                       sha256={name:digest(name) for name in files})
        (ROOT/'final_audit.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print('FINAL AUDIT PASS: all cases classified with stated external mathematical inputs.',flush=True)
    return 0


if __name__=='__main__':
    sys.exit(main())
