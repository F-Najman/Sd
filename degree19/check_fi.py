from pathlib import Path
import json,subprocess,re,concurrent.futures,time,sys,itertools
W=Path(__file__).resolve().parent;H=W/'FI';Ns=list(map(int,sys.argv[1:]))if len(sys.argv)>1 else[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137]
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
 assert p.exists(),p
 ls=p.read_text().splitlines();v=list(map(int,ls[0].split()));lev,i,tn,gen,nr,nc,d,rk=v;assert lev==n and d==19
 rows=[sum(int(v)<<(64*j)for j,v in enumerate(l.split()))for l in ls[1:]];assert len(rows)==nr and kernel(rows)[0]==rk
 at=lambda j,k:rows[d+9*(j-1):d+9*(j-1)+k]
 # All configurations with a non-first cusp of multiplicity >=7.
 stats={};fail=[]
 def ck(label,rr):
  r=kernel(rr)[0];stats[label]=stats.get(label,0)+1
  if r!=19:fail.append((label,r))
 # Normalized patterns with a non-first cusp of multiplicity 7 or 8.
 # The remaining degree is at most 3. Enumerate its multiset of cusps.
 for first in range(7,d-6):
  for second in range(7,min(first,9)+1):
   remaining=d-first-second
   if remaining<0:continue
   for j in range(1,i):
    others=[k for k in range(1,i)if k!=j]
    for positions in itertools.combinations_with_replacement(others,remaining):
     counts={k:positions.count(k)for k in set(positions)}
     rr=rows[:first]+at(j,second)+[v for k,mult in sorted(counts.items())for v in at(k,mult)]
     ck(f'{first}+{second}+rest{remaining}',rr)
 rr=rows[:d]+[v for j in range(1,i)for v in at(j,6)];rank,rels=kernel(rr);p6=H/f'FI{n}_cap6.compressed.txt';hdr=v[:];hdr[4]=len(rr);hdr[7]=rank
 p6.write_text(' '.join(map(str,hdr))+'\n'+'\n'.join(' '.join(str(c>>(64*k)&((1<<64)-1))for k in range(16))for c in rr)+'\n')
 if len(rels)<=32 and (1<<len(rels))<10*expected(i,d,6):
  z=H/f'FI{n}_cap6.relations.txt';z.write_text(f'{i} {d} {len(rels)}\n'+'\n'.join(' '.join(str(c>>(64*k)&((1<<64)-1))for k in range(16))for c in rels)+'\n');cp=subprocess.run([str(W/'relation_check'),str(z)],capture_output=True,text=True);ok=cp.returncode==0;detail=cp.stdout
  (H/f'FI{n}_relations.log').write_text(cp.stdout+cp.stderr)
 else:
  with(H/f'FI{n}_prefix.log').open('w')as f:cp=subprocess.run([str(W/'check_prefixes'),str(p6)],stdout=f,stderr=subprocess.STDOUT)
  detail=(H/f'FI{n}_prefix.log').read_text();mm=re.search(r'checked=(\d+)',detail);ok=cp.returncode==0 and mm and int(mm[1])==expected(i,d,6)
 out={'N':n,'status':'PASS'if ok and not fail else'FAIL','degree':d,'rows_cap6':len(rr),'rank_cap6':rank,'kernel_dimension':len(rels),'exceptional_counts':stats,'exceptional_failures':fail,'normalized_tuples_cap6':expected(i,d,6),'detail':detail[-250:]}
 (H/f'FI{n}_verified.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:out=list(ex.map(one,Ns))
(W/'formal_immersion.json').write_text(json.dumps({'status':'PASS'if all(v['status']=='PASS'for v in out)else'FAIL','results':out},indent=2)+'\n')
