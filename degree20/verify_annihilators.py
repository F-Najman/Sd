from pathlib import Path
import json
from sage.all import PolynomialRing,ZZ,cyclotomic_polynomial
W=Path(__file__).resolve().parent;B=W.parents[1];orders={};ps=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if ' p&'in line:ps=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif '\\ord(\\chi)&'in line:
  vals=[[int(t)for t in v.split(',')]for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(vals)==len(ps);orders.update(zip(ps,vals))
assert len(orders)==74 and orders[97]==[12]and orders[101]==[10]
R=PolynomialRing(ZZ,'x');x=R.gen();out=[];rankzero=json.loads((W/'rankzero_verified.json').read_text());assert rankzero['status']=='PASS'and{r['p']for r in rankzero['cases']}=={59,71}
for p in json.loads((W/'local_levels.json').read_text())['levels']:
 a=json.loads((W/f'full{p}/sieve.json').read_text());poly=sum((ZZ(v)*x**int(k)for k,v in a['alpha_coefficients'].items()),R.zero())
 if p in[59,71]:assert poly==1
 else:assert poly(1)==0
 for n in orders.get(p,[]):assert poly%R(cyclotomic_polynomial(n))==0
 out.append({'p':p,'positive_nontrivial_character_orders':orders.get(p,[]),'ordinary_annihilator':str(poly),'status':'PASS'})
for p in[151,163,167]:assert not orders.get(p,[])
assert json.loads((W/'sharp_finite_verified.json').read_text())['status']=='PASS'
(W/'annihilator_characters_verified.json').write_text(json.dumps({'status':'PASS','ordinary_operators':out,'global_nonstrange_primes':[151,163,167],'sharper_map_positive_orders':{'97':[12],'101':[10]},'table_used_only_below_100000':True},indent=2)+'\n');print('S20_ALL_ANNIHILATOR_CHARACTER_CONDITIONS_PASS',len(out),'local levels and3 global levels',flush=True)
