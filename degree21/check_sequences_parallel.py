"""Independent exact finite-sequence complexity check by polynomial Euclid.
If C*S=A modulo x^(2k), gcd(A,C)=1, C(0)=1, deg A<k, deg C<=k,
and max(deg A+1,deg C)=k, then no recurrence length<k exists:
for any such A'/C', deg(C'A-CA')<2k, so the congruence makes it zero;
coprimality forces a common polynomial multiple, contradicting degrees.
This avoids relying on Magma's BerlekampMassey implementation.
"""
from pathlib import Path
import json,re,ast,time,sys,hashlib
import concurrent.futures
from sage.all import GF,PolynomialRing
O=Path(__file__).resolve().parent;J=O/'large_orders';jobs=json.loads((O/'large_selected_orders.json').read_text())['jobs'];done={};start=time.monotonic()
def parse(text,name):return ast.literal_eval(re.search(r'\b'+name+r':=(.*?);',text,re.S)[1])
def check(job):
 p,n=job['p'],job['order'];stem=f'p{p}_n{n}';file=J/f'{stem}_sequence.m';text=file.read_text();q=parse(text,'q');k=parse(text,'dimension');L=parse(text,'linear_complexity');seq=parse(text,'sequence');magmaC=parse(text,'recurrence');assert len(seq)==2*k and L==k
 F=GF(q);R=PolynomialRing(F,'x');x=R.gen();S=R(seq);f0,f1=S,x**(2*k);s0,s1=R.one(),R.zero();steps=0;t=time.monotonic()
 while f1.degree()>=k:
  quotient,remainder=f0.quo_rem(f1);f0,f1=f1,remainder;s0,s1=s1,s0-quotient*s1;steps+=1
 assert s1[0]!=0
 C=s1/s1[0];A=f1/s1[0]
 assert C[0]==1 and C.degree()<=k and A.degree()<k
 assert (C*S-A)%(x**(2*k))==0
 assert C.gcd(A)==1
 complexity=max(int(C.degree()),int(A.degree())+1);assert complexity==k,(p,n,complexity,k)
 assert C==R(magmaC),(p,n,'Magma/Sage recurrence mismatch')
 # Retain the independently constructed coprime Pade certificate.
 cert={'p':p,'order':n,'q':q,'dimension':k,'complexity':complexity,'numerator_degree':int(A.degree()),'denominator_degree':int(C.degree()),'gcd_degree':0,'C':[int(a)for a in C.list()],'A':[int(a)for a in A.list()],'sequence_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'algorithm':'polynomial Euclid plus exact congruence/coprimality certificate','elapsed':time.monotonic()-t,'euclidean_steps':steps}
 cp=J/f'{stem}_independent_pade.json';tmp=cp.with_suffix('.json.tmp');tmp.write_text(json.dumps(cert,separators=(',',':'))+'\n');tmp.replace(cp);small={k:v for k,v in cert.items()if k not in['C','A']};print(small,flush=True);return small

def main():
 done={};inflight={};busy=set()
 for job in jobs:
  p,n=job['p'],job['order'];stem=f'p{p}_n{n}';cf=J/f'{stem}_independent_pade.json';sf=J/f'{stem}_sequence.m';mf=J/f'{stem}.json'
  if not all(f.exists()for f in[cf,sf,mf]):continue
  try:c=json.loads(cf.read_text());state=json.loads(mf.read_text())
  except json.JSONDecodeError:continue
  if state['status']=='PASS'and c['sequence_sha256']==hashlib.sha256(sf.read_bytes()).hexdigest():done[p,n]={k:v for k,v in c.items()if k not in['C','A']}
 print('S21_PADE_CACHE_VERIFIED',len(done),'parallel_workers4',flush=True)
 with concurrent.futures.ProcessPoolExecutor(max_workers=1)as ex:
  while len(done)<len(jobs):
   for job in jobs:
    key=job['p'],job['order'];mf=J/f'p{key[0]}_n{key[1]}.json'
    if key in done or key in busy or not mf.exists():continue
    state=json.loads(mf.read_text());assert state['status']=='PASS';busy.add(key);inflight[ex.submit(check,job)]=key
    if len(inflight)>=2:break
   if inflight:
    finished,_=concurrent.futures.wait(inflight,timeout=5,return_when=concurrent.futures.FIRST_COMPLETED)
    for f in finished:key=inflight.pop(f);done[key]=f.result();busy.remove(key)
   else:time.sleep(5)
 out={'status':'PASS','checked':len(done),'results':[done[(j['p'],j['order'])]for j in jobs],'elapsed':time.monotonic()-start,'workers':4};(O/'independent_sequence_results.json').write_text(json.dumps(out,indent=2)+'\n');print('S21_INDEPENDENT_SEQUENCE_COMPLEXITIES_COMPLETE',len(done),flush=True)
if __name__=='__main__':main()
