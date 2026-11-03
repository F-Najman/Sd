from pathlib import Path
import json,time,sys
from sage.all import QQ,PolynomialRing,NumberField,matrix,identity_matrix,DirichletGroup,ModularSymbols,CyclotomicField,euler_phi,divisors
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
P=PolynomialRing(QQ,'x');out=[];dimension=0;tt=time.monotonic()
for n,q,pol,d,aa,dc,nd in lit((W/'anti173_data.m').read_text(),'Anti173Data'):
 K=NumberField(P(pol),'z');elt=lambda a:K([QQ(u)/QQ(v)for u,v in a]);A=matrix(K,d,d,[elt(a)for a in aa]);det=A.det();assert det==elt(dc)and det.norm()==nd and QQ(nd).denominator()==1 and int(nd)%2
 assert K.degree()==euler_phi(n);dimension+=K.degree()*d;
 F=CyclotomicField(n);DG=DirichletGroup(173,base_ring=F);chi=next(c for c in DG if c.multiplicative_order()==n and c.is_even());S=ModularSymbols(chi,weight=2,sign=0).cuspidal_subspace();assert S.dimension()==d;B=S.hecke_matrix(q)-(chi(q)+q)*identity_matrix(F,d);newnorm=B.det().norm();assert newnorm==nd,(n,q,newnorm,nd)
 out.append({'order':n,'q':q,'dimension':d,'coefficient_degree':K.degree(),'norm':str(nd),'independent_Sage_modular_symbols_norm_equal':True});print('S22_ANTI173_INDEPENDENT',n,q,'seconds',round(time.monotonic()-tt,1),flush=True)
assert dimension==2268 and lit((W/'anti173_data.m').read_text(),'Anti173Dimension')==2268
assert [r['order']for r in out]==[43,86]
assert 6*22*65536<325*(173**2-1)and next(k for k in range(1,87)if pow(4,k,173)in[1,172])==43 and 22%43
(W/'global173_verified.json').write_text(json.dumps({'status':'PASS','degree':22,'anti_homology_dimension':dimension,'projector':'h=diamond4 order43; all B character components have odd A3 determinant','odd_degree_isogeny':True,'independent_Sage_modular_symbols':True,'results':out},indent=2,default=int)+'\n')
