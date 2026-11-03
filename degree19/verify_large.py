from pathlib import Path
import json,hashlib,ast,re,time,sys
from sage.all import GF,PolynomialRing,divisors,valuation,is_prime
W=Path(__file__).resolve().parent;J=W/'large_orders';sel=json.loads((W/'large_selected_orders.json').read_text());required={(r['p'],n)for r in sel['primes']for n in r['orders']};fresh={(r['p'],r['order'])for r in sel['jobs']};reused={(r['p'],r['order']):r for r in sel['reused']};assert len(fresh)==592 and len(reused)==555 and fresh.isdisjoint(reused)and fresh|set(reused)==required
for r in sel['primes']:
 p,ell,v,w,th=[r[k]for k in['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2;assert is_prime(p)and is_prime(ell)and valuation(m,ell)==v and valuation(19,ell)==w and th==v-w>0;assert [int(n)for n in divisors(m)if n%(ell**th)==0]==r['orders']
def parse(s,k):return ast.literal_eval(re.search(r'\b'+k+r':=(.*?);',s,re.S)[1])
done=[];missing=[]
for p,n in sorted(required):
 if(p,n)in reused:
  r=reused[p,n];fp=Path(r['path']);assert hashlib.sha256(fp.read_bytes()).hexdigest()==r['sha256'];s=fp.read_text();assert re.search(r'S(?:11|12|18)_SELECTED_CHARACTER_NONSTRANGE p='+str(p)+' order='+str(n)+r' .*rigorously_verified=true',s)and not any(e in s for e in['Runtime error','User error','Assertion failed','Traceback']);done.append({'p':p,'order':n,'inherited':True,'log_sha256':r['sha256']});continue
 stem=f'p{p}_n{n}';mf=J/f'{stem}.json';cf=J/f'{stem}_independent_pade.json';sf=J/f'{stem}_sequence.m'
 if not all(q.exists()for q in[mf,cf,sf]):missing.append([p,n]);continue
 a=json.loads(mf.read_text());c=json.loads(cf.read_text());assert a['status']=='PASS';s=sf.read_text();sha=hashlib.sha256(sf.read_bytes()).hexdigest();assert a['sequence_sha256']==c['sequence_sha256']==sha;q=parse(s,'q');k=parse(s,'dimension');seq=parse(s,'sequence');assert parse(s,'linear_complexity')==k==c['complexity']==c['dimension']and len(seq)==2*k and c['p']==p and c['order']==n and c['q']==q and is_prime(q)and(q-1)%(p-1)==0
 R=PolynomialRing(GF(q),'x');x=R.gen();C=R(c['C']);A=R(c['A']);assert C[0]==1 and C.degree()<=k and A.degree()<k and max(C.degree(),A.degree()+1)==k and C.gcd(A)==1 and(C*R(seq)-A)%(x**(2*k))==0 and C==R(parse(s,'recurrence'))
 assert(k+2)*(q-1)**2<=2**64-1
 for suffix,marker in[('_sparse.log',f'S19_SPARSE_EXPORT_COMPLETE p={p} order={n} q={q} dimension={k} '),('_cpp.log',f'S19_CPP_KRYLOV_COMPLETE q={q} ambient_dimension={k+2} dimension={k} '),('_bm.log',f'S19_CPP_LINEAR_COMPLEXITY_CERTIFIED dimension={k} q={q}')]:
  ss=(J/f'{stem}{suffix}').read_text();assert marker in ss and not any(e in ss for e in['Runtime error','User error','Assertion failed','Traceback'])
 done.append({'p':p,'order':n,'inherited':False,'dimension':k,'q':q,'sequence_sha256':sha})
out={'status':'PASS'if not missing else'PARTIAL','required':len(required),'verified':len(done),'missing':missing,'results':done};(W/'large_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_LARGE_COVERAGE',out['status'],len(done),'/',len(required),'missing',len(missing),flush=True)
if '--available-only'not in sys.argv:assert not missing
