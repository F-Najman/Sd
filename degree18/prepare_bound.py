from pathlib import Path
import json,math,re
from fractions import Fraction
from sage.all import prime_range,matrix,GF,factor,divisors,valuation
W=Path(__file__).resolve().parent;B=W.parents[1];d=18;m=36;cap=263169
for M in map(int,prime_range(181,500)):
 data=[];bad=0
 for u in range(1,M):
  rows=[sum((int(n*a%M>M//2)^int(n*u*pow(a,-1,M)%M>M//2))<<(a-1)for a in range(1,M))for n in range(1,m+1)];piv={}
  for x in rows:
   while x:
    k=x.bit_length()-1
    if k in piv:x^=piv[k]
    else:piv[k]=x;break
  bad+=len(piv)!=m;data.append({'u':u,'rows':list(map(hex,rows))})
 print('S18_DYADIC_SEARCH',M,'bad',bad,'cutoff',2*m*M,flush=True)
 if not bad:break
assert not bad and 2*m*M<cap
for v in data:assert matrix(GF(2),[[int(row,16)>>j&1 for j in range(M-1)]for row in v['rows']]).rank()==m
(W/'dyadic_jets.json').write_text(json.dumps({'status':'PASS','m':m,'M':M,'p_cutoff':2*m*M,'classes':data},indent=2)+'\n')
s=(B/'work/audit11/derickx_stoll_table2.txt').read_text();st={}
for pp,oo in zip(re.findall(r'(?<![A-Za-z])p&([^\\]+)',s),re.findall(r'\\ord\(\\chi\)&([^\\]+)',s)):
 st.update(zip([int(v)for v in pp.split('&')if v.strip()],[math.lcm(*map(int,v.split(',')))for v in oo.split('&')if v.strip()]))
assert len(st)==74
exc=[];pending=[]
for p in map(int,prime_range(47,100000)):
 t=st.get(p,1);h=(p-1)//(2*t);why=None
 if p*p>Fraction(2**19,325)*d+1 and d%h:why='Corollary7.5'
 elif p not in st:
  for ell in[2,3]:
   if ell==2 and p>157:continue
   if Fraction(325*(p*p-1),65536)<=(2*ell+1)*d:continue
   o=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1])
   if all(d%(o//v)for v in[1,2,3]if o%v==0):why=f'Proposition4.1 ell={ell}';break
 if why:exc.append({'p':p,'reason':why,'strangeness':t})
 else:pending.append(p)
# Only degrees18 can give ordinary good reduction with p>100000.
# Its order is even, hence equals2p; exact supersingular orders and the
# identity-component possibilities are retained explicitly.
ssorders=[261121,261633,262145,262657,263169]
large=[];large_ex=[];jobs=[];selected=[]
for p in map(int,prime_range(100000,cap+1)):
 good=(261121<=2*p<=263169)or any(v%p==0 for v in ssorders)
 toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,19))
 if not good and not toric:large_ex.append(p);continue
 large.append(p);mm=(p-1)//2;opts=[]
 for r,v in factor(mm):
  r,v=int(r),int(v);w=int(valuation(d,r))
  if v<=w:continue
  threshold=v-w;orders=[int(n)for n in divisors(mm)if int(n)%(r**threshold)==0]
  opts.append((len(orders),-r,r,v,w,threshold,orders))
 assert opts,p
 _,_,r,v,w,threshold,orders=min(opts)
 selected.append({'p':p,'r':r,'valuation_m':v,'valuation_degree':w,'threshold':threshold,'orders':orders})
 jobs +=[{'p':p,'order':n}for n in orders]
out={'status':'DYADIC_AND_PUBLISHED_REDUCTIONS_COMPLETE','degree':d,'cap':cap,'M':M,'coefficient_rank':m,'excluded':exc,'local_levels':pending,'large_dyadic_excluded':large_ex,'large_screen_primes':large,'supersingular18_orders':ssorders}
(W/'global_bound.json').write_text(json.dumps(out,indent=2)+'\n');(W/'large_selected_orders.json').write_text(json.dumps({'degree':d,'primes':selected,'jobs':jobs},indent=2)+'\n');print('S18_SMALL_LEVELS',pending,flush=True);print('S18_LARGE_PRIMES',len(large),'characters',len(jobs),'exception',large[-1],flush=True)
