from pathlib import Path
import json
from sage.all import PolynomialRing,QQ,cyclotomic_polynomial
W=Path(__file__).resolve().parent;R=PolynomialRing(QQ,'x');x=R.gen();checks=[]
for n,o in[(61,6),(97,12),(101,10)]:
 a=json.load(open(W/f'full{n}/sieve.json'));items=[('primary',a['alpha_coefficients'])]+([('alternative',a['alternative_alpha_coefficients'])]if n==97 else[])
 for name,cs in items:
  p=sum(QQ(v)*x**int(k)for k,v in cs.items());assert p(1)==0 and p%R(cyclotomic_polynomial(o))==0;checks.append({'p':n,'kind':name,'polynomial':str(p),'character_order':o,'status':'PASS'})
(W/'operator_annihilation_verified.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2)+'\n');print('S17_ALL_OPERATOR_ANNIHILATIONS_PASS',flush=True)
