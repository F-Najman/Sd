from pathlib import Path
W=Path(__file__).resolve().parent;O=W.parent/'degree18';(W/'FI').mkdir(exist_ok=True)
for name in ['export_FI_fast.m','export_FI_alpha_fast.m','export_combined_FI.m','run_fi.py','check_fi.py','pipeline_sieves.py','full_sieve.py']:
 s=(O/name).read_text().replace(str(O),str(W)).replace('d:=18','d:=19').replace('d==18','d==19').replace('r!=18','r!=19').replace('S18_','S19_')
 if name=='export_FI_alpha_fast.m':s=s.replace('127,131]','127,131,137]')
 if name=='run_fi.py':s=s.replace("(131,13,'2','3','alpha_fast')","(131,13,'2','3','alpha_fast'),(137,68,'2','3','alpha_fast')").replace('max_workers=4','max_workers=3')
 if name=='check_fi.py':s=s.replace('127,131]','127,131,137]').replace('range(7,12)','range(7,d-6)').replace('range(8)','range(16)').replace('max_workers=4','max_workers=2')
 if name=='pipeline_sieves.py':s=s.replace('r[0]==18','(n==137 or r[0]==19)').replace('max_workers=4','max_workers=2')
 if name=='full_sieve.py':
  a=s.index('def pmul(');b=s.index('def tensor(',a)
  s=s[:a]+'''from sage.libs.ntl.ntl_GF2X import ntl_GF2X
from functools import lru_cache
@lru_cache(maxsize=16384)
def as_ntl(x):return ntl_GF2X('0x'+format(x,'x')[::-1])
def pmul(x,y):return int((as_ntl(x)*as_ntl(y)).hex()[2:][::-1],16)&mask
'''+s[b:]
 (W/name).write_text(s)
s=(O/'compress_FI.py').read_text().replace('<=512','<=1024').replace('range(8)','range(16)');(W/'compress_FI.py').write_text(s)
for name in ['check_prefixes.cpp','relative_prefixes.cpp','relation_check.cpp']:
 s=(O/name).read_text().replace('uint64_t,8>','uint64_t,16>').replace('k=7','k=15').replace('<8;','<16;').replace('V,512>','V,1024>').replace('used[512]','used[1024]')
 (W/name).write_text(s)
print('S19_LOCAL_WORKERS_PREPARED')
