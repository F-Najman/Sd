"""Bind all reused global, lattice, torsion, and finite-image facts."""
from pathlib import Path
import re,json,hashlib
from sage.all import ZZ,PolynomialRing,cyclotomic_polynomial
W=Path(__file__).resolve().parent;O=W.parent/'degree20';B=W.parents[1]
def read(p):return json.loads(p.read_text())
def good(f):a=read(O/f);assert a['status']=='PASS';return a
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
a=read(W/'inherited_manifest_verified.json');assert a['status']=='PASS'and a['files']==37906
for f in['rankzero_verified.json','sharp_finite_verified.json','stabilizer_torsion_verified.json','global_extra_verified.json','anti163_norms_verified.json','finite_FI_verified.json','finite_FI_inheritance_verified.json']:good(f)
assert {r['p']for r in good('rankzero_verified.json')['cases']}=={59,71}
pols=lambda p:{(int(a),int(b)):re.sub(r'\s+','',c)for a,b,c in re.findall(r'FiniteFIPolynomials\[<(\d+),(\d+)>\]:=(.*?);',p.read_text(),re.S)}
keys=[(61,2),(61,3),(61,5),(67,2),(67,3),(67,5),(73,2),(73,3),(73,5),(79,2),(83,2),(89,2),(97,5),(103,2)];pp=pols(O/'finite_FI_polynomials.m');pn=pols(W/'finite_FI_polynomials.m');facts={(r['p'],r['hecke_index']):r for r in good('finite_FI_verified.json')['exact_J0_matrix_checks']};assert all(pp[k]==pn[k]and facts[k]['polynomial_image_in_winding_space']for k in keys)
orders={};ps=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if ' p&'in line:ps=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif '\\ord(\\chi)&'in line:
  vals=[[int(t)for t in v.split(',')]for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(vals)==len(ps);orders.update(zip(ps,vals))
assert len(orders)==74;R=PolynomialRing(ZZ,'x');x=R.gen();records=[]
for p in read(W/'local_levels.json')['levels']:
 parent=O if p!=61 else W.parent/'degree19';assert sha(W/f'full{p}/units_data.m')==sha(parent/f'full{p}/units_data.m');poly={61:x**6-1,97:(x-1)*(x**6+1),101:(x-1)*(x**5+1)}.get(p,R(1)if p in[59,71]else x-1)
 for n in orders.get(p,[]):assert poly%R(cyclotomic_polynomial(n))==0
 assert p in[59,71]or poly(1)==0
 records.append({'p':p,'ordinary_annihilator':str(poly),'positive_character_orders':orders.get(p,[]),'model_identical_to_proved_parent':True})
for p in[163,167]:assert not orders.get(p,[])
assert orders[181]==[6]and (x**6-1)%R(cyclotomic_polynomial(6))==0
out={'status':'PASS','parent_manifest_files':37906,'finite_FI_polynomials':keys,'ordinary_characters':records,'new_181_positive_order':6,'global_163_167_reused':True,'actual_torsion_73_89_reused':True,'sharp_97_101_reused':True,'q2_cuspidal_2primary_proved_range_all_local_levels_le157':True};(W/'inherited_hypotheses_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S21_ALL_INHERITED_HYPOTHESES_PASS',flush=True)
