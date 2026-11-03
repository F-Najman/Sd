from pathlib import Path
import json,math,re,shutil
from sage.all import prime_range,divisors,factor,matrix,GF
W=Path(__file__).resolve().parent;B=W.parents[1];D=12;cap=730**2
ss={}
for ell,d,cs in re.findall(r'S12_SS ell=(\d+) d=(\d+) orders=(\[.*?\])',(W/'ss_orders.log').read_text()):ss[int(ell),int(d)]=json.loads(cs)
def witnesses(p,ell):
 out=[]
 for d in range(1,D+1):
  q=ell**d
  if(q-1)%p==0 or(q+1)%p==0:out.append([d,'toric'])
  rad=math.isqrt(4*q)
  for k in range(max(1,(q+1-rad+p-1)//p),(q+1+rad)//p+1):
   tr=q+1-k*p
   if tr%ell:out.append([d,'ordinary',k,tr])
   elif any(c%p==0 for c in ss.get((ell,d),[])):out.append([d,'supersingular',k,tr])
 return out
fams=[]
for ell,M in[(3,61),(5,59),(7,59)]:
 for u in range(1,M):assert matrix(GF(ell),[[int(n*a%M>M//2)-int(n*u*pow(a,-1,M)%M>M//2)for a in range(1,M)]for n in range(1,13)]).rank()==12
 fams.append({'ell':ell,'M':M,'rank':12,'unit_matrices':M-1})
ps=list(map(int,prime_range(100001,cap+1)));surv=[];exc=[]
for p in ps:
 ws={ell:witnesses(p,ell)for ell in[3,5,7]}
 if all(ws.values()):surv.append({'p':p,'witnesses':ws})
 else:exc.append({'p':p,'ell':next(ell for ell in[3,5,7]if not ws[ell])})
reuse={}
for p in (B/'work/audit11/large_orders').glob('p*_n*.log'):
 ma=re.match(r'p(\d+)_n(\d+)\.log',p.name)
 if ma and'S11_SELECTED_CHARACTER_NONSTRANGE'in p.read_text():reuse[int(ma[1]),int(ma[2])]=str(p)
selected=[];jobs=[];reused=[]
for dat in surv:
 p=dat['p'];m=(p-1)//2;ds=list(map(int,divisors(m)));choices=[]
 for r,a in factor(m):
  r,a=int(r),int(a);b=0;dd=D
  while dd%r==0:b+=1;dd//=r
  if a<=b:continue
  threshold=r**(a-b);orders=[n for n in ds if n%threshold==0];new=[n for n in orders if(p,n)not in reuse]
  choices.append((len(new),len(orders),r,a,b,threshold,orders))
 assert choices,p
 _,_,r,a,b,th,orders=min(choices)
 selected.append({'p':p,'m':m,'omitted_prime':r,'m_valuation':a,'degree_valuation':b,'order_threshold':th,'orders':orders})
 for n in orders:
  rec={'p':p,'order':n}
  if(p,n)in reuse:reused.append(rec|{'source':reuse[p,n]})
  else:jobs.append(rec)
(W/'large_selected_orders.json').write_text(json.dumps({'degree':D,'prime_count':len(surv),'primes':selected,'jobs':jobs,'reused':reused},indent=2)+'\n')
(W/'large_filter.json').write_text(json.dumps({'degree':D,'cap':cap,'FI_families':fams,'excluded':exc,'survivors':surv},indent=2)+'\n')
print('S12_LARGE_FILTER',len(ps),'primes',len(exc),'excluded',len(surv),'selected primes')
print('SELECTED_CHARACTERS',len(jobs),'new',len(reused),'reused','total',len(jobs)+len(reused))
print('PRIME_BINS', {k:sum(p['p']>=k for p in surv)for k in[100000,200000,300000,500000]})
print('HIGHEST',max(p['p']for p in surv))
