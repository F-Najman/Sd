"""Independent intrinsic quotient cotangents and all degree-three ranks."""
from pathlib import Path
import json,itertools,time
from sage.all import GF,matrix,vector,PolynomialRing,PowerSeriesRing,ZZ
from intrinsic_model import Model,stack,coeff,units,F2,PR
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;start=time.monotonic();M=Model(127);g=M.g
s=(W/'quotient127_cusps_data.m').read_text();V=matrix(F2,lit(s,'Q127InvariantBasis'));assert V.rank()==V.nrows()==88 and V*(M.D**9-M.I)==0 and (M.D**9-M.I).nullity()==88
qs=lit(s,'Q127HeckePrimes');F=GF(2**7,name='a',modulus=PR(lit(s,'Q127NCPolynomial')));a=F(PR(lit(s,'Q127Zeta')));assert a.multiplicative_order()==127
PS=PowerSeriesRing(F,'u',default_prec=5);u=PS.gen();x=PS(a/(1+a)**2);y=PS(a*a/(1+a)**3);s1=PS(0);a6=PS(0)
for n in range(1,5):
 z=u**n*a;w=u**n/a;x+=z/(1+z)**2+w/(1+w)**2;y+=z*z/(1+z)**3+w/(1+w)**3;s1+=F(n%2)*u**n/(1+u**n);a6+=F(((5*n**3+7*n**5)//12)%2)*u**n/(1+u**n)
y+=s1;assert(y*y+x*y+x**3+s1*x+a6).valuation()>=5
uv=units([PS(1),PS(0),PS(0),s1,a6],x,y);Z=matrix(F,[[F(PR(v))for v in row]for row in lit(s,'Q127NCJets')]);assert Z.nrows()==g and Z.ncols()==5
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
RC=lit(s,'Q127RC');NC=lit(s,'Q127NC');blocks=[]
for k in range(9):
 assert stack([A*M.D**k*M.Q[:,1:6]for A in AA])==matrix(F2,RC[k])
 Zk=M.D.change_ring(F)**k*Z;VZ=V.change_ring(F)*Zk;ii=next(i for i in range(88)if VZ[i,0]);den=PS(list(VZ.row(ii)));out=[]
 for A in AA:
  AZ=A.change_ring(F)*Zk
  for row in AZ.rows():
   vals=PS(list(row))/den;assert all(vals[j]in F2 for j in range(5));out.append([F2(vals[j])for j in range(5)])
 assert matrix(F2,out)==matrix(F2,NC[k]),('NC',k)
blocks=[matrix(F2,r)for r in RC+NC];cnt=0
for pos in itertools.combinations_with_replacement(range(18),3):
 counts={i:pos.count(i)for i in set(pos)};A=None
 for i,c in counts.items():A=blocks[i][:,:c]if A is None else A.augment(blocks[i][:,:c])
 assert A.rank()==3;cnt+=1
assert cnt==1140;print('S21_QUOTIENT127_CUSPS_INTRINSIC_PASS',cnt,round(time.monotonic()-start,1),flush=True)
ss=(W/'quotient127_ss_data.m').read_text();K,z,orb=M.point(14,False,3);assert list(K.modulus())==[K.base_ring()(v)for v in lit(ss,'Q127SSField')];assert z==vector(K,[K(PR(v))for v in lit(ss,'Q127SSZ')]);bb=K(PR(lit(ss,'Q127SSOmega')));assert bb.multiplicative_order()==3
assert M.D.change_ring(K)**21*z==next(v for v in M.D.change_ring(K)**21*z if v)*z # normalization first nonzero z=1
AS=[V*(M.D**3-M.I)*(M.hecke(q)-M.D**M.log(q)-F2(q)*M.I)for q in lit(ss,'Q127SSPrimes')];SS=lit(ss,'Q127SS');CR=lit(ss,'Q127SSCusps');sb=[];cb=[]
for k in range(3):
 zk=M.D.change_ring(K)**k*z;vz=V.change_ring(K)*zk;raw=vector(K,[v for A in AS for v in A.change_ring(K)*zk]);native=vector(K,[K(r[0])+K(r[1])*bb for r in SS[k]]);ii=next(i for i,v in enumerate(native)if v);den=raw[ii]/native[ii];assert den in vz and den!=0;out=[]
 for A in AS:
  for v in A.change_ring(K)*zk/den:
   assert v**4==v;c=[K(0),K(1),bb,bb+1].index(v);out.append([c%2,c//2])
 B=matrix(F2,out);assert B==matrix(F2,SS[k])and B.rank()==2;sb.append(B)
for k in range(9):
 B=stack([A*M.D**k*M.Q[:,1:2]for A in AS]);assert B==matrix(F2,CR[k]);cb.append(B)
for A,B in itertools.product(sb,cb):assert A.augment(B).rank()==3
print('S21_QUOTIENT127_SS_INTRINSIC_PASS',27,round(time.monotonic()-start,1),flush=True)
# The two-pullback disk upstairs has base degree16 and rank14.
rs=(W/'relative127_data.m').read_text();O,zo,oo=M.point(9,True,7);assert oo==7
AP=[(M.D**7-M.I)*(M.D**M.log(2)-M.I)*(M.hecke(q)-M.D**M.log(q)-F2(q)*M.I)for q in[2,3,5]if M.hecke(q)is not None]
B=stack([coeff(A.change_ring(O)*zo,9).augment(coeff(A.change_ring(F)*z0,7))for A in AP]);assert B==matrix(F2,lit(rs,'Relative127Base'))and B.rank()==14
CJ=lit(rs,'Relative127CuspJets')
for k,rr in enumerate(CJ):assert stack([A*M.D**k*M.Q[:,1:6]for A in AP])==matrix(F2,rr)
(W/'quotients_intrinsic_verified.json').write_text(json.dumps({'status':'PASS','degree':21,'quotient_genus':88,'all_invariant_form_entries_rebuilt':True,'tate_jets_rebuilt':5,'pure_cusp_patterns':cnt,'supersingular_cusp_patterns':27,'relative127_base_rank':14,'relative127_cusp_blocks':63},indent=2)+'\n');print('S21_QUOTIENT_INTRINSIC_COMPLETE',round(time.monotonic()-start,1),flush=True)
