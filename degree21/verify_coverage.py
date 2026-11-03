"""Exhaustive degree21 support and prime coverage; final claims are guarded."""
from pathlib import Path
import sys,json,re,math,hashlib
from fractions import Fraction
from sage.all import prime_range,is_prime,divisors,valuation,factor
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;B=W.parents[1];O=W.parent/'degree20';Ns=json.loads((W/'local_levels.json').read_text())['levels'];structural='--structural-only'in sys.argv;local_only='--local-only'in sys.argv
read=lambda p:json.loads(p.read_text())
def good(name):a=read(W/name);assert a['status']=='PASS',name;return a
def src(folder,n):return lit((folder/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
def mark(p,needle):s=p.read_text();assert needle in s and not any(e in s for e in['Runtime error','User error','Assertion failed','Traceback','System Error']),str(p)
def strict(p,c,mult):assert Fraction(325*(p*p-1),65536)>mult*(21+c)
rs={n:src(W,n)for n in Ns};support=[];inventory={r['p']:r for r in read(W/'support_inventory.json')['levels']}
for n in Ns:
 ordinary=sorted({r[0]for r in rs[n]if r[6]});ss=sorted({r[0]for r in rs[n]if not r[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',d)for d in ordinary]+[('SS',d)for d in ss]+([('NC',nc)]if nc<=21 else[]);assert [list(t)for t in types]==inventory[n]['types']
 def classify(s,c):
  oo=[d for t,d in s if t=='O'];other=[(t,d)for t,d in s if t!='O'];total=21-c
  if not s:return 'full canonical cusp immersion'if n in[53,61,71,89,97,101,127]else('absolute cusp immersion with quotient relative fibers'if n in[103,131]else'absolute cusp immersion')
  if len(oo)==3:assert oo==[7,7,7]and not other and n in[59,61,67,71,73];return 'new unordered ordinary triples, Burnside-complete diamond orbits'
  if len(oo)==2:
   if other:assert n==73 and oo==[7,7]and other==[('SS',6)];return 'inherited mixed pair delta2 obstruction, all19 relative positions'
   if n==127 and oo==[9,9]:strict(n,c,2);return 'inherited pair obstructions; exceptional H9-invariant pair excluded by the odd-degree stabilizer'
   if n==113 and oo==[8,8]:strict(n,c,2);return 'inherited ordinary pair obstruction; exceptional even H8 stabilizer and real-diamond lemma'
   return 'ordinary pair obstruction, all relative positions, inherited below total21 (61 below20)'
  assert len(oo)<=1
  if oo:
   d=oo[0]
   if not other:
    if n==61 and d==20:return 'ordinary obstruction; unique H5-invariant source2921 resolved by degree4 quotient relative immersion and fixed C1'
    if n==113 and d==8:return 'ordinary obstruction; exceptional free H8 pullback relative immersion with C13'
    if n==127 and d==9:strict(n,c,2);return 'ordinary obstruction; exceptional H9 stabilizer, 9 does not divide21'
    if n==137 and d==17:strict(n,c,2);return 'ordinary obstruction; exceptional H17 stabilizer'
    return 'ordinary principal-divisor obstruction, including all new degree21 sources and61 degree20'
   if n==73:
    assert(d,tuple(other))in{(v,(('SS',6),))for v in[7,10,11,12,13,14,15]}|{(7,(('SS',6),('SS',6)))}|{(v,(('NC',9),))for v in[7,10,11,12]};return 'delta2 mixed obstruction; new O12 andO15 certificates, lower degrees inherited'
   if n==89:assert d in[9,10]and other==[('NC',11)];return 'delta2 mixed obstruction'
   if n==109:assert d in[11,12]and other==[('SS',9)];return 'delta2 mixed obstruction'
   if n==113:
    assert other==[('SS',7)]and d in[8,11,12,13,14]
    if d==8:strict(n,c,2);return 'even H2 stabilizer and real-diamond lemma'
    return 'delta2 mixed obstruction'
   assert n==127 and other==[('NC',7)]and d in[8,9,10,11,12,13,14]
   return 'two-pullback relative immersion; full 315-column relation code, minimum weight7'if d==9 else'delta2 mixed obstruction'
  if n==53:assert s==[('SS',13)];return 'H13 pullback relative immersion and fixed C8'
  if n==61:assert s in[[('SS',15)],[('SS',20)]];return 'free H5 pullback relative immersion and nonzero fixed cusp remainder'
  if n==73:
   if total==6:return 'tame H3-fixed lifts, H9 relative cusp fibers, fixed nonzero remainder'
   if total==9:return 'free H9 pullback and relative cusp fibers with fixed nonzero remainder'
   if total==12:return 'double tame H3-fixed lifts, all10 unordered positions; full C9 fiber handled by real-diamond lemma'
   if total==15:return 'SS6 plusNC9 relative immersion, all16 relative positions, fixed C6'
   assert total in[18,21];strict(n,c,1);return 'H9 stabilizer using actual rational2-torsion control, 9 does not divide21'
  if n==89:assert s==[('NC',11)];strict(n,c,1);return 'H11 stabilizer using inherited odd-degree anti-Jacobian isogeny'
  if n==97:assert s==[('SS',16)];return 'sharper finite Hecke maps and tame H3-fixed-lift relative immersion, C5'
  if n==109:
   if s==[('SS',9)]:return 'free H9 pullback relative immersion, C12'
   if s==[('SS',12)]:return 'new direct supersingular T3 principal-divisor obstruction'
   assert total in[18,21];strict(n,c,2);return 'even H18 stabilizer and real-diamond lemma'
  if n==113:
   if total==7:return 'new direct supersingular T3 principal-divisor obstruction'
   assert total in[14,21];strict(n,c,2);return 'even H14 stabilizer and real-diamond lemma'
  if n==127:
   if any(t=='SS'for t,d in s):
    if total==21:assert s==[('SS',14),('NC',7)];return 'direct SS14 plusNC7 T3 obstruction, all48 relative positions'
    assert s==[('SS',14)];strict(n,c,2);return 'T3 sources20,21; T5 sources22,25; T7 source24; source23 H7 quotient relative immersion, all27 disks'
   assert all(t=='NC'for t,d in s)and total in[7,14,21];strict(n,c,2);return 'H7 descent to degree3 on genus88 quotient, all1140 cusp configurations'
  assert n==137 and s==[('SS',17)];strict(n,c,2);return 'even H34 stabilizer and real-diamond lemma'
 cases=[]
 def walk(start,left,s):
  reason=classify(s,left);r={'p':n,'support':[list(v)for v in s],'cusp_complement':left,'argument':reason};support.append(r);cases.append({k:r[k]for k in['support','cusp_complement']})
  for j in range(start,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],s+[types[j]])
 walk(0,21,[]);assert cases==inventory[n]['cases']
assert len(support)==477
# Independently reconstruct every prime reduction, without a proof status yet.
g=read(W/'global_bound.json');assert(g['degree'],g['cap'],g['M'],g['coefficient_rank'])==(21,1050024,229,42)and g['local_levels']==Ns+[163,167,181]
lower=list(map(int,prime_range(2,48)));cases={p:'verified occurrence over an exact degree21 field'for p in lower};table={};pending=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if ' p&'in line:pending=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif '\\ord(\\chi)&'in line:
  vals=[math.lcm(*map(int,v.split(',')))for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(pending)==len(vals);table.update(zip(pending,vals));pending=None
assert len(table)==74;assert not{int(p)for d in divisors(21)if d%2==0 for p in[2*d+1,3*d+1]}
for z in g['excluded']:
 p,t=z['p'],z['strangeness'];assert is_prime(p)and 47<p<100000 and p not in cases and t==table.get(p,1)
 if z['reason']=='Corollary7.5':assert p*p>Fraction(2**19,325)*21+1 and 21%((p-1)//(2*t))
 else:
  ell=int(z['reason'].split('=')[1]);assert ell in[2,3]and t==1
  if ell==2:assert p<=157
  assert Fraction(325*(p*p-1),65536)>(2*ell+1)*21;o=next(k for k in range(1,p)if pow(ell,k,p)in[1,p-1]);assert all(21%(o//a)for a in[1,2,3]if o%a==0)
 cases[p]=z['reason']
for p in Ns+[163,167,181]:assert p not in cases;cases[p]='local or global certificate'
sel=read(W/'large_selected_orders.json');assert len(sel['primes'])==850 and(len(sel['jobs']),len(sel['reused']))==(2815,2474)
for z in sel['primes']:
 p,r,v,w,th=[z[k]for k in['p','r','valuation_m','valuation_degree','threshold']];m=(p-1)//2;assert is_prime(p)and is_prime(r)and valuation(m,r)==v and valuation(21,r)==w and th==v-w>0;assert [int(n)for n in divisors(m)if n%(r**th)==0]==z['orders']and p*p>Fraction(2**19,325)*21+1 and p not in cases;cases[p]='selected-character family'
assert sorted(z['p']for z in sel['primes'])==g['large_screen_primes'];ss=[n for vals in g['supersingular_orders'].values()for n in vals]
for f in['20','21']:
 for n in g['supersingular_orders'][f]:assert max(int(p)for p,e in factor(n))<100000
for p in map(int,prime_range(100000,1050025)):
 ordinary=False
 for f in[18,19,20,21]:
  q=2**f;t=math.isqrt(4*q);lo=(q+1-t+p-1)//p;hi=(q+1+t)//p;ordinary|=lo+lo%2<=hi
 goodred=ordinary or any(v%p==0 for v in ss);toric=any((2**f-1)%p==0 or(2**f+1)%p==0 for f in range(1,22))
 if goodred or toric:assert p in g['large_screen_primes']and p in cases
 else:assert p in g['large_dyadic_excluded']and p not in cases;cases[p]='dyadic parity, supersingular and toric orders, single-cusp immersion'
primes=list(map(int,prime_range(2,1050025)));assert set(cases)==set(primes)
if structural:
 (W/'coverage_plan.json').write_text(json.dumps({'status':'EXHAUSTIVE_PLAN_PENDING_CERTIFICATES','degree':21,'prime_count':len(primes),'support_types':len(support),'support':support},indent=2)+'\n');print('S21_COVERAGE_PLAN_COMPLETE',len(primes),'primes',len(support),'support types',flush=True);raise SystemExit(0)
# No exact set is issued until every required certificate below has passed.
for name in['sharp61_finite_verified.json','stabilizer_geometry_verified.json','intrinsic_full_new_verified.json','profile_spaces_full_new_verified.json','inherited_manifest_verified.json','inherited_hypotheses_verified.json','matches_verified.json','dyadic_independent.json','census_counts_independent.json','frobenius127_verified.json','global181_verified.json','fi_matrices_independent.json','intrinsic_relative_independent.json','intrinsic_full_cusps_extra.json','intrinsic_multiple_independent.json','quotients_intrinsic_verified.json','profile_coverage_independent.json','profile_spaces_independent.json','relative127_verified.json','relative_cusps_intrinsic_verified.json','relative61_o20_independent.json','polynomial_arithmetic_verified.json','ss_jets_independent.json','ss_jets_extra_T3_verified.json','support_inputs_verified.json','independent_rank_checks.json','large_verified.json','independent_sequence_results.json']:
 if local_only and name in['large_verified.json','independent_sequence_results.json']:continue
 good(name)
if not local_only:
 large=good('large_verified.json');assert large['verified']==5289 and good('independent_sequence_results.json')['checked']==2815
 fresh_large=[r for r in large['results']if not r['inherited']];assert len(fresh_large)==2815
 assert all(math.gcd(r['q'],6*r['p']*(r['p']-1))==1 for r in fresh_large)
 native=good('large_native_results.json');assert native['characters']==2815 and len(native['results'])==2815 and all(r['status']=='PASS'for r in native['results'])
rankdata=good('independent_rank_checks.json');sets=read(W/'small_jet_jobs.json')['degree_sets'];ranktasks={(f'full{n}','')for n in Ns}|{(f'full{n}','pair_')for n in map(int,sets)}|{(f'full{n}','mixed_')for n in[73,89,109,113,127]}|{(f'ss{n}','')for n in[73,109,113,127]}|{('ss5_127',''),('ss7_127',''),('ss127','mixed_nc_')}
assert{(r['folder'],''if r['kind']=='ordinary'else r['kind'])for r in rankdata['results']}==ranktasks and len(rankdata['results'])==len(ranktasks)==49
for rec in rankdata['results']:
 kind=''if rec['kind']=='ordinary'else rec['kind'];H=W/rec['folder'];a=read(H/(kind+'sieve.json'));archive=H/(kind+'matrices.json.gz');assert a['nonprincipal']==rec['matrices']and a['dimension']==rec['rank']and hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()==rec['matrix_archive_sha256']
 sec,gc,P=a['section_degree'],a['canonical_genus'],a['precision'];assert sec in[1,2]and P-2*sec>4*sec*(gc-1)and a['dimension']==(gc if sec==1 else 3*gc-3)and a['product_dimension']==(3*gc-3 if sec==1 else 7*gc-7)
assert sum(r['matrices']for r in rankdata['results'])==rankdata['matrices']==81523
assert all(r['status']=='PASS'for r in read(W/'new_ordinary_job_results.json'))
sieve_jobs=read(W/'new_ordinary_sieve_jobs.json');assert{r['N']for r in sieve_jobs}==set(Ns)and all(r['status']=='PASS'for r in sieve_jobs)
newcount=0
for n in Ns:
 H=W/f'full{n}';a=read(H/'sieve.json')
 if n==61:
  assert a['status']=='PASS_WITH_EXPLICIT_EXCEPTIONS'and[(r['source'],r['degree'],r['orbit'],r['status'])for r in a['exceptions']]==[(2921,20,6,'ZERO_DIVISOR')]
  q=good('relative61_o20_independent.json');assert(q['source'],q['profiles'],q['base_rank'])==(2921,6,16)
 else:assert a['status']=='PASS'and not a['exceptions']
 expected=[(i+1,r[0],r[5],r[4])for i,r in enumerate(rs[n])if r[6]and(r[0]in[20,21]if n==61 else r[0]==21)];meta=lit((H/'hecke_jets.m').read_text(),'SourceMetadata');assert sorted(meta)==sorted(expected);assert sorted((r['source'],r['degree'],r['orbit'])for r in a['results'])==sorted(v[:3]for v in expected)and a['nonprincipal']==len(expected)-(1 if n==61 else 0);newcount+=len(expected)
for name in['full_cusps61_sharp','full_cusps89','full_cusps97_sharp','full_cusps71','full_cusps127','relative53','full_cusps53','relative61','relative61_ss20','relative61_o20','relative73','relative73_nc','relative109','relative113_ordinary','relative97_sharp','full_cusps101_sharp']:good(name+'_profiles_verified.json')
good('relative73_multiple_verified.json')
for n in[59,67,73,79,83,103,107,109,113,131,137,139]:assert read(W/f'FI/FI{n}_verified.json')['status']in['PASS','PASS_RELATIVE']
for tag,ids in[('ss109',{4}),('ss113',{1}),('ss127',{20,21}),('ss5_127',{22,25}),('ss7_127',{24})]:
 a=read(W/tag/'sieve.json');assert ids<={r['source']for r in a['results']if r['status']=='NONPRINCIPAL'}
a=good('ss127/mixed_nc_sieve.json');assert a['nonprincipal']==48 and not a['exceptions'];good('quotient127_cusps_verified.json')
mark(W/'verify_occurrences.log','S21_ALL_OCCURRENCES_COMPLETE');mark(W/'bound_ss_certified.log','S21_BOUND_TWISTS_CERTIFIED_COMPLETE')
(W/'support_coverage.json').write_text(json.dumps({'status':'PASS','degree':21,'cases':support},indent=2)+'\n')
local={'status':'PASS','degree':21,'local_levels':Ns,'support_types':477,'new_ordinary_sources':newcount,'new_independent_matrices':good('independent_rank_checks.json')['matrices'],'resolved_fresh_ordinary_exceptions':[{'p':61,'source':2921,'argument':'free H5 pullback degree4 plus fixed cusp1, all6 relative disks'}]}
(W/'local_coverage_verified.json').write_text(json.dumps(local,indent=2)+'\n')
if local_only:
 print('S21_ALL_LOCAL_EXCLUSIONS_PROVED',477,newcount,local['new_independent_matrices'],flush=True);raise SystemExit(0)
out={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':21,'S':lower,'proved_lower_bound':lower,'proved_upper_bound':lower,'unresolved_primes':[],'dyadic_bound':1050024,'dyadic_M':229,'coefficient_rank':42,'audited_primes':len(primes),'large_primes_screened':850,'selected_characters_screened':5289,'new_characters_screened':2815,'inherited_characters':2474,'support_types':477,'new_ordinary_sources':newcount,'new_independent_matrices':good('independent_rank_checks.json')['matrices'],'cases':[{'p':p,'reason':cases[p]}for p in primes]};(W/'final_coverage.json').write_text(json.dumps(out,indent=2)+'\n');print('S21_FULL_COVERAGE_PROVED',len(primes),'primes,477 support types',flush=True)
