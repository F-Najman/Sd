from pathlib import Path
import sys,re,json
from sage.all import GF,matrix,PolynomialRing,vector
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit,matbits
F2=GF(2);p=73;g=187;s=(W/'full73/units_data.m').read_text();prec=int(re.search(r'precision:=(\d+)',s)[1]);root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);Q=matrix(F2,[[v>>j&1 for j in range(prec)]for v in matbits(s,'qcoeffs')]);D=matrix(F2,[[v>>j&1 for j in range(g)]for v in matbits(s,'DiamondMatrix')]);I=matrix.identity(F2,g);k2=next(k for k in range(36)if pow(root,k,73)in[2,71]);AA=[]
for q in[3,5,7]:
 cut=min(444,(prec-1)//q);C=Q[:,:cut+1]
 if C.rank()<g:continue
 k=next(k for k in range(36)if pow(root,k,73)in[q,73-q]);DQ=D**k*Q;TQ=matrix(F2,[[Q[i,q*n]+(DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;AA.append((D**k2-I)*(T-D**k-I))
dat=(W/'relative73_nc_data.m').read_text();PR=PolynomialRing(F2,'t');F=GF(2**9,name='a',modulus=PR(lit(dat,'RelativeNCPolynomial')));a=F(PR(lit(dat,'RelativeNCZeta')));assert a.multiplicative_order()==73;x=a/(1+a)**2;y=a*a/(1+a)**3;u3=x;u2=x;u4=x*x+y;v2=u2+(u4/u3)**2+u4/u3;b=v2**3/u3**2;c=(v2+u3)/u3;rv=b/c;sv=c*c/(b+c);tv=rv*sv+1;xu=(sv+rv)/tv;yu=tv/(sv*sv+sv+rv+1)
RX=matrix(F2,[[v>>j&1 for j in range(2*g)]for v in matbits(s,'UnitXRelations')]);RY=matrix(F2,[[v>>j&1 for j in range(2*g)]for v in matbits(s,'UnitYRelations')]);R=matrix(F,[[F(row[j])+u*F(row[g+j])for j in range(g)]for M,u in[(RX,xu),(RY,yu)]for row in M.rows()]);assert R.rank()==g-1;z=R.right_kernel().basis()[0];z/=next(v for v in z if v);assert z==vector(F,[F(PR(v))for v in lit(dat,'RelativeNCZ')]);SS=lit(dat,'RelativeSSMatrices');CJ=lit(dat,'RelativeCuspJets');assert len(SS)==4
for k,rr in enumerate(SS):
 zk=D.change_ring(F)**k*z;Bs=[]
 for A in AA:
  v=A.change_ring(F)*zk;Bs.append(matrix(F2,[list(a.polynomial())+[0]*(9-len(list(a.polynomial())))for a in v]))
 B=Bs[0]
 for B1 in Bs[1:]:B=B.stack(B1)
 assert B==matrix(F2,rr)and B.rank()==8
for k,rr in enumerate(CJ):
 Bs=[A*D**k*Q[:,1:11]for A in AA];C=Bs[0]
 for C1 in Bs[1:]:C=C.stack(C1)
 assert C==matrix(F2,rr)
out={'status':'PASS','degree':19,'base_degree':9,'base_rank':8,'translates':4,'cusp_jet_blocks':36,'all_entries_rebuilt':True};(W/'relative73_nc_intrinsic_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_RELATIVE73_NC_INTRINSIC_REPLAY_PASS',flush=True)
