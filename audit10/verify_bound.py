"""Exact arithmetic for S(10) subset Primes(101).
Mathematical inputs: Oesterle bound; Derickx-Stoll (arXiv:2505.14109),
Theorem 3.3, Proposition 4.1, Remark 4.4, Proposition 5.2 and Corollary 7.5;
S(1), S(2), S(5) subset Primes(19). This is NOT a full determination.
"""
from pathlib import Path
from fractions import Fraction
import re,math,json
B=Path(__file__).resolve().parent
s=(B/'derickx_stoll_table2.txt').read_text();pp=re.findall(r'(?<![A-Za-z])p&([^\\]+)',s);oo=re.findall(r'\\ord\(\\chi\)&([^\\]+)',s);st={}
assert len(pp)==len(oo)==9
for ps,os in zip(pp,oo):
 ps=[int(v)for v in ps.split('&')if v.strip()];os=[math.lcm(*map(int,v.split(',')))for v in os.split('&')if v.strip()]
 assert len(ps)==len(os);st.update(zip(ps,os))
assert len(st)==74
cap=(3**5+1)**2; sieve=bytearray(b'\1')*(cap+1);sieve[:2]=b'\0\0'
for k in range(2,math.isqrt(cap)+1):
 if sieve[k]:sieve[k*k:cap+1:k]=b'\0'*len(range(k*k,cap+1,k))
primes=[p for p in range(cap+1)if sieve[p]]
C=Fraction(2**19,325);assert 131**2>C*10+1
large=[]
for p in primes:
 if p<131:continue
 strange=st.get(p,1);assert (p-1)%(2*strange)==0;h=(p-1)//(2*strange)
 assert p not in (2*10+1,3*10+1) and 10%h!=0
 large.append(dict(p=p,strangeness=strange,kernel_order=h))
small=[]
for p in [103,107,109,113,127]:
 assert p not in st
 lower=Fraction(325*(p*p-1),65536);assert lower>5*10
 a=2;o=1
 while pow(a,o,p)not in [1,p-1]:o+=1
 # The geometric diamond-orbit lengths can only be o,o/2,o/3.
 lengths=[o//f for f in [1,2,3]if o%f==0]
 assert all(10%length!=0 for length in lengths)
 small.append(dict(p=p,diamond=2,diamond_order=o,possible_geometric_orbit_lengths=lengths,gonality_lower_bound=str(lower),n=5))
assert {x['p']for x in large+small}=={p for p in primes if p>101}
r=dict(degree=10,proved_prime_upper_bound=101,known_occurring_primes=[2,3,5,7,11,13,17,19,23,29,31],unresolved_primes=[p for p in primes if 31<p<=101],oesterle_bound=cap,large_prime_exclusions=large,small_global_exclusions=small,status='PROVED BOUNDS; FULL CLASSIFICATION NOT ESTABLISHED')
(B/'prime_bound.json').write_text(json.dumps(r,indent=2)+'\n');print('DECIC_PRIME_BOUND_VERIFIED',json.dumps({k:v for k,v in r.items()if k!='large_prime_exclusions'}));print('large_exclusions',len(large))
