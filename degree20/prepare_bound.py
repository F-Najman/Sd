from pathlib import Path
import math,json,re,hashlib
from fractions import Fraction
from sage.all import prime_range,matrix,GF,factor,divisors,valuation
W=Path(__file__).resolve().parent;B=W.parents[1];d=20;m=40;cap=525313
for M in map(int,prime_range(181,601)):
 data=[];bad=0
 for u in range(1,M):
  rows=[sum((int(n*a%M>M//2)^int(n*u*pow(a,-1,M)%M>M//2))<<(a-1)for a in range(1,M))for n in range(1,m+1)];piv={}
  for z in rows:
   while z:
    k=z.bit_length()-1
    if k in piv:z^=piv[k]
    else:piv[k]=z;break
  bad+=len(piv)!=m;data.append({'u':u,'rows':list(map(hex,rows))})
 print('S20_DYADIC_SEARCH',M,'bad',bad,'cutoff',2*m*M,flush=True)
 if not bad:break
assert not bad
for v in data:assert matrix(GF(2),[[int(z,16)>>j&1 for j in range(M-1)]for z in v['rows']]).rank()==m
(W/'dyadic_jets.json').write_text(json.dumps({'status':'PASS','degree':d,'m':m,'M':M,'p_cutoff':2*m*M,'classes':data},indent=2)+'\n')
st={};ps=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if' p&'in line:ps=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif'\\ord(\\chi)&'in line:
  oo=[math.lcm(*map(int,v.split(',')))for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(ps)==len(oo);st.update(zip(ps,oo))
assert len(st)==74
lower=list(map(int,prime_range(2,48)))+[61]
cm=set(int(p)for dd in divisors(d)if dd%2==0 for p in[2*dd+1,3*dd+1])
assert sorted(p for p in cm if p>47)==[61]
exc=[];local=[]
for p in map(int,prime_range(53,100000)):
 if p in lower:continue
 t=st.get(p,1);h=(p-1)//(2*t);reason=None
 if p not in cm and p*p>Fraction(2**19,325)*d+1 and d%h:reason='Corollary7.5'
 elif p not in st:
  for ell in[2,3]:
   if ell==2 and p>157:continue
   if Fraction(325*(p*p-1),65536)<=(2*ell+1)*d:continue
   o=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1])
   if all(d%(o//a)for a in[1,2,3]if o%a==0):reason=f'Proposition4.1 ell={ell}';break
 if reason:exc.append({'p':p,'strangeness':t,'reason':reason})
 else:local.append(p)
ss={18:[261121,261633,262145,262657,263169],19:[523265,524289,525313],20:[1046529,1047553,1048577,1049601,1050625]}
large=[];dyadic=[]
for p in map(int,prime_range(100000,cap+1)):
 good=False
 for f in[18,19,20]:
  q=2**f;s=math.isqrt(4*q);lo=(q+1-s+p-1)//p;hi=(q+1+s)//p
  if lo+(lo%2)<=hi:good=True
 good|=any(x%p==0 for vals in ss.values()for x in vals)
 toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,d+1))
 if good or toric:large.append(p)
 else:dyadic.append(p)
known={};proofs={}
for oldd in[11,12,18]:
 folder=B/f'work/degree{oldd}/large_orders'
 if not folder.exists():continue
 for fp in folder.glob('p*_n*.log'):
  mt=re.fullmatch(r'p(\d+)_n(\d+)\.log',fp.name)
  if not mt:continue
  p,n=map(int,mt.groups())
  if p not in large:continue
  s=fp.read_text()
  if f'S{oldd}_SELECTED_CHARACTER_NONSTRANGE p={p} order={n} 'in s and'rigorously_verified=true'in s and not any(z in s for z in['Runtime error','User error','Assertion failed','System Error']):known.setdefault(p,set()).add(n);proofs[(p,n)]={'kind':'native_log','path':str(fp),'sha256':hashlib.sha256(fp.read_bytes()).hexdigest()}
parent=W.parent/'degree19';a=json.loads((parent/'large_verified.json').read_text());assert a['status']=='PASS'
for z in a['results']:
 p,n=z['p'],z['order']
 if p not in large or z['inherited']:continue
 fp=parent/'large_orders'/f'p{p}_n{n}.json'
 known.setdefault(p,set()).add(n);proofs[p,n]={'kind':'pade','path':str(fp),'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'sequence_sha256':z['sequence_sha256']}
selected=[];jobs=[];reused=[]
for p in large:
 mm=(p-1)//2;options=[]
 for r,v in factor(mm):
  r,v=int(r),int(v);w=int(valuation(d,r))
  if v<=w:continue
  orders=[int(n)for n in divisors(mm)if n%(r**(v-w))==0];missing=[n for n in orders if n not in known.get(p,set())]
  options.append((len(missing),len(orders),-r,r,v,w,orders,missing))
 assert options,p
 _,_,_,r,v,w,orders,missing=min(options);selected.append({'p':p,'r':r,'valuation_m':v,'valuation_degree':w,'threshold':v-w,'orders':orders,'new_orders':missing})
 for n in orders:
  if n in missing:jobs.append({'p':p,'order':n})
  else:reused.append({'p':p,'order':n,**proofs[(p,n)]})
out={'status':'DYADIC_AND_PUBLISHED_REDUCTIONS_COMPLETE','degree':d,'cap':cap,'M':M,'coefficient_rank':m,'lower_candidates':lower,'CM_possible_primes':sorted(cm),'local_levels':local,'excluded':exc,'large_screen_primes':large,'large_dyadic_excluded':dyadic,'supersingular_orders':ss}
(W/'global_bound.json').write_text(json.dumps(out,indent=2)+'\n');(W/'large_selected_orders.json').write_text(json.dumps({'degree':d,'primes':selected,'jobs':jobs,'reused':reused},indent=2)+'\n');print('S20_SMALL_LEVELS',local,flush=True);print('S20_LARGE_PRIMES',len(large),'selected_characters',len(jobs)+len(reused),'new',len(jobs),'reused',len(reused),flush=True)
