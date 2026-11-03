from pathlib import Path
import json,subprocess
W=Path(__file__).resolve().parent;out=[]
def ok(s):return any(t in s for t in ['EXPORT_COMPLETE','EXPORTED'])and not any(t in s for t in ['Runtime error','User error','Assertion failed','Traceback'])
for name,args in json.loads((W/'relative_jobs.json').read_text()):
 p=W/name.replace('.m','.log');s=p.read_text()if p.exists()else''
 if not ok(s):
  with p.open('w')as f:r=subprocess.run(['magma','-b']+args+[str(W/name)],stdout=f,stderr=subprocess.STDOUT)
  assert r.returncode==0,name;s=p.read_text()
 assert ok(s),name;out.append({'source':name,'status':'PASS'});print('S22_RELATIVE_EXPORT',name,True,flush=True)
(W/'relative_exports.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_RELATIVE_EXPORTS_COMPLETE',flush=True)
