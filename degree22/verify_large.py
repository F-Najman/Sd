"""Complete selected-character families, integer provenance, and exact Pade replay."""
from pathlib import Path
import json,hashlib,ast,re,gzip,time
from functools import lru_cache
from sage.all import GF,PolynomialRing,divisors,valuation,is_prime
W=Path(__file__).resolve().parent;J=W/'large_orders';OPT=W/'optimization';sel=json.loads((W/'large_selected_orders.json').read_text());required={(r['p'],n)for r in sel['primes']for n in r['orders']};fresh={(r['p'],r['order'])for r in sel['jobs']};reused={(r['p'],r['order']):r for r in sel['reused']};assert len(fresh)==5018 and len(reused)==5047 and fresh.isdisjoint(reused)and fresh|set(reused)==required and len(required)==10065
for r in sel['primes']:
 p,ell,v,w,th=[r[k]for k in['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2;assert is_prime(p)and is_prime(ell)and valuation(m,ell)==v and valuation(22,ell)==w and th==v-w>0;assert [int(n)for n in divisors(m)if n%(ell**th)==0]==r['orders']
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
@lru_cache(None)
def code_sha(p):return sha(p)
def unsha(p):
 with gzip.open(p,'rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def parse(s,k):return ast.literal_eval(re.search(r'\b'+k+r':=(.*?);',s,re.S)[1])
def read(p):return json.loads(p.read_text())
def mark(p,needle):
 s=p.read_text();assert needle in s and not any(e in s for e in['Runtime error','User error','Assertion failed','Traceback']),str(p)
parents={}
for d in[19,20,21]:
 a=read(W.parent/f'degree{d}/large_verified.json');assert a['status']=='PASS';parents[d]={(r['p'],r['order']):r for r in a['results']}
for f in['packed_full_replay_verified.json','packed_fixtures_verified.json','free_full_replay_verified.json','free_fixtures_verified.json','fast_finish_verified.json','blocked_v2_verified.json','blocked_engine_verified.json']:
 assert read(OPT/f)['status']=='PASS'
impl=read(OPT/'fast_graph_implementation_verified.json');assert impl['status']=='PASS'and impl['fast_graph_source_sha256']==code_sha(OPT/'export_graph_fast.m')
bins={code_sha(W/b):b for b in['krylov_packed']}
def one(p,n):
 if(p,n)in reused:
  r=reused[p,n];fp=Path(r['path']);assert sha(fp)==r['sha256']
  if r['kind']=='native_log':mark(fp,re.search(r'S(?:11|12|18)_SELECTED_CHARACTER_NONSTRANGE p='+str(p)+' order='+str(n)+r' .*rigorously_verified=true',fp.read_text())[0])
  else:
   assert r['kind']=='pade';d=int(fp.parent.parent.name[6:]);v=parents[d][p,n];assert not v['inherited']and v['sequence_sha256']==r['sequence_sha256'];a=read(fp);assert a['status']=='PASS'and a['sequence_sha256']==r['sequence_sha256'];assert sha(fp.parent/(fp.stem+'_sequence.m'))==r['sequence_sha256']
  return{'p':p,'order':n,'inherited':True,'kind':r['kind'],'certificate_sha256':r['sha256']}
 stem=f'p{p}_n{n}';mf=J/f'{stem}.json';cf=J/f'{stem}_independent_pade.json';sf=J/f'{stem}_sequence.m'
 if not all(f.exists()for f in[mf,cf,sf]):return None
 a=read(mf);c=read(cf);assert a['status']=='PASS';s=sf.read_text();h=sha(sf);assert h==a['sequence_sha256']==c['sequence_sha256'];q=parse(s,'q');k=parse(s,'dimension');seq=parse(s,'sequence');assert parse(s,'linear_complexity')==k==c['complexity']==c['dimension']and len(seq)==2*k and(c['p'],c['order'],c['q'])==(p,n,q)and is_prime(q)and(q-1)%(p-1)==0 and q<2**32
 R=PolynomialRing(GF(q),'x');x=R.gen();C=R(c['C']);A=R(c['A']);assert C[0]==1 and C.degree()<=k and A.degree()<k and max(C.degree(),A.degree()+1)==k and C.gcd(A)==1 and(C*R(seq)-A)%(x**(2*k))==0 and C==R(parse(s,'recurrence'))
 assert a['graph_source_sha256']==code_sha(OPT/'export_graph_fast.m')and a['preparer_binary_sha256']==code_sha(OPT/'prepare_graph')and a['preparer_source_sha256']==code_sha(OPT/'prepare_graph.cpp')and a['native_prefix_source_sha256']==code_sha(OPT/'check_graph_prefix.m')and a['graph_verifier_source_sha256']==code_sha(OPT/'verify_graph.py')
 gf=J/f'{stem}_graph.txt.gz';pf=J/f'{stem}_prepared.txt.gz';rf=J/f'{stem}_graph_rank.json';vf=J/f'{stem}_graph_verified.json'
 assert sha(gf)==a['graph_archive_sha256']and sha(pf)==a['prepared_archive_sha256']and sha(rf)==a['rank_certificate_sha256']and sha(vf)==a['graph_independent_certificate_sha256'];v=read(vf);r=read(rf);ns=a['ambient_dimension'];assert v['status']=='PASS'and(v['p'],v['order'],v['q'],v['generators'],v['cuspidal_dimension'])==(p,n,q,ns,k)
 assert v['graph_sha256']==a['graph_sha256']==unsha(gf)and v['prepared_sha256']==a['prepared_sha256']==unsha(pf);assert v['rank_certificate_sha256']==sha(rf)and v['verifier_sha256']==code_sha(OPT/'verify_graph.py')and r['dimension']==v['full_dimension']==k+2 and r['relation_rank']==v['relation_rank'];assert all(v[t]for t in['all_functional_relations_verified','rank_lower_and_upper_certificates_verified','winding_vector_verified','all_prepared_operator_rows_identical'])
 binary=bins[a['cpp_binary_sha256']];assert a.get('cpp_binary_name',binary)==binary and a['cpp_source_sha256']==code_sha(W/(binary+'.cpp'));engine=a['cpp_implementation'];assert engine=='free_dual_graph_packed_v1'
 if engine=='free_dual_graph_packed_v1':
  assert binary=='krylov_packed';lf=J/f'{stem}_free.txt.gz';ff=J/f'{stem}_free_verified.json';assert sha(lf)==a['free_plan_archive_sha256']and unsha(lf)==a['free_plan_sha256']and sha(ff)==a['free_plan_verification_sha256']and a['free_plan_producer_sha256']==code_sha(OPT/'prepare_free.py')and a['free_plan_verifier_sha256']==code_sha(OPT/'verify_free.py');f=read(ff)
  assert f['status']=='PASS'and(f['p'],f['order'],f['q'],f['ambient_dimension'],f['dimension'],f['free_dimension'])==(p,n,q,ns,k,k+2)and f['free_plan_sha256']==a['free_plan_sha256']and f['graph_sha256']==a['graph_sha256']and f['prepared_sha256']==a['prepared_sha256']and f['rank_certificate_sha256']==sha(rf)and f['graph_verification_sha256']==sha(vf)and f['verifier_sha256']==code_sha(OPT/'verify_free.py');assert all(f[t]for t in['all_gauged_incidence_coefficients_checked','all_free_operator_entries_checked','forest_order_and_pivots_checked','initial_vector_and_winding_checked','full_one_step_operator_match']);mark(J/f'{stem}_cpp.log',f'S22_PACKED_GRAPH_KRYLOV_COMPLETE p={p} order={n} q={q} ambient_dimension={ns} dimension={k} free_dimension={k+2} ');mark(J/f'{stem}_free_check.log',f'S21_FREE_GRAPH_INDEPENDENT_PASS {p} {n} ')
 else:
  assert binary!='krylov_free'
  if binary=='krylov':assert ns*(q-1)**2<=2**64-1
  mark(J/f'{stem}_cpp.log',('S20_CPP_KRYLOV_COMPLETE'if binary=='krylov'else'S21_CPP_BLOCKED_KRYLOV_COMPLETE')+f' q={q} ambient_dimension={ns} dimension={k} ')
 if a.get('recurrence_engine')=='NTL_half_gcd':
  assert a['recurrence_source_sha256']==code_sha(W/'finish_fast.cpp')and a['recurrence_binary_sha256']==code_sha(W/'finish_fast')and a['fast_pade_sha256']==sha(J/f'{stem}_fast_pade.json');mark(J/f'{stem}_bm.log',f'S21_FAST_PADE_CERTIFIED dimension={k} q={q}')
 else:mark(J/f'{stem}_bm.log',f'S20_CPP_LINEAR_COMPLEXITY_CERTIFIED dimension={k} q={q}')
 for suffix,marker in[('_graph.log',f'S20_MANIN_GRAPH_EXPORT_COMPLETE p={p} order={n} q={q} generators={ns} '),('_graph_prep.log',f'S20_MANIN_GRAPH_PREPARED p={p} order={n} q={q} generators={ns} '),('_graph_check.log',f'S20_GRAPH_INDEPENDENT_CERTIFICATE_PASS {p} {n} '),('_native_prefix.log',f'S20_GRAPH_NATIVE_PREFIX_PASS p={p} order={n} q={q} dimension={k} ambient_dimension={ns} ')]:mark(J/f'{stem}{suffix}',marker)
 return{'p':p,'order':n,'inherited':False,'dimension':k,'q':q,'sequence_sha256':h,'independent_pade_sha256':sha(cf),'engine':engine,'binary':binary}
if __name__=='__main__':
 done={};start=time.monotonic()
 while len(done)<len(required):
  changed=False
  for p,n in sorted(required):
   if(p,n)in done:continue
   r=one(p,n)
   if r is None:continue
   done[p,n]=r;changed=True
   if len(done)%100==0:print('S22_LARGE_FULL_REPLAY',len(done),'/10065',round(time.monotonic()-start,1),flush=True)
  (W/'large_verification_progress.json').write_text(json.dumps({'verified':len(done),'required':len(required)},indent=2)+'\n')
  if not changed:time.sleep(20)
 (W/'large_verified.json').write_text(json.dumps({'status':'PASS','required':len(required),'verified':len(done),'missing':[],'results':[done[k]for k in sorted(done)]},indent=2)+'\n');print('S22_LARGE_COVERAGE_PASS',len(done),flush=True)
