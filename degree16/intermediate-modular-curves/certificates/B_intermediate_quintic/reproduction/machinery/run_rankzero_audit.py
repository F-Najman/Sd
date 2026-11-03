"""Replay every rank-zero input used directly by the strict classification.

Only the census subgroup is passed to Magma, never a subgroup index in place
of the subgroup. Outputs are parsed back and checked against that input.
The new directory is isolated from all existing proof artifacts.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
from run_genus5_batch import checked
from enumeration import signature

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(task):
    kind,row = task
    n = row['level']
    identifier = row['id'] if kind=='intermediate' else f'X1({n})'
    key = hashlib.sha256(identifier.encode()).hexdigest()[:16]
    directory = ROOT/'rankzero_replays'/key
    directory.mkdir(parents=True,exist_ok=True)
    script = 'intermediate_central_value.m' if kind=='intermediate' else 'central_value.m'
    command = ['magma','-b',f'N:={n}']
    if kind=='intermediate':
        command += [f'g:={row["genus"]}','delta:='+','.join(map(str,row['delta']))]
    command += [str(ROOT/script)]
    checked(command,directory,'central_value.log','SUCCESS')
    text = ' '.join((directory/'central_value.log').read_text().split())
    assert 'central_zero=false' in text and 'central_zero=true' not in text
    if kind=='intermediate':
        match = re.search(r'RESULT N=(\d+) delta=\[([^]]*)\] dimension=(\d+) central_zero=false',text,re.S)
        assert match and int(match[1])==n and int(match[3])==row['genus']
        assert [int(s.strip()) for s in match[2].split(',')]==row['delta']
    else:
        match = re.search(r'RESULT N=(\d+) dimension=(\d+) central_zero=false',text)
        assert match and int(match[1])==n
        assert int(match[2])==signature(n,tuple(sorted({1%n,(-1)%n})))['genus']
    sources = ['run_rankzero_audit.py',script,'enumeration.py',
               'run_genus5_batch.py','UNIFORM_EXCLUSIONS.md']
    (directory/'input.json').write_text(json.dumps(dict(kind=kind,row=row),indent=2)+'\n')
    certificate = dict(id=identifier,status='RANK_ZERO_BY_EXACT_CENTRAL_VALUE',
                       source_sha256={s:digest(ROOT/s) for s in sources},
                       artifact_sha256={s:digest(directory/s) for s in ['input.json','central_value.log']})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS replayed exact rank-zero input',identifier,flush=True)


if __name__=='__main__':
    rows = json.loads((ROOT/'classification_inventory.json').read_text())['curves']
    direct = [r for r in rows if r['quintic_status'] in {
        'FINITE_BY_INTERMEDIATE_RANK_ZERO','FINITE_BY_BIELLIPTIC_AND_RANK_ZERO'}]
    endpoints = sorted({r['level'] for r in rows if r['quintic_status']=='FINITE_BY_RANK_ZERO_AND_GONALITY'})
    tasks = [('intermediate',r) for r in direct]+[('endpoint',dict(level=n)) for n in endpoints]
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(run,tasks))
    print('SUCCESS all direct rank-zero inputs replayed',len(tasks),flush=True)
