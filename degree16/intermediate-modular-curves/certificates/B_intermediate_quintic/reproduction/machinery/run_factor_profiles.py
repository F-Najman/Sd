"""Profile the positive-rank cases where a degree-five function is excluded."""
import concurrent.futures
import json
from pathlib import Path
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(row):
    directory = ROOT/row['model_certificate']
    checked(['magma','-b',f'N:={row["level"]}',f'g:={row["genus"]}',
             'delta:='+','.join(map(str,row['delta'])),str(ROOT/'intermediate_factor_profile.m')],
            directory,'factor_profile.log','SUCCESS full intermediate factor profile')
    return row['id'], (directory/'factor_profile.log').read_text()


if __name__ == '__main__':
    rows = [r for r in json.loads((ROOT/'classification_inventory.json').read_text())['curves']
            if r['quintic_status']=='UNRESOLVED' and r['degree5_function']=='DOES_NOT_EXIST']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run,row) for row in rows]
        for future in concurrent.futures.as_completed(futures):
            print(future.result(),flush=True)
    print('SUCCESS factor profile batch finished',flush=True)
