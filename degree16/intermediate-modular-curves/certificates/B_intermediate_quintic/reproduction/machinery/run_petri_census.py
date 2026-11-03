"""Run independent Petri censuses for unresolved function cases (Sage Python)."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(row):
    directory = ROOT/row['model_certificate']
    subprocess.run([sys.executable,str(ROOT/'integral_relations.py'),str(directory)],check=True)
    integral = directory/'integral_model'
    prime = next(p for p in [2,3,5,7,11] if row['level'] % p)
    checked(['magma','-b',f'p:={prime}',str(ROOT/'petri_pencil_census.m')],integral,
            f'petri_p{prime}.log','SUCCESS exhaustive Petri-pencil metadata')
    return row['id'],(integral/f'petri_p{prime}.log').read_text()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--levels',type=int,nargs='*')
    args = parser.parse_args()
    rows = [r for r in json.loads((ROOT/'classification_inventory.json').read_text())['curves']
            if r['quintic_status']=='UNRESOLVED' and r['degree5_function']=='UNKNOWN'
            and (args.levels is None or r['level'] in args.levels)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run,row) for row in rows]
        for job in concurrent.futures.as_completed(jobs):
            try:
                print(job.result(),flush=True)
            except Exception as error:
                print('CENSUS FAILED (not a mathematical conclusion)',repr(error),flush=True)
