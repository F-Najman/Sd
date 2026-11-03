from pathlib import Path
import subprocess,concurrent.futures,json
W=Path(__file__).resolve().parent;Ns=[47,53,59,61,67,71,73,79,83,89,97,101,103]
def one(n):
 H=W/f'full{n}';p=H/'hecke_jets.m';assert p.exists()
 with(H/'sieve_extra.log').open('w')as o:r=subprocess.run(['python3',str(W/'full_sieve.py'),str(n)],stdout=o,stderr=subprocess.STDOUT)
 ok=r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in(H/'sieve_extra.log').read_text();print('S19_EXTRA_SIEVE_COMPLETE',n,ok,flush=True);return {'N':n,'status':'PASS'if ok else'FAIL'}
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:rs=list(ex.map(one,Ns))
(W/'extra_sieve_results.json').write_text(json.dumps(rs,indent=2)+'\n')
