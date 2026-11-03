from pathlib import Path
import json
from sage.all import EllipticCurve,vector
from intrinsic_model import Model,compare,results,PR
W=Path(__file__).resolve().parent;M=Model(61);F,z,orb=M.point(20,True,6);r=next(r for r in M.sources if r[6]and r[0]==20 and r[5]==6);assert M.sources.index(r)+1==2921;E=EllipticCurve([F(PR(v))for v in r[2]]);P=E([F(PR(v))for v in r[3]]);assert P!=E(0)and 61*P==E(0)
H=M.D**M.log(3);HF=H.change_ring(F);v=z
for i in range(1,6):
 v=HF*v;v/=next(a for a in v if a)
 if v==z:break
assert i==5 and H**5==M.I
hz=HF*z;hz/=next(a for a in hz if a);assert any(hz==vector(F,[a**(2**j)for a in z])for j in range(20))
compare(M,'relative61_o20',M.operators(3,[2,3,5,7]),20,16,True,6)
# Independent full profile-space checker, without rerunning the other cases.
s=(W/'verify_profile_spaces.py').read_text().split('cases=')[0];scope={'__file__':str(W/'verify_profile_spaces.py')};exec(compile(s,str(W/'verify_profile_spaces.py'),'exec'),scope);scope['check_case']('relative61_o20',1,20,16,6,1)
(W/'relative61_o20_independent.json').write_text(json.dumps({'status':'PASS','source':2921,'ordinary_degree':20,'closed_diamond_orbit':6,'H5_free_geometric_orbit':5,'quotient_genus':26,'quotient_divisor_degree':4,'base_rank':16,'fixed_cusp_degree':1,'profiles':6,'intrinsic':results,'profile_spaces':scope['out']},indent=2)+'\n');print('S21_RELATIVE61_O20_ALL_CHECKS_PASS',flush=True)
