from pathlib import Path
import subprocess,json
W=Path(__file__).resolve().parent;a=json.loads((W/'small_jet_jobs.json').read_text());sets={int(k):v for k,v in a['degree_sets'].items()};jobs=[]
for n,ds in sets.items():
 if n==139:jobs.append((n,'pair_low139.py','pair_low_sieve.log'))
 elif any(20-d in ds for d in ds):jobs.append((n,'pair_sieve.py','pair_sieve.log'))
for n in[73,89,113,127]:jobs.append((n,'mixed_sieve.py','mixed_sieve.log'))
done=[]
for n,name,log in jobs:
 with(W/f'full{n}'/log).open('w')as f:r=subprocess.run(['python3',str(W/name),str(n)],stdout=f,stderr=subprocess.STDOUT)
 s=(W/f'full{n}'/log).read_text();assert r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in s,(n,name)
 done.append({'N':n,'script':name,'status':'COMPLETED'});print('S20_SMALL_SIEVE_COMPLETED',n,name,flush=True)
(W/'small_sieve_results.json').write_text(json.dumps(done,indent=2)+'\n')
