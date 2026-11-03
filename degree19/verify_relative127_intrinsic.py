from pathlib import Path
import sys,re,json
from sage.all import GF,matrix,PolynomialRing
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit,matbits
F2=GF(2);p=127;g=610;s=(W/'full127/units_data.m').read_text();prec=int(re.search(r'precision:=(\d+)',s)[1]);Q=matrix(F2,[[v>>j&1 for j in range(prec)]for v in matbits(s,'qcoeffs')]);D=matrix(F2,[[v>>j&1 for j in range(g)]for v in matbits(s,'DiamondMatrix')]);I=matrix.identity(F2,g);k2=next(k for k in range(63)if pow(3,k,127)in[2,125]);alpha=(D**7-I)*(D**k2-I);AA=[]
for q in[2,3]:
 cut=min(1344,(prec-1)//q);C=Q[:,:cut+1];k=next(k for k in range(63)if pow(3,k,127)in[q,127-q]);DQ=D**k*Q;TQ=matrix(F2,[[Q[i,q*n]+(F2(q)*DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;AA.append(alpha*(T-D**k-F2(q)*I))
RX=matrix(F2,[[v>>j&1 for j in range(2*g)]for v in matbits(s,'UnitXRelations')]);RY=matrix(F2,[[v>>j&1 for j in range(2*g)]for v in matbits(s,'UnitYRelations')]);PR=PolynomialRing(F2,'t')
def units(aa,x,y):
 a1,a2,a3,a4,a6=aa;u3=a3+a1*x;u2=x+a2;u4=x*x+a4+a1*y;v2=u2+(u4/u3)**2+a1*u4/u3;b=v2**3/u3**2;c=(a1*v2+u3)/u3;rv=b/c;sv=c*c/(b+c);tv=rv*sv+1;return(sv+rv)/tv,tv/(sv*sv+sv+rv+1)
def CV(F,x,y):
 R=matrix(F,[[F(row[j])+u*F(row[g+j])for j in range(g)]for M,u in[(RX,x),(RY,y)]for row in M.rows()]);assert R.rank()==g-1;v=R.right_kernel().basis()[0];return v/next(a for a in v if a)
rs=lit((W/'sources127.m').read_text().replace('true','True').replace('false','False'),'AuditSources');r=rs[2];assert(r[0],r[5])==(9,7);FO=GF(2**9,name='a',modulus=PR(r[1]));aa=[FO(PR(v))for v in r[2]];x,y=[FO(PR(v))for v in r[3]];zo=CV(FO,*units(aa,x,y));old=(W.parent/'degree17/relative127_data.m').read_text();FN=GF(2**7,name='b',modulus=PR(lit(old,'Relative127NonratPolynomial')));b=FN.gen();assert b.multiplicative_order()==127;zn=CV(FN,*units([FN(1),FN(0),FN(0),FN(0),FN(0)],b/(1+b)**2,b*b/(1+b)**3));Bs=[]
for A in AA:
 vo=A.change_ring(FO)*zo;vn=A.change_ring(FN)*zn;O=matrix(F2,[list(a.polynomial())+[0]*(9-len(list(a.polynomial())))for a in vo]);N=matrix(F2,[list(a.polynomial())+[0]*(7-len(list(a.polynomial())))for a in vn]);Bs.append(O.augment(N))
B=Bs[0].stack(Bs[1]);dat=(W/'relative127_data.m').read_text();assert B==matrix(F2,lit(dat,'Relative127Base'))and B.rank()==14
CJ=lit(dat,'Relative127CuspJets');assert len(CJ)==63
for k,rr in enumerate(CJ):
 C=(AA[0]*D**k*Q[:,1:4]).stack(AA[1]*D**k*Q[:,1:4]);assert C==matrix(F2,rr)
out={'status':'PASS','relative_base_rank':14,'degree':19,'all_entries_rebuilt':True,'cusp_jet_blocks':63,'operators':[2,3]};(W/'relative127_intrinsic_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_RELATIVE127_INTRINSIC_REPLAY_PASS',flush=True)
