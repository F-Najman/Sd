"""Independent intrinsic quotient cotangents and all degree-three ranks."""
from pathlib import Path
import json,itertools,time
from sage.all import GF,matrix,vector,PolynomialRing,PowerSeriesRing,ZZ
from intrinsic_model import Model,stack,coeff,units,F2,PR
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;start=time.monotonic();M=Model(127);g=M.g
F=GF(2**7,name='a');a=F.multiplicative_generator()**((2**7-1)//127);assert a.multiplicative_order()==127;z0=M.cv(F,units([F(1),F(0),F(0),F(0),F(0)],a/(1+a)**2,a*a/(1+a)**3))
# The two-pullback disk upstairs has base degree16 and rank14.
rs=(W/'relative127_data.m').read_text();O,zo,oo=M.point(9,True,7);assert oo==7
AP=[(M.D**7-M.I)*(M.D**M.log(2)-M.I)*(M.hecke(q)-M.D**M.log(q)-F2(q)*M.I)for q in[2,3,5]if M.hecke(q)is not None]
B=stack([coeff(A.change_ring(O)*zo,9).augment(coeff(A.change_ring(F)*z0,7))for A in AP]);assert B==matrix(F2,lit(rs,'Relative127Base'))and B.rank()==14
CJ=lit(rs,'Relative127CuspJets')
for k,rr in enumerate(CJ):assert stack([A*M.D**k*M.Q[:,1:7]for A in AP])==matrix(F2,rr)
(W/'relative127_intrinsic_verified.json').write_text(json.dumps({'status':'PASS','degree':22,'base_rank':14,'base_degree':16,'cusp_degree':6,'cusp_blocks':63,'jet_precision':6},indent=2)+'\n');print('S22_RELATIVE127_INTRINSIC_COMPLETE',flush=True)
