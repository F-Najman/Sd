from pathlib import Path
import time,subprocess,concurrent.futures,json
W=Path(__file__).resolve().parent
while not(W/'fi_exports.json').exists():time.sleep(5)
assert all(a['status']=='PASS'for a in json.loads((W/'fi_exports.json').read_text()))
jobs=[('relative53.m',['P:=53','H:=10','SSDegree:=13']),('full_cusps53.m',['P:=53','H:=10','SSDegree:=13']),('relative73.m',['P:=73','H:=2','SSDegree:=6']),('relative73_nc.m',['P:=73','H:=2','SSDegree:=9']),('relative113.m',['P:=113','H:=4','SSDegree:=7']),('relative127.m',[])]
def one(job):
 name,args=job;log=W/name.replace('.m','.log')
 with log.open('w')as f:r=subprocess.run(['magma','-b']+args+[str(W/name)],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();assert r.returncode==0 and'EXPORT_COMPLETE'in s and'Runtime error'not in s,job
 print('S20_RELATIVE_EXPORT_PASS',name,flush=True);return name
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:a=list(ex.map(one,jobs))
(W/'relative_exports.json').write_text(json.dumps({'status':'PASS','files':a},indent=2)+'\n')
