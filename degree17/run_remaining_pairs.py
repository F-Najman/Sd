from pathlib import Path
import subprocess,concurrent.futures,time,sys,json
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
ns=[]
for p in W.glob('sources*.m'):
 n=int(p.stem[7:])
 if n not in[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]or n==41:continue
 rs=lit(p.read_text().replace('true','True').replace('false','False'),'AuditSources')
 if min(v[0]for v in rs if v[6])<=8:ns.append(n)
def one(n):
 H=W/f'full{n}'
 while not(H/'hecke_jets.m').exists():time.sleep(5)
 with(H/'pair_sieve.log').open('w')as f:r=subprocess.run(['python',str(W/'pair_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 print('S17_PAIR_FINISHED',n,r.returncode,flush=True);return(n,r.returncode)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(one,sorted(ns)))
(W/'pair_jobs.json').write_text(json.dumps(rs,indent=2)+'\n')
