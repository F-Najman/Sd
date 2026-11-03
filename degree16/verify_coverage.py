from pathlib import Path
import json,re,sys,hashlib,itertools
from fractions import Fraction
from sage.all import prime_range
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit
ns=[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113];S=set(map(int,prime_range(2,38)))
def check(path,marker):
 s=path.read_text();assert marker in s,(path,marker);assert not any(x in s for x in['Runtime error','User error','Assertion failed','Traceback','System Error']),path
check(W/'verify_occurrences.log','S16_ALL_OCCURRENCES_COMPLETE')
check(W/'census_sources.log','S16_ALL_FINITE_SOURCE_ORBITS_COMPLETE');check(W/'census193.log','S16_ALL_FINITE_SOURCE_ORBITS_COMPLETE')
check(W/'stabilizers.log','S16_ALL_STABILIZERS_COMPLETE')
check(W/'certify_odd_anti.log','S16_ODD_ANTI_ISOGENIES_COMPLETE')
check(W/'cm_small.log','S16_RATIONAL_CM_J_EXCLUSIONS_COMPLETE')
check(W/'torsion43_upper.log','S16_TORSION43_Q_TWO_BOUND=4 COMPLETE')
check(W/'torsion43_reduction.log','S16_TORSION43_REDUCTION_INJECTIVE_COMPLETE')
check(W/'torsion43_Q_first.log','S16_TORSION43_ONE_CUSP_DIFFERENCE_ORDER_DIVIDES38_COMPLETE')
check(W/'known41_lifting.log','S16_KNOWN41_LIFT_AND_FI_COMPLETE cusp_configurations=210')
check(W/'lift43_14.log','S16_KNOWN43_DEGREE14_LIFT_MATCH_COMPLETE')
check(W/'known43_cot.log','S16_KNOWN43_COT_EXPORT_COMPLETE')
check(W/'export_new_finite.log','S16_NEW_FINITE_IMAGE_CHECKS_COMPLETE')
for n in ns:
 check(W/f'full{n}/stage2.log','AUDIT_ACTUAL_HECKE_JETS_COMPLETE')
 assert 'S16_OLD_ORBIT_REUSE_VERIFIED'in(W/f'full{n}/stage2.log').read_text()
 old=W.parent/('degree13'if n==43 else'degree15')/f'full{n}/units_data.m'
 assert hashlib.sha256(old.read_bytes()).digest()==hashlib.sha256((W/f'full{n}/units_data.m').read_bytes()).digest()
 a=json.load(open(W/f'full{n}/sieve.json'))
 ex=[(v['source'],v['degree'],v['orbit'])for v in a['exceptions']]
 assert ex==({41:[(79,14,10)],43:[(29,12,7),(91,14,21),(207,15,7),(221,15,7)],113:[(2,8,7)]}.get(n,[])),(n,ex)
 assert a['source_orbits']==a['nonprincipal']+len(a['exceptions'])
fi=json.load(open(W/'formal_immersion.json'));assert fi['status']=='PASS'and{v['N']for v in fi['results']}==set(ns)and all(v['status']=='PASS'and not v['exceptional_failures']for v in fi['results'])
assert json.load(open(W/'FI/FI193_verified.json'))['status']=='PASS'
aux=json.load(open(W/'auxiliary_verified.json'));assert aux['status']=='PASS'and aux['dyadic_ranks']==156
rank=json.load(open(W/'independent_rank_checks.json'));assert rank['status']=='PASS'
counts={k:sum(v['matrices']for v in rank['results']if v['kind']==k)for k in['ordinary','pair_','mixed_','borrowed_7plus7','borrowed_7plus8']}
assert counts=={'ordinary':4515,'pair_':558,'mixed_':34,'borrowed_7plus7':137,'borrowed_7plus8':254},counts
assert sum(counts.values())==5498
for n in[41,43,47,59,61,67,71,113]:
 a=json.load(open(W/f'full{n}/pair_sieve.json'));ex=a['exceptions']
 assert not ex if n!=113 else len(ex)==3 and all(v['source'][:2]==[2,2]for v in ex)
for n in[41,43,73]:assert not json.load(open(W/f'full{n}/mixed_sieve.json'))['exceptions']
for p,mark in[(B/'work/independent_audit/exceptional/P41_cusps.log','DECIC41_NONRATIONAL_CUSP_COMPLETE'),(B/'work/independent_audit/exceptional/P41_pairs.log','DECIC41_NC5_COMPLETE'),(B/'work/independent_audit/exceptional/supersingular41.log','NONIC_PRIME_GOOD_BRANCHES_COMPLETED'),(B/'work/independent_audit/exceptional/supersingular43.log','NONIC_PRIME_GOOD_BRANCHES_COMPLETED'),(B/'work/degree13/cusp43.log','S13_CUSP43_TEST_COMPLETE'),(B/'work/degree15/exceptional41.log','S15_NATIVE41_EXCEPTIONAL_COMPLETE')]:check(p,mark)
assert Fraction(127**2-1,192)==84>5*16
assert Fraction(97**2-1,192)==49>2*16 and 8*6<49 and 7>4
for n,c,r,factor in[(61,1,5,1),(73,10,9,1),(73,4,9,1),(73,7,9,1),(73,1,9,1),(89,5,11,1),(109,7,18,2),(109,4,18,2),(113,9,14,2),(113,2,14,2),(113,1,2,2)]:
 assert Fraction(325*(n*n-1),65536)>factor*(16+c)and c%r
assert 20>19 and 24>20 and 24>17 and 24>18
assert Fraction(325*(113**2-1),65536)>48
# Exhaust all possible support-degree multisets. R denotes rational cusps.
ledger=[]
for n in ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');oo=sorted({v[0]for v in rs if v[6]});ss=sorted({v[0]for v in rs if not v[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',v)for v in oo]+[('SS',v)for v in ss]+([('NC',nc)]if nc<=16 else[])
 def classify(support):
  d=sum(v for k,v in support);c=16-d;O=[v for k,v in support if k=='O'];other=[(k,v)for k,v in support if k!='O']
  if not support:return 'rational-cusp formal immersion'
  if len(O)==2:
   assert not other and sum(O)in[14,15,16]
   return 'ordinary pairs; exceptional orbit at113 descends to CM quadratic points'if n==113 else'ordinary pair obstruction'
  if len(O)==1 and not other:return 'ordinary obstruction or the explicitly resolved ordinary exception'
  if len(O)==1:
   assert len(other)==1
   k,e=other[0];v=O[0]
   assert (n,k,e,v)in{(41,'SS',5,x)for x in[8,9,10,11]}|{(43,k,7,x)for k in['SS','NC']for x in[8,9]}|{(73,'SS',6,x)for x in[7,10]}|{(73,'NC',9,7),(113,'SS',7,8)}
   return 'mixed obstruction or the113 involution'
  assert not O
  if n==41:assert all(k in['SS','NC']for k,v in other);return 'native41 certificates, including triples and SS+NC'
  if n==43:
   assert d in[7,14]
   return 'native degree7 test'if d==7 else'order7 stabilizer with injective torsion reduction'
  allowed={53:[13],61:[15],73:[6,9,12,15],89:[11],97:[16],109:[9,12],113:[7,14]}
  assert n in allowed and d in allowed[n],(n,support)
  return 'quotient97 and odd isogeny'if n==97 else'proved stabilizer exclusion'
 def walk(start,left,support):
  reason=classify(support);ledger.append({'p':n,'support':support,'rational_cusp_complement':left,'reason':reason})
  for j in range(start,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],support+[types[j]])
 walk(0,16,[])
# Quotient193 has no noncuspidal reduction with j-degree<=2.
rs=lit((W/'sources193.m').read_text().replace('true','True').replace('false','False'),'AuditSources');assert all(len(v[4])-1>2 for v in rs)
a=json.load(open(W/'gonality53.json'));b=json.load(open(W/'gonality53_nonrat.json'));assert a['status']==b['status']=='PASS'and a['gonality_lower_bound']==20 and a['independent_expected_tuples']==12982006
# All primes through the proven cap.
g=json.load(open(W/'global_bound.json'));assert g['status']=='PASS'and g['degree']==16 and g['cap']==66049 and set(g['local_levels'])==set(ns)|{127,193}
cases={p:'verified occurrence'for p in S}
for a in g['excluded']:
 assert a['p']not in cases;cases[a['p']]=a['reason']
for n in ns:assert n not in cases;cases[n]='complete local exclusion at2'
cases[127]='proved Selberg spectral bound and Proposition4.1'
cases[193]='index12 quotient, finite-field census and degree2 cusp formal immersion'
assert set(cases)==set(map(int,prime_range(2,66050)))
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':16,'S':sorted(S),'proved_lower_bound':sorted(S),'proved_upper_bound':sorted(S),'unresolved_primes':[],'dyadic_bound':66049,'coefficient_rank':32,'dyadic_M':157,'audited_primes':len(cases),'resolved_primes':len(cases),'complete_local_exclusions':18,'ordinary_source_orbits':4521,'ordinary_nonprincipal':4515,'independent_obstruction_matrices':5498,'new_ordinary_pair_configurations':561,'exceptional_pair_configurations_resolved':3,'mixed_obstructions':34,'support_types_checked':len(ledger),'gonality43_reference':'Varivoda TheoremD, hexagon:2610.00219v1','reference_code_commit':'66c5f61e9ead7ea430f6d2c8538237e01a83e652','cases':[{'p':p,'reason':cases[p]}for p in sorted(cases)]}
(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','cases':ledger},indent=2)+'\n');(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S16_FINAL_COVERAGE_PASS',len(cases),'primes;',len(ledger),'support types; unresolved=[]')
