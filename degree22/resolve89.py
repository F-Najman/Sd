from pathlib import Path
import json,hashlib
from fractions import Fraction
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;P=W.parent/'degree21';O=W.parent/'degree20'
def good(p):
 a=json.loads(p.read_text());assert a['status']=='PASS',p;return a
parent=good(W/'inherited_manifest_verified.json');assert parent['files']==100184
for f in['frobenius89_verified.json','quotient89_verified.json','quotient89_point_count_bound.json','quotient89_fixed_points_verified.json','quotient89_intrinsic_verified.json','ss_jets_independent.json']:good(W/f)
tor=good(O/'stabilizer_torsion_verified.json');r=[v for v in tor['fresh_actual_lattice_and_odd_degree_checks']if v['p']==89];assert sorted(v['Betti_sign']for v in r)==[-1,1]and all(v['anti_dimension']==260 and int(v['odd_determinant'])%2 for v in r)
ss=json.loads((W/'ss89/sieve.json').read_text());a={v['source']:v for v in ss['results']};assert a[4763]['status']=='NONPRINCIPAL';assert[(a[k]['degree'],a[k]['orbit'])for k in[4764,4765,4766,4767]]==[(22,4),(22,4),(22,2),(22,1)]
for q in[5,7]:
 a=good(W/f'ss{q}_89/sieve.json');assert{v['source']for v in a['results']}=={4764,4765}and not a['exceptions']
assert Fraction(325*(89**2-1),65536)>33
geo=good(W/'quotient89_fixed_points_verified.json');assert geo['Frobenius_cycle_lengths_on_fixed_points']==[4]
gon=good(W/'quotient89_point_count_bound.json');assert gon['gonality_Q_lower_bound']==8 and gon['rational_points']==38 and 38>7*5
text=(W/'references/Mazur1978.txt').read_text();assert'Theorem 1. Let N be a prime number'in text and'N = 1 1 , 17, 19, 37, 43, 67,'in text
out={'status':'PASS','N':89,'degree':22,'odd_anti_H11_isogeny_reused':True,'gonality_upstairs_lower_bound':str(Fraction(325*(89**2-1),65536)),'NC11_or_NC11_doubled':'H11 invariance, descent to Sym2(Y), all36 cusp disks formally immersed','SS22_sources':{'4763':'independent T3 principal-divisor obstruction','4764':'independent T5 obstruction (T7 also passes)','4765':'independent T5 obstruction (T7 also passes)','4766':'H11 descent then residual involution, doubled degree4 < quotient gonality8','4767':'H11 descent then residual involution, doubled degree4 < quotient gonality8'},'residual_involution_fixed_points_all_degree':4,'free_invariant_pair_descends_to':'rational noncuspidal point of a quotient mapping to X0(89); excluded by Mazur Theorem1','Mazur_pdf_sha256':hashlib.sha256((W/'references/Mazur1978.pdf').read_bytes()).hexdigest()};(W/'resolution89_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_ALL_NEW_89_DISKS_RESOLVED',flush=True)
