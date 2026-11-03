"""Isolated reproducible jobs for unresolved genus-five curves.

Run with Sage's Python. Each subprocess uses that same interpreter.
Only new local modules and standard Sage/Magma are used.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def checked(command, cwd, logname, success):
    with (cwd/logname).open('w') as stream:
        result = subprocess.run(command,cwd=cwd,stdout=stream,stderr=subprocess.STDOUT)
    text = (cwd/logname).read_text()
    if result.returncode != 0 or 'error' in text.lower() or success not in text:
        raise RuntimeError(f'{cwd.name}/{logname}: missing success or error')


def run(row):
    # Full subgroup in the metadata remains the identity, not this short name.
    name = f"N{row['level']}_d{row['degree_to_x0']}"
    directory = ROOT/'genus5_jobs'/name
    directory.mkdir(parents=True,exist_ok=True)
    metadata = directory/'curve.json'
    if metadata.exists():
        assert json.loads(metadata.read_text())['id'] == row['id']
    metadata.write_text(json.dumps(row,indent=2)+'\n')
    start = time.monotonic()
    checked([sys.executable,str(ROOT/'canonical_relations.py'),str(row['level']),
             '--generators',*map(str,row['delta']),'--output','relations.json'],
            directory,'relations.log','SUCCESS exact relations')
    subprocess.run([sys.executable,str(ROOT/'export_genus5.py'),'relations.json'],
                   cwd=directory,check=True)
    checked(['magma','-b',str(ROOT/'verify_genus5.m')],directory,
            'geometry.log','SUCCESS: smooth genus-five')
    # Search ordinary effective divisors first, then canonical residuals.
    searches = [('search_quintic_genus5.m','effective.log'),
                ('search_residual_genus5.m','residual.log')]
    found = False
    for script, log in searches:
        checked(['magma','-b',str(ROOT/script)],directory,log,
                '')
        output = (directory/log).read_text()
        if 'SUCCESS EXACT DEGREE FIVE' in output:
            found = True
            break
        assert 'SEARCH FINISHED:' in output
    files = [ROOT/'canonical_relations.py',ROOT/'enumeration.py',
             ROOT/'export_genus5.py',ROOT/'verify_genus5.m',
             ROOT/'search_quintic_genus5.m',ROOT/'search_residual_genus5.m',
             ROOT/'RATIONAL_MODELS.md']
    report = {'id':row['id'],'model_verified':True,
              'quintic_witness':found,'seconds':round(time.monotonic()-start,2),
              'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (directory/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    return name,report


def main():
    inventory = json.loads((ROOT/'classification_inventory.json').read_text())
    rows = [r for r in inventory['curves'] if r['genus']==5 and r['quintic_status']=='UNRESOLVED']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run,row) for row in rows]
        for job in concurrent.futures.as_completed(jobs):
            name,report = job.result()
            print(name,report,flush=True)
    print('SUCCESS batch completed; negative searches are not exclusions.')


if __name__ == '__main__':
    main()
