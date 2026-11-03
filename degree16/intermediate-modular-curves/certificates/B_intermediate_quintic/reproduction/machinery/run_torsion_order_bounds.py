"""Compute fresh Frobenius torsion-order bounds for the final rank-zero cases."""
import concurrent.futures
import json
from pathlib import Path
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(row):
    directory = ROOT/row['model_certificate']
    checked(['magma','-b',f'N:={row["level"]}',f'g:={row["genus"]}',
             'delta:='+','.join(map(str,row['delta'])),str(ROOT/'torsion_order_bounds.m')],
            directory,'torsion_order_bound.log','SUCCESS prime-to-characteristic torsion-order bound')
    return row['id'],(directory/'torsion_order_bound.log').read_text()


if __name__ == '__main__':
    rows = [r for r in json.loads((ROOT/'classification_inventory.json').read_text())['curves']
            if r['quintic_status']=='UNRESOLVED' and r['level'] in [40,48,64]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(run,rows):
            print(result,flush=True)
