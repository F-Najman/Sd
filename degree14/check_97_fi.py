from pathlib import Path
import json,subprocess,re,concurrent.futures,time
W=Path(__file__).resolve().parent;H=W/'FI';Ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]
def kernel(rows):
 bs={};rels=[]
 for k,x in enumerate(rows):
  c=1<<k
  while x:
   j=x.bit_length()-1
   if j in bs:v,b=bs[j];x^=v;c^=b
   else:bs[j]=(x,c);break
  else:rels.append(c)
 return len(bs),rels
def expected(i,d,cap):
 total=0
 for first in range(1,d+1):
  a=[1]+[0]*d
  for _ in range(i-1):a=[sum(a[t-k]for k in range(min(t,first,cap)+1))for t in range(d+1)]
  total+=a[d-first]
 return total
def one(n):
 p=H/('FI97_i8.compressed.txt'if n==97 else f'FI{n}.compressed.txt')
 while not p.exists():time.sleep(1)
 ls=p.read_text().splitlines();v=list(map(int,ls[0].split()));lev,i,tn,gen,nr,nc,d,rk=v;assert lev==n and d==(2 if n==127 else 14)
 rows=[sum(int(v)<<(64*j)for j,v in enumerate(l.split()))for l in ls[1:]];assert len(rows)==nr and kernel(rows)[0]==rk
 if d==2:
  rank,rels=kernel(rows);rr=[kernel(rows[:2])[0]]+[kernel([rows[0],rows[2+j]])[0]for j in range(i-1)];assert all(v==2 for v in rr);out={'N':n,'status':'PASS','degree':d,'rows':nr,'rank':rank,'prefix_ranks':rr,'method':'all normalized degree2 cusp prefixes'}
 else:
  balanced=[kernel(rows[:7]+rows[d+7*j:d+7*j+7])[0]for j in range(i-1)]
  rr=rows[:d]+[v for j in range(i-1)for v in rows[d+7*j:d+7*j+6]];rank,rels=kernel(rr);p6=H/f'FI{n}_cap6.compressed.txt';hdr=v[:];hdr[4]=len(rr);hdr[7]=rank
  p6.write_text(' '.join(map(str,hdr))+'\n'+'\n'.join(' '.join(str(c>>(64*k)&((1<<64)-1))for k in range(8))for c in rr)+'\n')
  if len(rels)<=32:
   z=H/f'FI{n}_cap6.relations.txt';z.write_text(f'{i} {d} {len(rels)}\n'+'\n'.join(' '.join(str(c>>(64*k)&((1<<64)-1))for k in range(8))for c in rels)+'\n');cp=subprocess.run([str(W/'relation_check'),str(z)],capture_output=True,text=True);ok=cp.returncode==0;detail=cp.stdout
   (H/f'FI{n}_relations.log').write_text(cp.stdout+cp.stderr)
  else:
   with(H/f'FI{n}_prefix.log').open('w')as f:cp=subprocess.run([str(W/'check_prefixes'),str(p6)],stdout=f,stderr=subprocess.STDOUT)
   detail=(H/f'FI{n}_prefix.log').read_text();mm=re.search(r'checked=(\d+)',detail);ok=cp.returncode==0 and mm and int(mm[1])==expected(i,d,6)
  out={'N':n,'status':'PASS'if ok and all(x==14 for x in balanced)else'FAIL','degree':d,'rows_cap6':len(rr),'rank_cap6':rank,'kernel_dimension':len(rels),'balanced_pair_ranks':balanced,'normalized_tuples_cap6':expected(i,d,6),'detail':detail[-250:]}
 (H/f'FI{n}_verified.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True);return out

one(97)
