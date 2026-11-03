from pathlib import Path
import sys,json,re
from sage.all import GF,matrix,PolynomialRing,vector
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit,matbits
F2=GF(2);p=127;g=610;s=(W/'full127/units_data.m').read_text();prec=int(re.search(r'precision:=(\d+)',s)[1]);Q=matrix(F2,[[v>>j&1 for j in range(prec)]for v in matbits(s,'qcoeffs')]);D=matrix(F2,[[v>>j&1 for j in range(g)]for v in matbits(s,'DiamondMatrix')]);I=matrix.identity(F2,g);assert D**63==I
log2=next(k for k in range(63)if pow(3,k,127)in[2,125]);alpha=(D**7-I)*(D**log2-I);AA=[]
for q in[2,3]:
 cut=min(1344,(prec-1)//q);C=Q[:,:cut+1];assert C.rank()==g;log=next(k for k in range(63)if pow(3,k,127)in[q,127-q]);DQ=D**log*Q;TQ=matrix(F2,[[Q[i,q*n]+(F2(q)*DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;A=alpha*(T-D**log-F2(q)*I);assert A*D==D*A;AA.append(A)
RX=matrix(F2,[[v>>j&1 for j in range(2*g)]for v in matbits(s,'UnitXRelations')]);RY=matrix(F2,[[v>>j&1 for j in range(2*g)]for v in matbits(s,'UnitYRelations')]);PR=PolynomialRing(F2,'t');dat=(W/'relative127_data.m').read_text()
def CV(F,x,y):
 R=matrix(F,[[F(row[j])+u*F(row[g+j])for j in range(g)]for M,u in[(RX,x),(RY,y)]for row in M.rows()]);assert R.rank()==g-1;z=R.right_kernel().basis()[0];return z/next(v for v in z if v)
def units(aa,x,y):
 a1,a2,a3,a4,a6=aa;u3=a3+a1*x;u2=x+a2;u4=x*x+a4+a1*y;v2=u2+(u4/u3)**2+a1*u4/u3;b=v2**3/u3**2;c=(a1*v2+u3)/u3;rv=b/c;sv=c*c/(b+c);tv=rv*sv+1;return(sv+rv)/tv,tv/(sv*sv+sv+rv+1)
FO=GF(2**9,name='a',modulus=PR(lit(dat,'Relative127OrdinaryPolynomial')));FN=GF(2**7,name='b',modulus=PR(lit(dat,'Relative127NonratPolynomial')))
rs=lit((W/'sources127.m').read_text().replace('true','True').replace('false','False'),'AuditSources');r=rs[2];assert(r[0],r[5])==(9,7);aa=[FO(PR(v))for v in r[2]];x,y=[FO(PR(v))for v in r[3]];xo,yo=units(aa,x,y);zo=CV(FO,xo,yo);assert zo==vector(FO,[FO(PR(v))for v in lit(dat,'Relative127OrdinaryZ')])
b=FN.gen();assert b.multiplicative_order()==127;xn,yn=units([FN(1),FN(0),FN(0),FN(0),FN(0)],b/(1+b)**2,b*b/(1+b)**3);zn=CV(FN,xn,yn);assert zn==vector(FN,[FN(PR(v))for v in lit(dat,'Relative127NonratZ')])
v=(D**log2).change_ring(FN)*zn;v/=next(a for a in v if a);assert any(v==vector(FN,[a**(2**k)for a in zn])for k in range(7))
Bs=[]
for A in AA:
 vo=A.change_ring(FO)*zo;vn=A.change_ring(FN)*zn
 O=matrix(F2,[list(v.polynomial())+[0]*(9-len(list(v.polynomial())))for v in vo]);N=matrix(F2,[list(v.polynomial())+[0]*(7-len(list(v.polynomial())))for v in vn]);Bs.append(O.augment(N))
B=Bs[0].stack(Bs[1]);assert B.rank()==14
ms=lit(dat,'Relative127Matrices');assert len(ms)==63;Dp=I;q1=Q.column(1)
for k,rr in enumerate(ms):
 cs=[Dp*A*q1 for A in AA];c=matrix(F2,[[v]for v in list(cs[0])+list(cs[1])]);R=B.augment(c);assert R==matrix(F2,rr)and R.rank()==15;Dp*=D
out={'status':'PASS','degree':17,'family_dimension':2,'relative_rank':15,'patterns_checked':63,'pullback_degrees':[9,7],'fixed_rational_cusp_degree':1,'operators':[2,3],'cotangent_entries_rebuilt':True,'nonrational_cusp_identification_verified':True}
(W/'relative127_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S17_RELATIVE127_INDEPENDENT_PASS',out,flush=True)
