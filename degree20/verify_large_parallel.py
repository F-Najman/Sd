"""Exact selected-character certificates and complete divisor families."""
from pathlib import Path
import json,hashlib,ast,re,sys,gzip
from sage.all import GF,PolynomialRing,divisors,valuation,is_prime
W=Path(__file__).resolve().parent;J=W/'large_orders';sel=json.loads((W/'large_selected_orders.json').read_text());required={(r['p'],n)for r in sel['primes']for n in r['orders']};fresh={(r['p'],r['order'])for r in sel['jobs']};reused={(r['p'],r['order']):r for r in sel['reused']}
assert len(fresh)==1951 and len(reused)==1069 and fresh.isdisjoint(reused)and fresh|set(reused)==required and len(required)==3020
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def uncompressed_sha(p):
 with gzip.open(p,'rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def parse(s,k):return ast.literal_eval(re.search(r'\b'+k+r':=(.*?);',s,re.S)[1])
for r in sel['primes']:
 p,ell,v,w,th=[r[k]for k in['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2
 assert is_prime(p)and is_prime(ell)and valuation(m,ell)==v and valuation(20,ell)==w and th==v-w>0
 assert [int(n)for n in divisors(m)if n%(ell**th)==0]==r['orders']
done=[];missing=[];parent=json.loads((W.parent/'degree19/large_verified.json').read_text());assert parent['status']=='PASS';parent_results={(r['p'],r['order']):r for r in parent['results']}
hybridsha=sha(W/'krylov_hybrid');assert hybridsha=='c7f3fe6412e499968c1f32b3e6846243160ba70e6bd32de491749257475b5294'
assert json.loads((W/'optimization/hybrid_full_replay_verified.json').read_text())['status']=='PASS'
def verify_one(task):
 p,n=task
 if(p,n)in reused:
  r=reused[p,n];fp=Path(r['path']);assert sha(fp)==r['sha256']
  if r['kind']=='native_log':
   s=fp.read_text();assert re.search(r'S(?:11|12|18)_SELECTED_CHARACTER_NONSTRANGE p='+str(p)+' order='+str(n)+r' .*rigorously_verified=true',s)and not any(e in s for e in['Runtime error','User error','Assertion failed','Traceback'])
  else:
   assert r['kind']=='pade';v=parent_results[p,n];assert not v['inherited']and v['sequence_sha256']==r['sequence_sha256'];a=json.loads(fp.read_text());assert a['status']=='PASS'and a['sequence_sha256']==r['sequence_sha256']
   assert sha(fp.parent/(fp.stem+'_sequence.m'))==r['sequence_sha256']
  return({'p':p,'order':n,'inherited':True,'kind':r['kind'],'certificate_sha256':r['sha256']})
 stem=f'p{p}_n{n}';mf=J/f'{stem}.json';cf=J/f'{stem}_independent_pade.json';sf=J/f'{stem}_sequence.m'
 if not all(z.exists()for z in [mf,cf,sf]):return {'missing':[p,n]}
 a=json.loads(mf.read_text());c=json.loads(cf.read_text());assert a['status']=='PASS';s=sf.read_text();h=sha(sf);assert a['sequence_sha256']==c['sequence_sha256']==h
 q=parse(s,'q');k=parse(s,'dimension');seq=parse(s,'sequence');assert parse(s,'linear_complexity')==k==c['complexity']==c['dimension']and len(seq)==2*k and c['p']==p and c['order']==n and c['q']==q and is_prime(q)and(q-1)%(p-1)==0
 R=PolynomialRing(GF(q),'x');x=R.gen();C=R(c['C']);A=R(c['A']);assert C[0]==1 and C.degree()<=k and A.degree()<k and max(C.degree(),A.degree()+1)==k and C.gcd(A)==1 and(C*R(seq)-A)%(x**(2*k))==0 and C==R(parse(s,'recurrence'))
 graph=a.get('cpp_implementation')=='raw_manin_graph_v1';ambient=k+2
 markers=[('_bm.log',f'S20_CPP_LINEAR_COMPLEXITY_CERTIFIED dimension={k} q={q}')]
 if graph:
  OPT=W/'optimization';implementation=json.loads((OPT/'fast_graph_implementation_verified.json').read_text());assert implementation['status']=='PASS'
  assert a['graph_source_sha256']==sha(OPT/'export_graph_fast.m')==implementation['fast_graph_source_sha256']
  assert a['preparer_binary_sha256']==sha(OPT/'prepare_graph')and a['preparer_source_sha256']==sha(OPT/'prepare_graph.cpp')
  assert a['native_prefix_source_sha256']==sha(OPT/'check_graph_prefix.m')and a['graph_verifier_source_sha256']==sha(OPT/'verify_graph.py')and a['cpp_binary_sha256']==sha(W/'krylov')
  gf=J/f'{stem}_graph.txt.gz';pf=J/f'{stem}_prepared.txt.gz';rf=J/f'{stem}_graph_rank.json';vf=J/f'{stem}_graph_verified.json'
  assert sha(gf)==a['graph_archive_sha256']and sha(pf)==a['prepared_archive_sha256']and sha(rf)==a['rank_certificate_sha256']and sha(vf)==a['graph_independent_certificate_sha256']
  v=json.loads(vf.read_text());r=json.loads(rf.read_text());ambient=a['ambient_dimension'];assert v['status']=='PASS'and(v['p'],v['order'],v['q'],v['generators'],v['cuspidal_dimension'])==(p,n,q,ambient,k)
  assert v['graph_sha256']==a['graph_sha256']==uncompressed_sha(gf)and v['prepared_sha256']==a['prepared_sha256']==uncompressed_sha(pf)
  assert v['rank_certificate_sha256']==sha(rf)and v['verifier_sha256']==sha(OPT/'verify_graph.py')and r['dimension']==v['full_dimension']==k+2 and r['relation_rank']==v['relation_rank']
  assert all(v[key]for key in ['all_functional_relations_verified','rank_lower_and_upper_certificates_verified','winding_vector_verified','all_prepared_operator_rows_identical'])
  markers += [('_graph.log',f'S20_MANIN_GRAPH_EXPORT_COMPLETE p={p} order={n} q={q} generators={ambient} '),('_graph_prep.log',f'S20_MANIN_GRAPH_PREPARED p={p} order={n} q={q} generators={ambient} '),('_graph_check.log',f'S20_GRAPH_INDEPENDENT_CERTIFICATE_PASS {p} {n} '),('_native_prefix.log',f'S20_GRAPH_NATIVE_PREFIX_PASS p={p} order={n} q={q} dimension={k} ambient_dimension={ambient} ')]
 else:markers.append(('_sparse.log',f'S20_SPARSE_EXPORT_COMPLETE p={p} order={n} q={q} dimension={k} '))
 assert ambient*(q-1)**2<=2**64-1
 markers.append(('_cpp.log',f'S20_CPP_KRYLOV_COMPLETE q={q} ambient_dimension={ambient} dimension={k} '))
 for suffix,marker in markers:
  ss=(J/f'{stem}{suffix}').read_text();assert marker in ss and not any(e in ss for e in['Runtime error','User error','Assertion failed','Traceback'])
 if a.get('cpp_implementation'):
  impl=a['cpp_implementation'];assert impl in ['hybrid_dense_rows_v1','legacy_csc','raw_manin_graph_v1']
  assert a['cpp_binary_sha256']==(hybridsha if impl=='hybrid_dense_rows_v1'else sha(W/'krylov'))
 return({'p':p,'order':n,'inherited':False,'dimension':k,'q':q,'sequence_sha256':h})

if __name__=='__main__':
 import concurrent.futures,time
 if '--probe'in sys.argv:
  t=time.monotonic();r=verify_one((524959,262479));print('S20_VERIFICATION_PROBE_PASS',r['p'],r['order'],'seconds',time.monotonic()-t,flush=True);raise SystemExit(0)
 done=[];missing=[];t=time.monotonic()
 with concurrent.futures.ProcessPoolExecutor(max_workers=8)as ex:
  for r in ex.map(verify_one,sorted(required),chunksize=1):
   if 'missing'in r:missing.append(r['missing'])
   else:done.append(r)
   if(len(done)+len(missing))%100==0:print('S20_FINAL_CHARACTER_REPLAY',len(done),'/3020','seconds',round(time.monotonic()-t,1),flush=True)
 out={'status':'PASS'if not missing else'PARTIAL','required':len(required),'verified':len(done),'missing':missing,'results':done,'verification_workers':8};(W/'large_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S20_LARGE_COVERAGE',out['status'],len(done),'/',len(required),'missing',len(missing),flush=True)
 assert not missing
