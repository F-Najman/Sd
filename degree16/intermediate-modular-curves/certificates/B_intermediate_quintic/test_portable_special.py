"""Re-execute all special negatives using only the portable machinery tree.

Run with Sage's Python. Each computation uses a disposable copy, so this
test does not change the bundle's saved certificates or its hash manifest.
This deliberately checks more than the saved-ledger packaging test.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import replay_special

FOLDER = Path(__file__).resolve().parent
replay_special.ROOT = FOLDER/'reproduction'/'machinery'
replay_special.OUT = FOLDER/'audit_runs'/'portable_special'


if __name__ == '__main__':
    out = replay_special.OUT
    out.mkdir(parents=True,exist_ok=True)
    manifest = json.loads((FOLDER/'reproduction'/'manifest.json').read_text())
    assert manifest['status'] == 'PORTABLE_LEDGER_BUNDLE_PASS'
    for relative,value in manifest['files'].items():
        path = FOLDER/'reproduction'/relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==value,relative
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(replay_special.replay,task,replay_special.ROOT)
                   for task in replay_special.TASKS]
        for future in as_completed(futures):
            results.append(future.result())
    assert len(results)==12
    receipt = dict(status='PORTABLE_ALL_12_SPECIAL_REPLAYS_PASS',
                   receipts={r['name']:hashlib.sha256((out/r['name']/'receipt.json').read_bytes()).hexdigest()
                             for r in results},
                   bundle_manifest_sha256=hashlib.sha256((FOLDER/'reproduction'/'manifest.json').read_bytes()).hexdigest())
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(receipt['status'],flush=True)
