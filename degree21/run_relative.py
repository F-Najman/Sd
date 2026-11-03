from pathlib import Path
import json,subprocess
W=Path(__file__).resolve().parent
for name,args in json.loads((W/'relative_jobs.json').read_text()):
 with(W/name.replace('.m','.log')).open('w')as f:r=subprocess.run(['magma','-b']+args+[str(W/name)],stdout=f,stderr=subprocess.STDOUT)
 s=(W/name.replace('.m','.log')).read_text();ok=r.returncode==0 and'EXPORT_COMPLETE'in s and'Runtime error'not in s;print('S21_RELATIVE_EXPORT',name,ok,flush=True)
 if not ok:raise RuntimeError(name)
print('S21_RELATIVE_EXPORTS_COMPLETE',flush=True)
