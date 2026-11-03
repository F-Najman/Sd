from pathlib import Path
import json,math,re
from fractions import Fraction
from sage.all import prime_range
W=Path(__file__).resolve().parent;B=W.parents[1];s=(B/'work/audit11/derickx_stoll_table2.txt').read_text();pp=re.findall(r'(?<![A-Za-z])p&([^\\]+)',s);oo=re.findall(r'\\ord\(\\chi\)&([^\\]+)',s);st={}
for ps,os in zip(pp,oo):
 ps=[int(v)for v in ps.split('&')if v.strip()];os=[math.lcm(*map(int,v.split(',')))for v in os.split('&')if v.strip()];assert len(ps)==len(os);st.update(zip(ps,os))
assert len(st)==74;mid=[]
for p in map(int,prime_range(149,100000)):
 t=st.get(p,1);h=(p-1)//(2*t);assert(p-1)%(2*t)==0 and 12%h!=0 and p*p>Fraction(2**19,325)*12+1;mid.append({'p':p,'strangeness':t,'kernel_order':h})
small=[]
for p in[113,127,131,137,139]:
 assert p not in st and Fraction(325*(p*p-1),65536)>60
 o=next(k for k in range(1,p)if pow(2,k,p)in[1,p-1]);assert all(12%(o//d)!=0 for d in[1,2,3]if o%d==0)
 small.append({'p':p,'diamond2_order':o,'gonality_lower_bound':str(Fraction(325*(p*p-1),65536))})
data={'status':'PASS','degree':12,'midrange':mid,'small_global':small};assert data==json.loads((W/'published_prime_bound.json').read_text());print('S12_PUBLISHED_PRIME_EXCLUSIONS_VERIFIED',len(mid),len(small))
