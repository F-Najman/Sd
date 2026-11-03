from pathlib import Path
import json,subprocess,concurrent.futures,time
W=Path(__file__).resolve().parent
while not(W/'small_jet_results.json').exists():time.sleep(10)
a=json.loads((W/'small_jet_results.json').read_text());assert a['status']=='PASS';sets=json.loads((W/'small_jet_jobs.json').read_text())['degree_sets'];jobs=[(int(n),'pair')for n in sets]+[(n,'mixed_new')for n in[73,89,109,113,127]]
def one(j):
 n,kind=j;H=W/f'full{n}'
 jp=H/('mixed_sieve.json'if kind=='mixed_new'else'pair_sieve.json')
 if jp.exists():
  z=json.loads(jp.read_text())
  if z['status']=='PASS'and not z['exceptions']:print('S22_SMALL_SIEVE_REUSED',j,flush=True);return{'N':n,'kind':kind,'status':'PASS'}
 if n==97:
  while not(H/'units_data_extended.m').exists()or'S22_EXTENDED97_BASIS_COMPLETE'not in(W/'extend97.log').read_text():time.sleep(10)
 with(H/(kind+'_sieve.log')).open('w')as f:r=subprocess.run(['sage',str(W/(kind+'_sieve.py')),str(n)],stdout=f,stderr=subprocess.STDOUT)
 s=(H/(kind+'_sieve.log')).read_text();assert r.returncode==0 and'AUDIT_FULL_SIEVE_COMPLETE'in s,(j,s[-1000:]);z=json.loads((H/('mixed_sieve.json'if kind=='mixed_new'else'pair_sieve.json')).read_text());print('S22_SMALL_SIEVE',j,z['status'],'exceptions',[(v['source'],v['degree'])for v in z['exceptions']],flush=True);return{'N':n,'kind':kind,'status':z['status']}
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:out=list(ex.map(one,jobs))
(W/'small_sieves_results.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_SMALL_SIEVES_COMPLETE',flush=True)
