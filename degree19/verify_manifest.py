from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;d=json.loads((W/'proof_manifest.json').read_text());bad=[]
for name,want in d.items():
 p=Path(name);actual=hashlib.sha256(p.read_bytes()).hexdigest()if p.exists()else None
 if actual!=want:bad.append(name)
assert not bad,bad
out={'status':'PASS','files':len(d),'manifest_sha256':hashlib.sha256((W/'proof_manifest.json').read_bytes()).hexdigest()};(W/'manifest_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_PROOF_MANIFEST_VERIFIED',out,flush=True)
