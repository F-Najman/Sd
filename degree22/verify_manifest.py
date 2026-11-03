"""Stream-verify every file in the complete inherited and fresh proof closure."""
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;a=json.loads((W/'proof_manifest.json').read_text())
for i,(name,want)in enumerate(a.items()):
 with Path(name).open('rb')as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
 assert actual==want,name
 if(i+1)%10000==0:print('S22_MANIFEST_VERIFY_PROGRESS',i+1,'/',len(a),flush=True)
(W/'manifest_verified.json').write_text(json.dumps({'status':'PASS','files':len(a),'manifest_sha256':hashlib.sha256((W/'proof_manifest.json').read_bytes()).hexdigest()},indent=2)+'\n');print('S22_FULL_MANIFEST_VERIFIED',len(a),flush=True)
