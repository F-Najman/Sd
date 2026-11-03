from pathlib import Path
import zipfile,tempfile,json,hashlib,subprocess,time
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';tt=time.monotonic();root=Path(tempfile.mkdtemp(prefix='S13_packet_check_'))
with zipfile.ZipFile(O/'S13_certificates.zip')as z:z.extractall(root)
manifest=json.load(open(root/'manifest.json'))
for name,rec in manifest.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==rec['sha256'],name
logs=[]
for args in[['python','relocate.py'],['g++','-O3','-std=c++17','work/degree13/relation_check.cpp','-o','work/degree13/relation_check'],['python','work/degree13/verify_dyadic.py'],['python','work/degree13/verify_auxiliary.py'],['python','work/degree13/verify_coverage.py']]:
 r=subprocess.run(args,cwd=root,capture_output=True,text=True);logs.append({'args':args,'exit':r.returncode,'stdout':r.stdout[-2000:],'stderr':r.stderr[-2000:]});assert r.returncode==0,logs[-1]
# Every pure numerical Magma data file remains identical after path relocation.
numeric=[n for n in manifest if n.endswith(('units_data.m','hecke_jets.m','_sequence.m','.compressed.txt','.matrices.json.gz','matrices.json.gz','mixed43_tangents.m','two53_data.m'))]
for name in numeric:assert hashlib.sha256((root/name).read_bytes()).hexdigest()==manifest[name]['sha256'],name
out={'status':'PASS','packet_sha256':hashlib.sha256((O/'S13_certificates.zip').read_bytes()).hexdigest(),'extracted_root':str(root),'original_manifest_files_verified':len(manifest),'numerical_files_unchanged':len(numeric),'logs':logs,'elapsed':time.monotonic()-tt};(W/'packet_portability.json').write_text(json.dumps(out,indent=2)+'\n');print('S13_PACKET_PORTABILITY PASS files',len(manifest),'numeric',len(numeric),'elapsed',out['elapsed'])
