"""Independent intrinsic quotient cotangents and all degree-three ranks."""
from pathlib import Path
import json,itertools,time
from sage.all import GF,matrix,vector,PolynomialRing,PowerSeriesRing,ZZ
from intrinsic_model import Model,stack,coeff,units,F2,PR
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;start=time.monotonic();M=Model(89);g=M.g
s=(W/'quotient89_cusps_data.m').read_text();V=matrix(F2,lit(s,'Q89InvariantBasis'));assert V.rank()==V.nrows()==27 and V*(M.D**4-M.I)==0 and (M.D**4-M.I).nullity()==27
qs=lit(s,'Q89HeckePrimes');F=GF(2**11,name='a',modulus=PR(lit(s,'Q89NCPolynomial')));a=F(PR(lit(s,'Q89Zeta')));assert a.multiplicative_order()==89
PS=PowerSeriesRing(F,'u',default_prec=5);u=PS.gen();x=PS(a/(1+a)**2);y=PS(a*a/(1+a)**3);s1=PS(0);a6=PS(0)
for n in range(1,5):
 z=u**n*a;w=u**n/a;x+=z/(1+z)**2+w/(1+w)**2;y+=z*z/(1+z)**3+w/(1+w)**3;s1+=F(n%2)*u**n/(1+u**n);a6+=F(((5*n**3+7*n**5)//12)%2)*u**n/(1+u**n)
y+=s1;assert(y*y+x*y+x**3+s1*x+a6).valuation()>=5
uv=units([PS(1),PS(0),PS(0),s1,a6],x,y);Z=matrix(F,[[F(PR(v))for v in row]for row in lit(s,'Q89NCJets')]);assert Z.nrows()==g and Z.ncols()==5
z0=vector(F,Z.column(0));assert z0==M.cv(F,[uv[0][0],uv[1][0]])
for R,U in [(M.RX,uv[0]),(M.RY,uv[1])]:
 A=R[:,:g].change_ring(F);B=R[:,g:].change_ring(F)
 for n in range(5):assert A*Z.column(n)+sum((U[j]*(B*Z.column(n-j))for j in range(n+1)),vector(F,B.nrows()))==0
# Rank g-1 and fixed first nonzero coordinate imply that these are the unique
# canonical-coordinate jets satisfying the independently reconstructed units.
ki=next(i for i,v in enumerate(z0)if v);assert list(Z.row(ki))==[F(1),F(0),F(0),F(0),F(0)]
AA=[]
for q in qs:
 T=M.hecke(q);Dq=M.D**M.log(q);AA.append(V*(M.D-M.I)*(T-Dq-F2(q)*M.I)*(T-M.I-F2(q)*Dq))
RC=lit(s,'Q89RC');NC=lit(s,'Q89NC');blocks=[]
for k in range(4):
 assert stack([A*M.D**k*M.Q[:,1:6]for A in AA])==matrix(F2,RC[k])
 Zk=M.D.change_ring(F)**k*Z;VZ=V.change_ring(F)*Zk;ii=next(i for i in range(88)if VZ[i,0]);den=PS(list(VZ.row(ii)));out=[]
 for A in AA:
  AZ=A.change_ring(F)*Zk
  for row in AZ.rows():
   vals=PS(list(row))/den;assert all(vals[j]in F2 for j in range(5));out.append([F2(vals[j])for j in range(5)])
 assert matrix(F2,out)==matrix(F2,NC[k]),('NC',k)
(W/'quotient89_intrinsic_verified.json').write_text(json.dumps({'status':'PASS','degree':22,'genus':27,'all_invariant_forms_and_operators_rebuilt':True,'Tate_jet_precision':5,'rational_cusp_blocks':4,'other_cusp_blocks':4,'Hecke_primes':qs},indent=2)+'\n');print('S22_QUOTIENT89_INTRINSIC_COMPLETE',flush=True)
