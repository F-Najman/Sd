from pathlib import Path
import json,math,re
from sage.all import prime_range,matrix,GF
from fractions import Fraction
W=Path(__file__).resolve().parent;B=W.parents[1];m=28
for M in map(int,prime_range(149,450)):
 data=[];bad=0
 for u in range(1,M):
  rows=[sum((int(n*a%M>M//2)^int(n*u*pow(a,-1,M)%M>M//2))<<(a-1)for a in range(1,M))for n in range(1,m+1)];piv={}
  for x in rows:
   while x:
    k=x.bit_length()-1
    if k in piv:x^=piv[k]
    else:piv[k]=x;break
  if len(piv)!=m:bad+=1
  data.append({'u':u,'rows':list(map(hex,rows))})
 print('S14_DYADIC_SEARCH',M,'bad',bad,'cutoff',2*m*M,flush=True)
 if not bad:break
assert not bad and 56*M<16641
for v in data:
 assert matrix(GF(2),[[int(row,16)>>j&1 for j in range(M-1)]for row in v['rows']]).rank()==m
(W/'dyadic_jets.json').write_text(json.dumps({'status':'PASS','m':m,'M':M,'p_cutoff':56*M,'classes':data},indent=2)+'\n')
s=(B/'work/audit11/derickx_stoll_table2.txt').read_text();ps=re.findall(r'(?<![A-Za-z])p&([^\\]+)',s);os=re.findall(r'\\ord\(\\chi\)&([^\\]+)',s);st={}
for pp,oo in zip(ps,os):st.update(zip([int(v)for v in pp.split('&')if v.strip()],[math.lcm(*map(int,v.split(',')))for v in oo.split('&')if v.strip()]))
exc=[];pending=[]
for p in map(int,prime_range(47,16642)):
 t=st.get(p,1);h=(p-1)//(2*t);why=None
 if p*p>Fraction(2**19,325)*14+1 and 14%h:why='Corollary 7.5'
 elif p not in st and Fraction(325*(p*p-1),65536)>70:
  o=next(k for k in range(1,p)if pow(2,k,p)in[1,p-1])
  if all(14%(o//v)for v in[1,2,3]if o%v==0):why='Proposition 4.1'
 if why:exc.append({'p':p,'reason':why,'strangeness':t})
 else:pending.append(p)
(W/'global_bound.json').write_text(json.dumps({'status':'PASS','degree':14,'cap':16641,'M':M,'coefficient_rank':m,'excluded':exc,'local_levels':pending},indent=2)+'\n');print('S14_BOUND_PASS cap=16641 local=',pending,flush=True)
