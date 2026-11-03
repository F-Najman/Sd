"""Exact L-values of actual intermediate Jacobians; independent genus check."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent


def run(row):
    identifier = hashlib.sha256(row['id'].encode()).hexdigest()[:16]
    log = ROOT/'intermediate_central'/f'{identifier}.log'
    command = ['magma','-b',f'N:={row["level"]}',f'g:={row["genus"]}',
               'delta:='+','.join(map(str,row['delta'])),'intermediate_central_value.m']
    with log.open('w') as stream:
        result = subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    text = log.read_text()
    assert result.returncode == 0 and 'SUCCESS intermediate central-value test' in text
    assert 'error' not in text.lower()
    return row['id'],dict(rank_zero_proved='central_zero=false' in text,
                          log=str(log.relative_to(ROOT)),genus_checked=row['genus'])


def main():
    (ROOT/'intermediate_central').mkdir(exist_ok=True)
    rows = json.loads((ROOT/'classification_inventory.json').read_text())['curves']
    rows = [r for r in rows if r['quintic_status']=='UNRESOLVED']
    answers = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = [pool.submit(run,r) for r in sorted(rows,key=lambda r:r['genus'])]
        for future in as_completed(pending):
            identifier,result = future.result()
            answers[identifier] = result
            # Each completed result is durable even while the sweep continues.
            (ROOT/'intermediate_central.json').write_text(json.dumps(answers,indent=2)+'\n')
            print(identifier,result,flush=True)
    print('SUCCESS intermediate central-value sweep')


if __name__ == '__main__':
    main()
