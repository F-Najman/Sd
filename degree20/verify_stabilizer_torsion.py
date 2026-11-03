from pathlib import Path
import re,ast,json,time
from sage.all import QQ,GF,matrix
from unit_arithmetic import lit
W=Path(__file__).resolve().parent
while not(W/'two73_data.m').exists()or'RATIONAL_TWO_DONE'not in(W/'rational_two73.log').read_text():time.sleep(3)
s=(W/'two73_data.m').read_text();assert s.startswith('// Exact JOne(73) integral homology, sign0.')and re.search(r'\bd:=374;',s)
def mat(name):
 a=re.search(r'\b'+name+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);assert a;return matrix(GF(2),int(a[1]),int(a[2]),ast.literal_eval(a[3]))
A,B,D=mat('Aq3Z'),mat('Aq5Z'),mat('D2Z');K=A.left_kernel().intersection(B.left_kernel());assert all(v*(D-matrix.identity(GF(2),374))==0 for v in K.basis())
out=[{'p':73,'status':'PASS','actual_JOne':True,'full_integral_homology_rank':374,'rational_2torsion_upper_dimension':int(K.dimension()),'diamond2_trivial_on_upper_bound':True}]
while not(W/'odd_anti89_data.m').exists()or'S20_ODD_ANTI_ISOGENIES_COMPLETE'not in(W/'certify_odd_anti89.log').read_text():time.sleep(3)
records=lit((W/'odd_anti89_data.m').read_text(),'OddAntiData');assert len(records)==2
for p,ind,sign,g,r,det,entries in records:
 A=matrix(QQ,r,r,[QQ(a)/QQ(b)for a,b in entries]);assert(p,ind,g,r)==(89,44,287,260)and A.det()==det and int(det)%2 and QQ(det).denominator()==1
 out.append({'p':89,'status':'PASS','Betti_sign':sign,'anti_dimension':r,'odd_determinant':str(det)})
assert {v['Betti_sign']for v in out if v['p']==89}=={1,-1}
(W/'stabilizer_torsion_verified.json').write_text(json.dumps({'status':'PASS','fresh_actual_lattice_and_odd_degree_checks':out},indent=2)+'\n');print('S20_STABILIZER_TORSION_INDEPENDENT_PASS 73 actual_JOne and89 both_Betti_signs',flush=True)
