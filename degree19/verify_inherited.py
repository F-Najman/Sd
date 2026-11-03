from pathlib import Path
import json,hashlib,time
W=Path(__file__).resolve().parent;O=W.parent/'degree18';d=json.loads((O/'proof_manifest.json').read_text());tt=time.monotonic();bad=[]
for k,v in d.items():
 p=Path(k);want=v if isinstance(v,str)else v['sha256'];h=hashlib.sha256(p.read_bytes()).hexdigest()if p.exists()else None
 if h!=want:bad.append(str(p))
assert not bad,bad
out={'status':'PASS','files':len(d),'manifest_sha256':hashlib.sha256((O/'proof_manifest.json').read_bytes()).hexdigest()};(W/'inherited_manifest_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_INHERITED_MANIFEST_VERIFIED',out,flush=True)
