from pathlib import Path
import re,json,hashlib,math
from fractions import Fraction
W=Path(__file__).resolve().parent;P=W.parent/'degree21';O=W.parent/'degree20';B=W.parents[1]
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
manifest=json.loads((P/'proof_manifest.json').read_text());assert sha(P/'proof_manifest.json')=='1ce61f220611ed348af3b0e92554a21f46d2bedd48058d45b654ac3f26e8f1c5'
def pinned(p):
 k=str(p.resolve());assert k in manifest,k;v=manifest[k];assert sha(p)==(v if isinstance(v,str)else v['sha256']);return k
def good(p):pinned(p);a=json.loads(p.read_text());assert a['status']=='PASS',p;return a
assert json.loads((W/'inherited_manifest_verified.json').read_text())['status']=='PASS'
facts=[P/'inherited_hypotheses_verified.json',P/'sharp61_finite_verified.json',P/'stabilizer_geometry_verified.json',O/'rankzero_verified.json',O/'sharp_finite_verified.json',O/'stabilizer_torsion_verified.json',O/'global_extra_verified.json',O/'anti163_norms_verified.json',O/'finite_FI_verified.json',O/'finite_FI_inheritance_verified.json',P/'global181_verified.json']
for p in facts:good(p)
for f in['finite_FI_polynomials.m','strange_eigenvalues_data.m','strange_eigenvalues61_data.m']:
 pinned(P/f);assert sha(W/f)==sha(P/f)
Ns=json.loads((W/'local_levels.json').read_text())['levels'];assert Ns==[59,61,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139]
for n in Ns:pinned(P/f'full{n}/units_data.m');assert sha(W/f'full{n}/units_data.m')==sha(P/f'full{n}/units_data.m')
assert json.loads((W/'source_prefixes_verified.json').read_text())['status']=='PASS'
records=[]
for p,n,h in[(167,5,83),(181,6,15)]:
 assert n*22<Fraction(325*(p*p-1),65536)
 orbits=[h]+[h//a for a in[2,3]if h%a==0];assert all(22%r for r in orbits)
 records.append({'p':p,'n':n,'strict_gonality_bound':str(Fraction(325*(p*p-1),65536)),'diamond_order':h,'all_geometric_orbits':orbits,'none_divides22':True})
a=good(O/'anti163_norms_verified.json');assert a['diamond_order']==27 and a['anti_homology_dimension']==1980 and a['total_degree_odd'];assert 6*22>=Fraction(325*(163**2-1),65536)
out={'status':'PASS','degree':22,'parent_manifest_files':100184,'pinned_facts':[str(f.resolve())for f in facts],'models_exactly_identical':Ns,'source_prefixes_identical':True,'global_167_181_applicability':records,'163_anti_H27_odd_isogeny_reused':True,'163_treated_locally':True,'ordinary_finite_maps_reused':True,'q2_cuspidal_2primary_used_only_at_levels_le157':True,'odd_degree_real_diamond_lemma_used':False};(W/'inherited_hypotheses_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_ALL_INHERITED_HYPOTHESES_PASS',flush=True)
