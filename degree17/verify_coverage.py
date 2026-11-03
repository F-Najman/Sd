from pathlib import Path
import json,re,sys,math,hashlib
from fractions import Fraction
from sage.all import prime_range
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127];lower=set(map(int,prime_range(2,44)))
def check(p,mark):
 s=p.read_text();assert mark in s and not any(v in s for v in['Runtime error','User error','Assertion failed','Traceback']),p
check(W/'verify_occurrences.log','S17_ALL_OCCURRENCES_COMPLETE');check(W/'verify_occurrence23.log','S17_ALL_OCCURRENCES_COMPLETE');check(W/'verify_occurrences41_43.log','S17_OCCURRENCES_41_43_COMPLETE');check(W/'bound_ss.log','S17_SUPERSINGULAR_BOUND_PASS');check(W/'cm_small.log','S17_CM_FROBENIUS_COMPLETE');check(W/'census_sources.log','S17_ALL_FINITE_SOURCE_ORBITS_COMPLETE');check(W/'stabilizers.log','S17_ALL_STABILIZERS_COMPLETE');check(B/'work/degree16/stabilizers.log','S16_ALL_STABILIZERS_COMPLETE')
rs={};pairlevels=[];ordinary=0;ordinary_mats=0;newpairs=0;pairmats=0;mixedmats=0
for n in ns:
 rs[n]=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');expected=[(j+1,v[0],v[5],v[4])for j,v in enumerate(rs[n])if v[6]]
 H=W/f'full{n}';a=json.load(open(H/'sieve.json'));assert a['source_orbits']==len(expected)and a['source_orbits']==a['nonprincipal']+len(a['exceptions'])
 ex=[(v['source'],v['degree'],v['orbit'])for v in a['exceptions']];assert ex==({113:[(2,8,7)],127:[(3,9,7)]}.get(n,[])),(n,ex)
 if n!=127:check(H/'stage2.log','AUDIT_ACTUAL_HECKE_JETS_COMPLETE')
 else:
  for start in range(1,222,25):check(H/f'chunk_{start}.log','AUDIT_ACTUAL_HECKE_JETS_COMPLETE')
  check(W/'run127.log','S17_ALL_127_CHUNKS_COMPLETE 215')
 meta=lit((H/'hecke_jets.m').read_text(),'SourceMetadata');assert sorted(meta)==sorted(expected)
 old=B/f'work/degree{14 if n==127 else 16}/full{n}/units_data.m';assert hashlib.sha256(old.read_bytes()).digest()==hashlib.sha256((H/'units_data.m').read_bytes()).digest()
 if n!=127:
  oldmd=lit((B/f'work/degree16/full{n}/hecke_jets.m').read_text(),'SourceMetadata');matches=re.findall(r'S17_OLD_ORBIT_REUSE_VERIFIED N=\d+ source=(\d+) old_source=(\d+) degree=(\d+)',(H/'stage2.log').read_text());assert len(matches)==len(oldmd)and len({int(v[1])for v in matches})==len(oldmd)
 fi=json.load(open(W/f'FI/FI{n}_verified.json'));assert not fi['exceptional_failures'];assert fi['status']=='PASS'if n!=103 else fi['status']=='FAIL'
 if n==97:
  assert {int(k):v for k,v in a['alpha_coefficients'].items()}=={12:1,0:-1}
  assert a['alternative_sources']==[2,3,41]and {int(k):v for k,v in a['alternative_alpha_coefficients'].items()}=={5:1,4:-1,3:-1,2:1,1:1,0:-1}
  assert json.load(open(W/'operator97_verified.json'))['status']=='PASS'
 ordinary+=a['source_orbits'];ordinary_mats+=a['nonprincipal']
 if min(v[1]for v in expected)<=8:
  pairlevels.append(n);pa=json.load(open(H/'pair_sieve.json'));rlist=pa['results'];assert len(rlist)==pa['nonprincipal']+len(pa['exceptions'])
  md=[v for v in meta if v[1]in[7,8,9,10]];tasks=set()
  for i,u in enumerate(md):
   for j in range(i,len(md)):
    v=md[j]
    if u[1]+v[1]not in[16,17]:continue
    for off in range(math.gcd(u[2],v[2])):
     if i==j and off>u[2]//2:continue
     tasks.add((u[0],v[0],off))
  assert {tuple(v['source'])for v in rlist}==tasks
  ex=pa['exceptions'];assert not ex if n!=113 else len(ex)==3 and all(v['source'][:2]==[2,2]for v in ex)
  newpairs+=len(rlist);pairmats+=pa['nonprincipal']
for n in[73,127]:
 a=json.load(open(W/f'full{n}/mixed_sieve.json'));assert not a['exceptions']if n==73 else [(v['source'],v['degree'],v['orbit'])for v in a['exceptions']]==[(3,9,7)];mixedmats+=a['nonprincipal']
for n,dd in[(59,14),(61,14),(67,14),(71,14),(73,14),(59,15),(61,15),(67,15),(71,15)]:
 a=json.load(open(B/f'work/degree{dd}/full{n}/pair_sieve.json'));assert not a['exceptions']
assert json.load(open(W/'FI/FI59_independent.json'))['status']=='PASS'
assert json.load(open(W/'operator_annihilation_verified.json'))['status']=='PASS'
aux=json.load(open(W/'auxiliary_verified.json'));assert aux['status']=='PASS'and aux['dyadic_ranks']==180
for n in[53,61]:assert json.load(open(W/f'relative{n}_verified.json'))['status']=='PASS'
assert json.load(open(W/'relative73_verified.json'))['status']=='PASS';assert json.load(open(W/'relative103_verified.json'))['status']=='PASS';assert json.load(open(W/'relative127_verified.json'))['status']=='PASS'
rank=json.load(open(W/'independent_rank_checks.json'));assert rank['status']=='PASS';nmat=sum(v['matrices']for v in rank['results']);assert nmat==ordinary_mats+pairmats+mixedmats+137+254
# Arithmetic inequalities used by the stabilizer exclusions.
for n,c,r,fac in[(73,5,9,1),(73,8,9,1),(73,2,9,1),(89,6,11,1),(97,1,4,2),(109,8,18,2),(109,5,18,2),(113,10,14,2),(113,3,14,2),(113,9,8,2),(113,1,8,2),(113,2,2,2),(127,10,7,2),(127,3,7,2),(127,8,9,2)]:assert Fraction(325*(n*n-1),65536)>fac*(17+c)
# All support-degree multisets, including repeated closed points.
ledger=[]
for n in ns:
 O=sorted({v[0]for v in rs[n]if v[6]});SS=sorted({v[0]for v in rs[n]if not v[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',v)for v in O]+[('SS',v)for v in SS]+([('NC',nc)]if nc<=17 else[])
 def classify(support):
  o=[v for k,v in support if k=='O'];other=[(k,v)for k,v in support if k!='O'];total=sum(v for k,v in support)
  if not support:return 'relative cusp immersion at103'if n==103 else'absolute cusp formal immersion'
  if len(o)==2:
   assert not other and total in[14,15,16,17]
   return 'ordinary pair obstruction or the113 order8 exception'
  if len(o)==1:
   if not other:return 'ordinary obstruction or the113/127 stabilizer exception'
   assert len(other)==1;kind,e=other[0];v=o[0]
   assert(n,kind,e,v)in{(73,'SS',6,x)for x in[7,10,11]}|{(73,'NC',9,7),(113,'SS',7,8)}|{(127,'NC',7,x)for x in[8,9,10]},(n,support)
   if n==127 and v==9:return 'partially relative immersion on degree9 and degree7 pullbacks with fixed cusp'
   return '113 involution and CM exclusion'if n==113 else'mixed principal-divisor obstruction'
  assert not o
  if n==53:assert support==[('SS',13)];return 'relative13 pullback plus fixed degree4 cusp divisor'
  if n==61:assert support==[('SS',15)];return 'relative5 pullback of cubic divisor plus fixed degree2 cusp divisor'
  if n==73:
   assert total in[6,9,12,15]
   return 'relative fixed-locus immersion'if total==6 else'order9 stabilizer and actual-Jacobian torsion control'
  allowed={89:[11],97:[16],109:[9,12],113:[7,14],127:[7,14]};assert n in allowed and total in allowed[n],(n,support)
  return 'proved stabilizer exclusion'
 def walk(start,left,support):
  reason=classify(support);ledger.append({'p':n,'support':support,'rational_cusp_complement':left,'reason':reason})
  for j in range(start,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],support+[types[j]])
 walk(0,17,[])
# Every prime in the complete dyadic range.
g=json.load(open(W/'global_bound.json'));assert(g['degree'],g['cap'],g['M'],g['coefficient_rank'])==(17,66049,181,34)
assert set(g['local_levels'])==set(ns)|{41,43,137,409,1021}
cases={p:'verified occurrence'for p in lower}
for v in g['excluded']:
 p=v['p'];reason=v['reason'];assert p not in cases
 if reason=='Corollary 7.5':assert p*p>Fraction(2**19,325)*17+1 and 17%((p-1)//(2*v['strangeness']))
 elif reason=='Proposition 4.1 ell=3':assert p==163 and Fraction(325*(p*p-1),65536)>7*17
 else:assert reason=='Proposition 4.1'and p<=157 and Fraction(325*(p*p-1),65536)>5*17
 cases[p]=reason
for n in ns:assert n not in cases;cases[n]='complete local exclusion at2'
cases[137]='order34 criterion and CM Frobenius exclusion';cases[409]=cases[1021]='order17 quotient and Mazur rational-isogeny theorem'
assert set(cases)==set(map(int,prime_range(2,66050)))
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':17,'S':sorted(lower),'proved_lower_bound':sorted(lower),'proved_upper_bound':sorted(lower),'unresolved_primes':[],'dyadic_bound':66049,'coefficient_rank':34,'dyadic_M':181,'audited_primes':len(cases),'complete_local_exclusions':len(ns),'ordinary_source_orbits':ordinary,'ordinary_nonprincipal':ordinary_mats,'new_pair_configurations':newpairs,'new_pair_nonprincipal':pairmats,'mixed_nonprincipal':mixedmats,'independent_obstruction_matrices':nmat,'support_types_checked':len(ledger),'relative_levels':[53,61,73,103,127],'cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]}
(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','cases':ledger},indent=2)+'\n');(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S17_FINAL_COVERAGE_PASS',len(cases),'primes;',len(ledger),'support types; unresolved=[]')
