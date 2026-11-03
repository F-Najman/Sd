from pathlib import Path
import subprocess,json,time,hashlib,fcntl
W=Path(__file__).resolve().parent;B=W.parents[1];lock=open(W/'finalize.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
def complete(p,key,n):
 if not p.exists():return False
 try:a=json.loads(p.read_text())
 except json.JSONDecodeError:return False
 return a.get('status')=='PASS'and a.get(key)==n
print('S19_FINALIZER_WAITING_FOR_ALL592_CHARACTERS_AND_PADE_CERTIFICATES',flush=True)
while not(complete(W/'large_native_results.json','characters',592)and complete(W/'independent_sequence_results.json','checked',592)):time.sleep(5)
p=json.loads((W/'character_library_provenance.json').read_text());assert hashlib.sha256(Path(p['frozen']).read_bytes()).hexdigest()==p['sha256'];assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in p['Magma_internal_sources'].items())
for name in['verify_large.py','verify_coverage.py','package_result.py','build_manifest.py','verify_manifest.py']:
 log=W/(name.replace('.py','.log'));print('S19_FINALIZER_RUNNING',name,flush=True)
 with log.open('w')as o:r=subprocess.run(['python3',str(W/name)],cwd=B,stdout=o,stderr=subprocess.STDOUT)
 assert r.returncode==0,(name,log)
print('S19_FINAL_PROOF_AND_CERTIFICATE_PACKET_COMPLETE',flush=True)
