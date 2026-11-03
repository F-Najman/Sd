from pathlib import Path
import subprocess,concurrent.futures
W=Path(__file__).resolve().parent
jobs=[('relative53.m',['P:=53','H:=10','SSDegree:=13']),('relative61.m',['P:=61','H:=9','SSDegree:=15']),('relative73.m',['P:=73','H:=2','SSDegree:=6']),('relative73_nc.m',['P:=73','H:=2','SSDegree:=9']),('relative127.m',[])]+[(f'match{n}.m',[f'P:={n}'])for n in [47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131]]
def one(j):
 name,args=j
 with(W/name.replace('.m','.log')).open('w')as o:r=subprocess.run(['magma','-b']+args+[str(W/name)],stdout=o,stderr=subprocess.STDOUT)
 print('S19_RELATIVE_EXPORT',name,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:list(ex.map(one,jobs))
