"""Fresh small arithmetic inputs: elliptic obstructions and J1 rank zero.

Standard Python suffices; Magma must be on PATH. No saved output is used
to decide whether a case passed.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent/'audit_runs'/'arithmetic_inputs'
TASKS = [
    ('degree37','small_density_elliptic.m',['N:=37'],
     ['SUCCESS small-density elliptic obstruction','minimum_positive_elliptic_degree=12']),
    ('degree57','small_density_elliptic.m',['N:=57'],
     ['SUCCESS small-density elliptic obstruction','minimum_positive_elliptic_degree=8']),
    ('rank_endpoints','rank_zero_endpoints.m',[],
     ['SUCCESS rank-zero endpoint certificates']),
]
for n in [73,109,125]:
    TASKS.append((f'elliptic{n}','elliptic_factors.m',[f'N:={n}'],
                  ['SUCCESS elliptic factor census','CERTIFIED: no positive-rank elliptic factors']))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(task):
    name,script,parameters,markers = task
    directory = OUT/name
    directory.mkdir()
    source_hash = digest(ROOT/script)
    command = ['magma','-b',*parameters,str(ROOT/script)]
    with (directory/'run.log').open('w') as stream:
        process = subprocess.run(command,cwd=directory,stdout=stream,stderr=subprocess.STDOUT)
    output = (directory/'run.log').read_text()
    assert process.returncode == 0 and all(m in output for m in markers),name
    assert not any(m in output for m in ['Runtime error','User error','Assertion failed']),name
    assert digest(ROOT/script) == source_hash
    receipt = dict(status='FRESH_ARITHMETIC_INPUT_PASS',name=name,command=command,
                   source_sha256={script:source_hash},log_sha256=digest(directory/'run.log'))
    (directory/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS',name,flush=True)
    return name


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        names = list(pool.map(run,TASKS))
    receipt = dict(status='FRESH_ALL_6_ARITHMETIC_INPUTS_PASS',
                   receipts={name:digest(OUT/name/'receipt.json') for name in names})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(receipt['status'],flush=True)
