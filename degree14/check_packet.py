from pathlib import Path
import tempfile,zipfile,json,hashlib,subprocess,time
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';root=Path(tempfile.mkdtemp(prefix='S14_packet_check_'));tt=time.monotonic()
with zipfile.ZipFile(O/'S14_certificates.zip')as z:z.extractall(root)
m=json.load(open(root/'manifest.json'))
for name,v in m.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==v['sha256'],name
logs=[];commands=[['python','relocate.py']]+[['g++','-O3','-std=c++17',f'work/degree14/{stem}.cpp','-o',f'work/degree14/{stem}']for stem in['relation_check','check_prefixes','gon_prefixes']]+[['python','work/degree14/check_fi.py'],['python','work/degree14/gonality53.py'],['python','work/degree14/verify_auxiliary.py'],['magma','-b','work/degree14/quotient127.m'],['python','work/degree14/verify_ranks.py'],['python','work/degree14/verify_coverage.py']]
for args in commands:
 print('PACKET_STAGE',args,flush=True);r=subprocess.run(args,cwd=root,capture_output=True,text=True);logs.append({'args':args,'exit':r.returncode,'stdout':r.stdout[-1600:],'stderr':r.stderr[-1600:]});assert r.returncode==0,logs[-1]
num=[name for name in m if name.endswith(('units_data.m','hecke_jets.m','matrices.json.gz'))]
for name in num:assert hashlib.sha256((root/name).read_bytes()).hexdigest()==m[name]['sha256'],name
out={'status':'PASS','extracted_root':str(root),'files_verified':len(m),'numerical_files_unchanged':len(num),'sha256':hashlib.sha256((O/'S14_certificates.zip').read_bytes()).hexdigest(),'logs':logs,'elapsed':time.monotonic()-tt};(W/'packet_portability.json').write_text(json.dumps(out,indent=2)+'\n');print('S14_PACKET_PORTABILITY PASS',len(m),'files elapsed',out['elapsed'])
