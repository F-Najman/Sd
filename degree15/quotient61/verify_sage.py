from pathlib import Path
import sys,re,ast,json,math
from sage.all import QQ,GF,matrix
H=Path(__file__).resolve().parent;W=H.parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
out=[]
for ind,g,r,ws,us in lit((H/'finite_diamonds_data.m').read_text(),'FiniteDiamondData'):
 A=matrix(QQ,g,g,[QQ(a)/b for a,b in ws]);B=matrix(QQ,g,g,[QQ(a)/b for a,b in us]);assert A.rank()==r==A.stack(B).rank();out.append({'index':ind,'genus':g,'winding_rank':r});print('SAGE_FINITE_IMAGE',ind,g,r,flush=True)
s=(W/'two61_data.m').read_text()
def m(name):
 a=re.search(name+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);return matrix(GF(2),int(a[1]),int(a[2]),ast.literal_eval(a[3]))
K=m('Aq3Z').left_kernel().intersection(m('Aq5Z').left_kernel()).intersection(m('Aq7Z').left_kernel());assert K.dimension()==0
A=matrix(QQ,[[0,0,-QQ(1)/2,QQ(1)/2],[0,1,0,0],[-QQ(1)/2,0,0,QQ(1)/2],[QQ(1)/2,0,QQ(1)/2,0]]);assert A.det()==-QQ(1)/4 and A.rank()==4
# Independent prime-level genus formula, using the subgroup before quotient by sign.
genera=[]
for generator in[1,3,4,2]:
 Hfull={pow(generator,k,61)*sgn%61 for k in range(60)for sgn in[1,-1]};ind=60//len(Hfull);mu=62*ind;cusps=2*ind;e2=ind*sum((a*a+1)%61==0 for a in Hfull);e3=ind*sum((a*a+a+1)%61==0 for a in Hfull);g=1+QQ(mu)/12-QQ(e2)/4-QQ(e3)/3-QQ(cusps)/2;genera.append(int(g))
assert genera==[126,26,8,4]
assert 2*8-2-2*(2*4-2)==2 and QQ(325*3720)/65536>15
for name,mark in [('finite_diamonds.log','S15_DIAMOND_FINITE_IMAGES_COMPLETE'),('verify_small_quotient.log','S15_SMALL_QUOTIENT61_CHECKS_COMPLETE'),('verify_reduction.log','S15_SS61_REDUCTION_AND_TRANSITIVE_H15_ACTION_COMPLETE')]:
 s=(H/name).read_text();assert mark in s and not any(x in s for x in['Runtime error','Assertion failed','User error'])
(H/'independent_checks.json').write_text(json.dumps({'status':'PASS','finite_images':out,'rational_two_torsion_dimension':0,'quadric_determinant':'-1/4','genera_X_Y_Z_X0':genera,'geometric_fixed_points':2},indent=2)+'\n');print('S15_QUOTIENT61_INDEPENDENT_CHECKS_PASS',flush=True)
