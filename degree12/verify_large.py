"""Verify all required character orders, including coprime Pade certificates."""
from pathlib import Path
import ast,hashlib,json,re,sys,time
from sage.all import GF,PolynomialRing,divisors,factor,is_prime
W=Path(__file__).resolve().parent;B=W.parents[1];J=W/'large_orders';old=B/'work/independent_audit/global_fi/large73';sel=json.loads((W/'large_selected_orders.json').read_text());required={(r['p'],n)for r in sel['primes']for n in r['orders']};fresh={(r['p'],r['order'])for r in sel['jobs']};reused={(r['p'],r['order'])for r in sel['reused']};assert len(fresh)==603 and len(reused)==53 and fresh.isdisjoint(reused)and fresh|reused==required
for rec in sel['primes']:
 p,r,a,b,th=map(int,[rec[k]for k in ['p','omitted_prime','m_valuation','degree_valuation','order_threshold']]);m=(p-1)//2;assert is_prime(p)and is_prime(r)and m==rec['m'];va=dict(factor(m))[r];vb=dict(factor(12)).get(r,0);assert a==va>b==vb and th==r**(a-b);assert list(map(int,[n for n in divisors(m)if n%th==0]))==rec['orders']
def parse(s,key):return ast.literal_eval(re.search(r'\b'+key+r':=(.*?);',s,re.S)[1])
clean_required=json.loads((W/'clean_regeneration_required.json').read_text())['jobs'];clean_keys={(r['p'],r['order'])for r in clean_required};clean_file=W/'scheduler_cleanup.json';clean_records={}
if clean_file.exists():
 cr=json.loads(clean_file.read_text());assert cr['status']=='PASS'and cr['isolated_regeneration']and cr['all_previous_numerical_stages_exited_before_regeneration'];clean_records={(r['p'],r['order']):r for r in cr['jobs']};assert set(clean_records)==clean_keys and len(clean_records)==20
done=[];missing=[];tt=time.monotonic()
for p,n in sorted(required):
 if(p,n)in clean_keys and(p,n)not in clean_records:missing.append([p,n]);continue
 h=J if(p,n)in fresh else old;stem=f'p{p}_n{n}';seqfile=h/f'{stem}_sequence.m';cf=h/f'{stem}_independent_pade.json';mf=h/f'{stem}.json'
 if not all(f.exists()for f in[seqfile,cf,mf]):missing.append([p,n]);continue
 state=json.loads(mf.read_text());assert state['status']=='PASS',(p,n,state);c=json.loads(cf.read_text());s=seqfile.read_text();q=parse(s,'q');k=parse(s,'dimension');ss=parse(s,'sequence');assert parse(s,'linear_complexity')==k and len(ss)==2*k;assert is_prime(q)and q>p and(q-1)%(p-1)==0
 sha=hashlib.sha256(seqfile.read_bytes()).hexdigest();assert c['sequence_sha256']==sha and c['p']==p and c['order']==n and c['q']==q and c['dimension']==c['complexity']==k
 if(p,n)in clean_records:assert clean_records[p,n]['sequence_sha256']==sha and clean_records[p,n]['pade_certificate_sha256']==hashlib.sha256(cf.read_bytes()).hexdigest()
 if 'sequence_sha256'in state:assert state['sequence_sha256']==sha
 R=PolynomialRing(GF(q),'x');x=R.gen();C=R(c['C']);A=R(c['A']);assert C[0]==1 and C.degree()<=k and A.degree()<k and max(C.degree(),A.degree()+1)==k;assert C.gcd(A)==1 and(C*R(ss)-A)%(x**(2*k))==0;assert C==R(parse(s,'recurrence'))
 if 'C++'in state.get('method',''):
  log=(h/f'{stem}_sparse.log').read_text();assert f'S12_SPARSE_EXPORT_COMPLETE p={p} order={n} q={q} dimension={k} 'in log
  assert (k+2)*(q-1)**2<2**64
  for suffix in ['_sparse.log','_cpp.log','_bm.log']:
   assert not any(err in(h/f'{stem}{suffix}').read_text()for err in ['Runtime error','User error','Assertion failed','Traceback'])
  assert f'S12_CPP_KRYLOV_COMPLETE q={q} ambient_dimension={k+2} dimension={k} 'in(h/f'{stem}_cpp.log').read_text()and'native_prefix_checked=64'in(h/f'{stem}_cpp.log').read_text()
  assert f'S12_CPP_LINEAR_COMPLEXITY_CERTIFIED dimension={k} q={q}'in(h/f'{stem}_bm.log').read_text()
 else:
  log=(h/f'{stem}.log').read_text();assert re.search(r'S(?:11|12)_SELECTED_CHARACTER_NONSTRANGE p='+str(p)+r' order='+str(n)+r' ',log)
  assert not any(err in log for err in ['Runtime error','User error','Assertion failed','Traceback'])
 done.append({'p':p,'order':n,'dimension':k,'q':q,'reused':(p,n)in reused,'sequence_sha256':sha,'pade_certificate_sha256':hashlib.sha256(cf.read_bytes()).hexdigest()})
out={'status':'PASS'if not missing else'PARTIAL','required_characters':len(required),'verified_characters':len(done),'pending_characters':len(missing),'missing':missing,'results':done,'seconds':time.monotonic()-tt};(W/'large_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S12_CHARACTER_COVERAGE',out['status'],len(done),'/',len(required),'pending',len(missing),'seconds',out['seconds'],flush=True)
if '--available-only'not in sys.argv:assert not missing,missing
