from pathlib import Path
import subprocess,concurrent.futures,time,json,os
W=Path(__file__).resolve().parent
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
active={}
for line in subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines():
 if 'magma.exe -b'not in line:continue
 for n in ns:
  if f'/degree17/full{n}/stage2.m'in line:active[n]=int(line.split()[0])
def alive(pid):
 try:os.kill(pid,0);return True
 except ProcessLookupError:return False
def one(n):
 H=W/f'full{n}';start=time.monotonic()
 if n in active:
  while alive(active[n])and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'not in(H/'stage2.log').read_text():time.sleep(5)
 if not(H/'hecke_jets.m').exists():
  with(H/'stage2.log').open('w')as f:subprocess.run(['magma','-b',str(H/'stage2.m')],stdout=f,stderr=subprocess.STDOUT,check=True)
 s=(H/'stage2.log').read_text();assert 'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s and not any(x in s for x in['Runtime error','User error','Assertion failed'])
 print('S17_JETS_READY',n,round(time.monotonic()-start,1),flush=True)
 if not(H/'sieve.json').exists():
  with(H/'sieve.log').open('w')as f:subprocess.run(['python',str(W/'full_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT,check=True)
 a=json.load(open(H/'sieve.json'));print('S17_ORDINARY_DONE',n,a['source_orbits'],a['nonprincipal'],[(r['source'],r['degree'],r['orbit'])for r in a['exceptions']],round(time.monotonic()-start,1),flush=True);return{'N':n,'status':'PASS_WITH_EXCEPTIONS'if a['exceptions']else'PASS'}
with concurrent.futures.ThreadPoolExecutor(max_workers=12)as ex:rs=list(ex.map(one,ns))
(W/'ordinary_jobs.json').write_text(json.dumps(rs,indent=2)+'\n')
