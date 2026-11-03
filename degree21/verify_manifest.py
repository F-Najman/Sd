from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;a=json.loads((W/'proof_manifest.json').read_text())
for name,want in a.items():
 with Path(name).open('rb')as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
 assert actual==want,name
(W/'manifest_verified.json').write_text(json.dumps({'status':'PASS','files':len(a),'manifest_sha256':hashlib.sha256((W/'proof_manifest.json').read_bytes()).hexdigest()},indent=2)+'\n');print('S21_FULL_MANIFEST_VERIFIED',len(a),flush=True)
