"""Recompute all direct rank-zero inputs without overwriting old evidence."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from enumeration import signature

rows = json.loads((root/'classification_inventory.json').read_text())['curves']
tasks = [('intermediate',r) for r in rows if r['quintic_status'] in
         {'FINITE_BY_INTERMEDIATE_RANK_ZERO','FINITE_BY_BIELLIPTIC_AND_RANK_ZERO'}]
levels = sorted({r['level'] for r in rows if r['quintic_status']=='FINITE_BY_RANK_ZERO_AND_GONALITY'})
tasks += [('endpoint',dict(level=n)) for n in levels]
base = Path(__file__).resolve().parent/'audit_runs'/'rankzero'
base.mkdir(parents=True,exist_ok=True)
def run(task):
    kind,row = task
    n = row['level']
    identifier = row['id'] if kind == 'intermediate' else f'X1({n})'
    key = hashlib.sha256(identifier.encode()).hexdigest()[:16]
    folder = base/key
    folder.mkdir(exist_ok=True)
    script = root/('intermediate_central_value.m' if kind=='intermediate' else 'central_value.m')
    command = ['magma','-b',f'N:={n}']
    if kind == 'intermediate':
        command += [f'g:={row["genus"]}','delta:='+','.join(map(str,row['delta']))]
    command += [str(script)]
    with (folder/'run.log').open('w') as log:
        result = subprocess.run(command,cwd=folder,stdout=log,stderr=subprocess.STDOUT)
    text = ' '.join((folder/'run.log').read_text().split())
    assert result.returncode == 0 and 'SUCCESS' in text and 'error' not in text.lower(), text
    assert 'central_zero=false' in text and 'central_zero=true' not in text, text
    expected = row.get('genus',signature(n,tuple(sorted({1%n,(-1)%n})))['genus'])
    assert re.search(rf'dimension={expected}\b',text), text
    assert re.search(rf'RESULT N={n}\b',text), text
    if kind=='intermediate':
        match = re.search(r'delta=\[([^]]*)\]',text)
        assert match and [int(x) for x in match[1].split(',')] == row['delta']
    receipt = dict(id=identifier,status='FRESH_EXACT_CENTRAL_VALUE_NONZERO',
                   command=command,genus=expected,
                   source_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                   log_sha256=hashlib.sha256((folder/'run.log').read_bytes()).hexdigest())
    (folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS',identifier,flush=True)
    return receipt
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run,tasks))
assert len(results)==65 and len({r['id'] for r in results})==65
(base/'receipt.json').write_text(json.dumps(dict(status='FRESH_RANKZERO_REPLAY_PASS',
                                                count=65,results=results),indent=2)+'\n')
print('FRESH_RANKZERO_REPLAY_PASS 65',flush=True)
