from pathlib import Path
import subprocess,concurrent.futures,json,re,time
W=Path(__file__).resolve().parent;B=W.parents[1];S=W;H=W/'FI';H.mkdir(exist_ok=True)
levels=[37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
combined={41:(20,'2,3,6','3,5'),61:(15,'2,3,5','3,5,7'),67:(11,'2,3,5','3,5')}
def expected(ind,d):
 z=0
 for first in range(1,d+1):
  cap=min(first,d//2);a=[1]+[0]*d
  for _ in range(ind-1):a=[sum(a[t-k]for k in range(min(t,cap)+1))for t in range(d+1)]
  z+=a[d-first]
 return z
def run(N):
 tt=time.monotonic();stem=f'FI{N}';out=H/f'{stem}.txt'
 if N in combined:
  ind,tn,q=combined[N];cmd=['magma','-b',f'P:={N}',f'Ind:={ind}',f'Tn:={tn}',f'Q:={q}',f'Out:={out}',str(S/'export_combined_FI.m')]
 else:
  ss=(H/f'FI{N}_export.log').read_text();ma=re.search(r'index=(\d+) Tn=(\d+) q=(\d+)',ss);ind,tn,q=map(int,ma.groups());cmd=['magma','-b',f'P:={N}',f'Ind:={ind}',f'Tn:={tn}',f'Q:={q}',f'Out:={out}',str(S/'export_FI.m')]
 with(H/f'{stem}_export.log').open('w')as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0 and'DECIC_FI_EXPORT_COMPLETE'in(H/f'{stem}_export.log').read_text(),N
 with(H/f'{stem}_compression.log').open('w')as f:r=subprocess.run(['python',str(W/'compress_FI.py'),str(out)],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,N
 with(H/f'{stem}_prefix.log').open('w')as f:r=subprocess.run([str(W/'check_prefixes'),str(out.with_suffix('.compressed.txt'))],stdout=f,stderr=subprocess.STDOUT)
 ss=(H/f'{stem}_prefix.log').read_text();assert r.returncode==0 and'status=PASS'in ss,N;num=int(re.search(r'checked=(\d+)',ss)[1]);assert num==expected(ind,11),(N,num,expected(ind,11))
 rec={'N':N,'index':ind,'checked':num,'independent_expected':num,'status':'PASS','elapsed':time.monotonic()-tt};print(rec,flush=True);return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(run,levels))
(W/'formal_immersion.json').write_text(json.dumps({'status':'PASS','results':rs,'total_checked':sum(r['checked']for r in rs)},indent=2)+'\n')
print('AUDIT_ALL_RATIONAL_CUSP_FORMAL_IMMERSIONS_COMPLETE',flush=True)
