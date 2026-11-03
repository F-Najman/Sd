from pathlib import Path
import sys,json,time
from sage.all import QQ,PolynomialRing,NumberField,matrix,identity_matrix,CyclotomicField,DirichletGroup,ModularSymbols
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
P=PolynomialRing(QQ,'x');s=(W/'frobenius127_data.m').read_text();tot=[0]*21;out=[];dim=0;tt=time.monotonic()
for n,pol,d,aa,c2,cs in lit(s,'Frob127Data'):
 K=NumberField(P(pol),'z');elt=lambda a:K([QQ(u)/QQ(v)for u,v in a]);T=matrix(K,d,d,[elt(a)for a in aa]);c=elt(c2);H0=2*identity_matrix(K,d);H1=T;values=[H1.trace().trace()]
 for f in range(2,22):H0,H1=H1,T*H1-2*c*H0;values.append(H1.trace().trace())
 assert values==cs;F=CyclotomicField(n);DG=DirichletGroup(127,base_ring=F);chi=next(c for c in DG if c.multiplicative_order()==n and c.is_even());S=ModularSymbols(chi,weight=2,sign=1).cuspidal_subspace();assert S.dimension()==d
 A=S.hecke_matrix(2);U0=2*identity_matrix(F,d);U1=A;new=[U1.trace().trace()]
 for f in range(2,22):U0,U1=U1,A*U1-2*chi(2)*U0;new.append(U1.trace().trace())
 assert new==cs;tot=[a+int(b)for a,b in zip(tot,cs)];dim+=K.degree()*d;out.append({'order':n,'dimension':d,'field_degree':K.degree(),'all21_traces_independently_recomputed':True});print('S21_FROB127_INDEPENDENT',n,round(time.monotonic()-tt,1),flush=True)
assert dim==610 and tot==lit(s,'Frob127Trace');points=[2**f+1-tot[f-1]for f in range(1,22)];assert points==lit(s,'Frob127PointCounts')
a=json.loads((W/'census_counts_independent.json').read_text());v=next(v for v in a['results']if v['p']==127);ss=v['supersingular_closed_diamond_orbits'];nc=7
for f in range(1,22):assert points[f-1]==v['ordinary_counts'][f-1]['rational_ordinary_points']+sum(d*o for d,o in ss if f%d==0)+63*(1+int(f%nc==0)),f
(W/'frobenius127_verified.json').write_text(json.dumps({'status':'PASS','degree':21,'genus':dim,'point_counts':points,'ordinary_full_torsion_correction_confirmed':True,'independent_Sage_modular_symbols':True,'results':out},indent=2,default=int)+'\n')
