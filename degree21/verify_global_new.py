from pathlib import Path
import json,time,sys
from sage.all import QQ,PolynomialRing,NumberField,matrix,identity_matrix,DirichletGroup,ModularSymbols,CyclotomicField,euler_phi,divisors
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
P=PolynomialRing(QQ,'x');out=[];dimension=0;tt=time.monotonic()
for n,q,pol,d,aa,dc,nd in lit((W/'anti181_data.m').read_text(),'Anti181Data'):
 K=NumberField(P(pol),'z');elt=lambda a:K([QQ(u)/QQ(v)for u,v in a]);A=matrix(K,d,d,[elt(a)for a in aa]);det=A.det();assert det==elt(dc)and det.norm()==nd and QQ(nd).denominator()==1 and int(nd)%2
 assert K.degree()==euler_phi(n);dimension+=K.degree()*d;z=K.gen();uu=z**2;EE=5*sum(uu**(5*j)for j in range(9))-sum(uu**j for j in range(45));assert EE==(45 if n in[5,10]else 0)
 F=CyclotomicField(n);DG=DirichletGroup(181,base_ring=F);chi=next(c for c in DG if c.multiplicative_order()==n and c.is_even());S=ModularSymbols(chi,weight=2,sign=0).cuspidal_subspace();assert S.dimension()==d;B=S.hecke_matrix(q)-(chi(q)+q)*identity_matrix(F,d);newnorm=B.det().norm();assert newnorm==nd,(n,q,newnorm,nd)
 out.append({'order':n,'q':q,'dimension':d,'coefficient_degree':K.degree(),'norm':str(nd),'independent_Sage_modular_symbols_norm_equal':True});print('S21_ANTI181_INDEPENDENT',n,q,'seconds',round(time.monotonic()-tt,1),flush=True)
assert dimension==2388 and lit((W/'anti181_data.m').read_text(),'Anti181Dimension')==2388
assert [r['order']for r in out]==[n for n in divisors(90)if 6%n!=0]
assert 6*21*65536<325*(181**2-1)and next(k for k in range(1,91)if pow(64,k,181)in[1,180])==15 and 21%15
(W/'global181_verified.json').write_text(json.dumps({'status':'PASS','degree':21,'anti_homology_dimension':dimension,'projector':'E=5*N_(u^5)-N_u, u=diamond2^2; beta=E*A11+(45-E)*A3','odd_degree_isogeny':True,'independent_Sage_modular_symbols':True,'results':out},indent=2,default=int)+'\n')
