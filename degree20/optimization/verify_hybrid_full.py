from pathlib import Path
import subprocess,json,re,ast,time,hashlib
O=Path(__file__).resolve().parent;W=O.parent;a=json.loads((O/'benchmark_input.json').read_text());out=O/'hybrid_full_sequence.m';log=O/'hybrid_full.log';t=time.monotonic()
with log.open('w')as f:r=subprocess.run([str(W/'krylov_hybrid'),str(O/'benchmark_sparse.txt'),str(out)],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0 and'S20_CPP_KRYLOV_COMPLETE'in log.read_text()
ref=Path(a['reference_sequence']);meta=ref.with_name(ref.name.replace('_sequence.m','.json'))
while not(ref.exists()and meta.exists()):time.sleep(5)
def parse(s,k):return ast.literal_eval(re.search(r'\b'+k+r':=(.*?);',s,re.S)[1])
s=out.read_text();r=ref.read_text();q=parse(s,'q');k=parse(s,'dimension');seq=parse(s,'sequence');assert parse(r,'q')==q and parse(r,'dimension')==k and parse(r,'linear_complexity')==k and len(seq)==2*k and seq==parse(r,'sequence')
sha=hashlib.sha256((O/'benchmark_sparse.txt').read_bytes()).hexdigest();state=json.loads(meta.read_text());assert state['status']=='PASS'and state['sparse_export_sha256']==sha
result={'status':'PASS','p':a['p'],'order':a['order'],'q':q,'dimension':k,'all_sequence_terms_checked':2*k,'sparse_input_sha256':sha,'legacy_sequence_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'hybrid_source_sha256':hashlib.sha256((W/'krylov_hybrid.cpp').read_bytes()).hexdigest(),'hybrid_binary_sha256':hashlib.sha256((W/'krylov_hybrid').read_bytes()).hexdigest(),'elapsed':time.monotonic()-t,'arithmetic':'identical exact matrix; dense rows and sparse rows partition the original entries; source indices fit uint16; same uint64 overflow bound'}
(O/'hybrid_full_replay_verified.json').write_text(json.dumps(result,indent=2)+'\n');print('S20_HYBRID_COMPLETE_SEQUENCE_REPLAY_PASS',result,flush=True)
