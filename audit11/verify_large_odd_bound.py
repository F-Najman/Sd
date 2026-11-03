"""Prime bound using only odd-characteristic formal immersion criteria.

The argument is explained in outputs/S11_proof.txt. No characteristic-2
winding-quotient cotangent assertion is used here.
"""
from pathlib import Path
import json,math,re,sys
from fractions import Fraction
from sage.all import GF,matrix,prime_range,divisors,is_prime
W=Path(__file__).resolve().parent
D=11;CAP=177148+math.isqrt(3*486**2);assert CAP==177989
fi=[]
for ell,M in[(3,53),(5,73)]:
 cases=[]
 for u in range(1,M):
  rows=[[int(n*a%M>M//2)-int(n*u*pow(a,-1,M)%M>M//2)for a in range(1,M)]for n in range(1,D+1)]
  assert matrix(GF(ell),rows).rank()==D
  cases.append({'u':u,'rank':D,'rows':rows})
 fi.append({'ell':ell,'modulus':M,'formal_immersion_cutoff':2*D*M,'matrices':cases})
def admissible(p,ell):
 witnesses=[]
 for e in range(1,D+1):
  q=ell**e
  if (q-1)%p==0 or(q+1)%p==0:witnesses.append({'residue_degree':e,'kind':'toric root of unity'})
  h=math.isqrt(4*q);lo=(q+1-h+p-1)//p;hi=(q+1+h)//p
  if lo<=hi:witnesses.append({'residue_degree':e,'kind':'Hasse interval','multiples':[lo,hi]})
 return witnesses
large=[];both=[];excluded=[]
for p in map(int,prime_range(100001,CAP+1)):
 a,b=admissible(p,3),admissible(p,5)
 if a and b:both.append(p)
 else:excluded.append({'p':p,'ell':3 if not a else 5})
assert len(excluded)+len(both)==6567 and len(both)==45
# In characteristic 3 supersingular j is 0: its Hasse invariant is the
# x^2 coefficient of y^2=x^3+a2*x^2+a4*x+a6, and j=a2^6/Delta.
# Every j=0 twist over F_(3^11) was enumerated by Magma.
ss=(W/'supersingular3.log').read_text();assert 'twists=4 group_orders=[ 176419, 177148, 177877 ]'in ss
ss_cards={176419,177148,177877};remaining=[];ss_excluded=[]
for p in both:
 assert p>=(3**11+1-math.isqrt(4*3**11)) and not any((3**e-1)%p==0 or(3**e+1)%p==0 for e in range(1,12))
 if p%3==1 and p not in ss_cards:ss_excluded.append(p)
 else:remaining.append(p)
selected=json.loads((W/'large_selected_orders.json').read_text());assert sorted(remaining)==sorted(z['p']for z in selected['primes'])and len(remaining)==21 and len(ss_excluded)==24
out={'degree':11,'oesterle_integer_cap':CAP,'odd_characteristic_formal_immersion_certificates':fi,'hasse_or_toric_excluded':excluded,'hasse_filter_survivors':both,'supersingular_excluded':ss_excluded,'selected_character_primes':remaining,'status':'ODD-CHARACTERISTIC FILTER VERIFIED'}
(W/'large_odd_filter_verified.json').write_text(json.dumps(out,indent=2)+'\n')
print('S11_ODD_CHARACTERISTIC_FILTER_PASS',len(excluded),'Hasse/toric exclusions;',len(ss_excluded),'supersingular exclusions;',len(remaining),'selected primes',flush=True)
if '--prepare-only'in sys.argv:sys.exit(0)
batch=json.loads((W/'large_orders/all_results.json').read_text());assert batch['status']=='PASS'and batch['characters']==73
done={(r['p'],r['order']):r for r in batch['results']};assert len(done)==73
for rec in selected['primes']:
 p,r,v=rec['p'],rec['omitted_prime'],rec['power'];m=(p-1)//2
 assert is_prime(r)and r!=11 and m%(r**v)==0 and m%(r**(v+1))!=0
 orders=[int(n)for n in divisors(m)if n%(r**v)==0];assert orders==rec['orders']
 for n in orders:
  assert done[p,n]['status']=='PASS'
  s=(W/f'large_orders/p{p}_n{n}.log').read_text()
  assert f'S11_SELECTED_CHARACTER_NONSTRANGE p={p} order={n} 'in s and not any(x in s for x in['Runtime error','User error','Traceback'])
# Published Table 2 covers every prime below 100000.
s=(W/'derickx_stoll_table2.txt').read_text();pp=re.findall(r'(?<![A-Za-z])p&([^\\]+)',s);oo=re.findall(r'\\ord\(\\chi\)&([^\\]+)',s);st={}
for ps,os in zip(pp,oo):
 ps=[int(v)for v in ps.split('&')if v.strip()];os=[math.lcm(*map(int,v.split(',')))for v in os.split('&')if v.strip()];assert len(ps)==len(os);st.update(zip(ps,os))
assert len(st)==74;mid=[]
for p in map(int,prime_range(137,100000)):
 s=st.get(p,1);h=(p-1)//(2*s);assert(p-1)%(2*s)==0 and 11%h!=0 and p*p>Fraction(2**19,325)*11+1
 mid.append({'p':p,'strangeness':s,'kernel_order':h})
small=[]
for p in[107,109,113,127,131]:
 assert p not in st and Fraction(325*(p*p-1),65536)>55
 o=next(k for k in range(1,p)if pow(2,k,p)in[1,p-1]);assert all(11%(o//d)!=0 for d in[1,2,3]if o%d==0)
 small.append({'p':p,'diamond2_order':o,'gonality_lower_bound':str(Fraction(325*(p*p-1),65536))})
out.update(status='PASS',proved_prime_upper_bound=103,selected_character_count=73,selected_character_omissions=selected['primes'],midrange_exclusions=mid,small_global_exclusions=small)
(W/'prime_bound.json').write_text(json.dumps(out,indent=2)+'\n')
print('S11_UNCONDITIONAL_PRIME_BOUND_PASS p<=103 published_table_primes',len(mid),'new_selected_characters73')
