from pathlib import Path
from unit_arithmetic import lit
import subprocess,concurrent.futures,json,re
W=Path(__file__).resolve().parent;s=(W/'relative73_nc_data.m').read_text();SS=lit(s,'RelativeSSMatrices');JC=lit(s,'RelativeCuspJets');m=len(JC);d=9
assert m==36 and len(SS)==4

def expected():
 total=0
 for first in range(1,d+1):
  a=[1]+[0]*d
  for _ in range(m-1):a=[sum(a[t-k]for k in range(min(t,first)+1))for t in range(d+1)]
  total+=a[d-first]
 return total

def one(si):
 mat=SS[si];piv={}
 for j in range(9):
  x=sum(row[j]<<i for i,row in enumerate(mat))
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 assert len(piv)==8
 def red(x):
  for k,v in sorted(piv.items(),reverse=True):
   if x>>k&1:x^=v
  return x
 rows=[red(sum(JC[k][i][j]<<i for i in range(len(mat))))for k in range(m)for j in range(d)]
 p=W/f'relative73_nc_{si}.txt';p.write_text(f'{m} {d} 4\n'+'\n'.join(' '.join(str(x>>(64*k)&((1<<64)-1))for k in range(8))for x in rows)+'\n')
 log=W/f'relative73_nc_{si}.log'
 with log.open('w')as f:r=subprocess.run([str(W/'relative_prefixes'),str(p)],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();cnt=re.search(r'checked=(\d+)',s);ok=r.returncode==0 and cnt and int(cnt[1])==expected();rec={'ss_translate':si,'status':'PASS'if ok else'FAIL','checked':int(cnt[1])if cnt else 0,'expected':expected(),'detail':s[-600:]};print(rec,flush=True);return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(one,range(4)))
(W/'relative73_nc_verified.json').write_text(json.dumps({'status':'PASS'if all(v['status']=='PASS'for v in rs)else'FAIL','results':rs},indent=2)+'\n')
