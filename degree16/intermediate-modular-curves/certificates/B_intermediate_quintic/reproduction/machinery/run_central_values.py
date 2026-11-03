"""Exact central values at unresolved levels, retaining completed transcripts."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent


def run(n):
    path = ROOT/'central_values'/f'{n}.log'
    if path.exists():
        output = path.read_text()
        if 'SUCCESS central-value test' in output and 'error' not in output.lower():
            return n, 'central_zero=false' in output
    with path.open('w') as log:
        result = subprocess.run(['magma','-b',f'N:={n}','central_value.m'],
                                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    output = path.read_text()
    assert result.returncode == 0 and 'SUCCESS central-value test' in output
    assert 'error' not in output.lower()
    return n, 'central_zero=false' in output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-level',type=int,default=50)
    args = parser.parse_args()
    rows = json.loads((ROOT/'classification_inventory.json').read_text())['curves']
    levels = sorted({r['level'] for r in rows if r['level'] <= args.max_level and r['quintic_status']=='UNRESOLVED'})
    (ROOT/'central_values').mkdir(exist_ok=True)
    previous = ROOT/'central_values.json'
    answer = json.loads(previous.read_text()) if previous.exists() else {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run,n) for n in levels]
        for future in as_completed(jobs):
            n,nonzero = future.result()
            answer[str(n)] = {'rank_zero_proved':nonzero}
            print(n,answer[str(n)],flush=True)
    (ROOT/'central_values.json').write_text(json.dumps(answer,indent=2)+'\n')
    print('SUCCESS central-value batch')


if __name__ == '__main__':
    main()
