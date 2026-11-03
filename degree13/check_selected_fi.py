from pathlib import Path
import json,subprocess,concurrent.futures,time
W=Path(__file__).resolve().parent;H=W/'FI';Ns=[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
def expected(i,d):
 total=0
 for first in range(1,d+1):
  cap=min(first,d//2);a=[1]+[0]*d
  for _ in range(i-1):a=[sum(a[t-k]for k in range(min(t,cap)+1))for t in range(d+1)]
  total+=a[d-first]
 return total
def one(n):
 p=H/({43:'FI43_combined',79:'FI79_i39'}.get(n,f'FI{n}')+'.compressed.txt')
 while not p.exists():time.sleep(2)
 while True:
  ls=p.read_text().splitlines();hdr=list(map(int,ls[0].split()))
  if len(ls)==hdr[4]+1:break
  time.sleep(1)
 lev,i,tn,gen,nr,nc,d,rank=hdr;assert lev==n and d==13
 rows=[sum(int(v)<<(64*j)for j,v in enumerate(l.split()))for l in ls[1:]]
 basis={};rels=[]
 for k,x in enumerate(rows):
  c=1<<k
  while x:
   j=x.bit_length()-1
   if j in basis:v,b=basis[j];x^=v;c^=b
   else:basis[j]=(x,c);break
  else:rels.append(c)
 assert len(basis)==rank and len(rels)==nr-rank
 if n==79:
  z=H/'FI79_rechecked.relations.txt';z.write_text(f'{i} {d} {len(rels)}\n'+'\n'.join(' '.join(str(c>>(64*k)&((1<<64)-1))for k in range(8))for c in rels)+'\n');assert len(rels)==25
  cp=subprocess.run([str(W/'relation_check'),str(z)],capture_output=True,text=True,check=True);assert 'PASS relations=25 tested=33554431'in cp.stdout
  out={'N':n,'status':'PASS','method':'complete binary relation enumeration in C++','relations':len(rels),'tested_relations':33554431,'covered_degree13_tuples':expected(i,d)}
 elif len(rels)<=16:
  v=0;tested=0;fail=[]
  for k in range(1,1<<len(rels)):
   v^=rels[(k&-k).bit_length()-1];m0=(v&((1<<d)-1)).bit_length();other=[((v>>(d+6*j))&63).bit_length()for j in range(i-1)];cost=max([m0]+other)+sum(other);tested+=1
   if cost<=d:fail.append({'relation':hex(v),'minimum_normalized_degree':cost});break
  out={'N':n,'status':'FAIL'if fail else'PASS','method':'complete binary relation enumeration','relations':len(rels),'tested_relations':tested,'failures':fail,'covered_degree13_tuples':expected(i,d)}
 else:
  q=H/f'FI{n}_rechecked_prefix.log'
  with q.open('w')as f:r=subprocess.run([str(W/'check_prefixes'),str(p)],stdout=f,stderr=subprocess.STDOUT)
  s=q.read_text();import re;got=int(re.search(r'checked=(\d+)',s)[1]);ok=r.returncode==0 and'status=PASS'in s and got==expected(i,d)
  out={'N':n,'status':'PASS'if ok else'FAIL','method':'complete cusp-prefix enumeration','checked':got,'independent_expected':expected(i,d),'relations':len(rels)}
 (H/f'FI{n}_rechecked.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True);return out

with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(one,Ns))
assert all(r['status']=='PASS'for r in rs),rs
(W/'formal_immersion_rechecked.json').write_text(json.dumps({'status':'PASS','results':rs},indent=2)+'\n')
