from pathlib import Path
import json,math,re
from sage.all import matrix,GF,prime_range
from fractions import Fraction
W=Path(__file__).resolve().parent;B=W.parents[1];a=json.loads((W/'dyadic_jets.json').read_text());M=a['M'];m=a['m'];assert (M,m)==(157,26)
for u in range(1,M):
 rows=[[int(n*v%M>M//2)^int(n*u*pow(v,-1,M)%M>M//2)for v in range(1,M)]for n in range(1,m+1)]
 assert matrix(GF(2),rows).rank()==m
 c=a['classes'][u-1];assert c['u']==u and [sum(v<<j for j,v in enumerate(row))for row in rows]==[int(v,16)for v in c['rows']]
cap=8193+math.isqrt(128**2*2);assert cap==8374 and 52*M<cap
s=(B/'work/audit11/derickx_stoll_table2.txt').read_text();pp=re.findall(r'(?<![A-Za-z])p&([^\\]+)',s);oo=re.findall(r'\\ord\(\\chi\)&([^\\]+)',s);st={}
for ps,os in zip(pp,oo):st.update(zip([int(v)for v in ps.split('&')if v.strip()],[math.lcm(*map(int,v.split(',')))for v in os.split('&')if v.strip()]))
assert len(st)==74
exc=[];pending=[]
for p in map(int,prime_range(41,cap+1)):
 t=st.get(p,1);h=(p-1)//(2*t);why=None
 if p*p>Fraction(2**19,325)*13+1 and 13%h!=0:why='Corollary 7.5'
 elif p not in st and Fraction(325*(p*p-1),65536)>65:
  o=next(k for k in range(1,p)if pow(2,k,p)in[1,p-1])
  if all(13%(o//v)!=0 for v in[1,2,3]if o%v==0):why='Proposition 4.1'
 if why:exc.append({'p':p,'reason':why,'strangeness':t})
 else:pending.append(p)
print('S13_DYADIC_BOUND_VERIFIED',cap,'matrices',M-1,'rank',m,'published_excluded',len(exc),'remaining',pending)
(W/'global_bound.json').write_text(json.dumps({'status':'PASS','degree':13,'cap':cap,'M':M,'coefficient_rank':m,'matrices_verified':M-1,'excluded':exc,'local_levels':pending},indent=2)+'\n')
