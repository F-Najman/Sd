from pathlib import Path
import json,hashlib,time
W=Path(__file__).resolve().parent;M=W.parent/'degree21/proof_manifest.json';pinned='1ce61f220611ed348af3b0e92554a21f46d2bedd48058d45b654ac3f26e8f1c5'
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert sha(M)==pinned;data=json.loads(M.read_text());assert len(data)==100184;bad=[];tt=time.monotonic()
for i,(k,v)in enumerate(data.items(),1):
 p=Path(k);want=v if isinstance(v,str)else v['sha256'];actual=sha(p)if p.exists()else None
 if actual!=want:bad.append({'path':str(p),'expected':want,'actual':actual})
 if i%10000==0:print('S22_INHERITED_HASH_PROGRESS',i,round(time.monotonic()-tt,1),flush=True)
a={'status':'PASS'if not bad else'FAIL','files':len(data),'manifest_sha256':pinned,'bad':bad};(W/'inherited_manifest_verified.json').write_text(json.dumps(a,indent=2)+'\n');print('S22_PARENT_MANIFEST',a['status'],len(data),'bad',len(bad),flush=True);assert not bad
