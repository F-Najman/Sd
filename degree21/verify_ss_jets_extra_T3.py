"""Sage replay of new supersingular deformation and Hecke data."""
from pathlib import Path
import json,time,collections
from sage.all import GF,PolynomialRing,PowerSeriesRing,EllipticCurve,ZZ,matrix,vector
from compact_records import compact
from unit_arithmetic import lit,decode_record
from intrinsic_model import Model,units
W=Path(__file__).resolve().parent;start=time.monotonic();P2=PolynomialRing(GF(2),'t');out=[]
def psi(xx,aa,N):
 a1,a2,a3,a4,a6=aa;b2=a1*a1;b4=a1*a3;b6=a3*a3;b8=a1*a1*a6+a1*a3*a4+a2*a3*a3+a4*a4;v=a1*xx+a3;R=xx.parent();pp=[R.zero(),R.one(),v,xx**4+b2*xx**3+b4*xx**2+b6*xx+b8,v*(b2*xx**5+b4*xx**4+(b2*b8+b4*b6)*xx+b4*b8+b6*b6)]
 for n in range(5,N+1):
  m=n//2;pp.append(pp[m+2]*pp[m]**3+pp[m-1]*pp[m+1]**3 if n%2 else pp[m]/v*(pp[m+2]*pp[m-1]**2+pp[m-2]*pp[m+1]**2))
 return pp[N]
def primevec(a):
 if hasattr(a,'_vector_'):return vector(GF(2),a._vector_())
 K=a.parent();cs=list(a.list());cs += [K.base_ring().zero()]*(K.degree()-len(cs));return vector(GF(2),[v for c in cs for v in primevec(c)])
def keyuv(uv):
 # Canonical joint Frobenius-orbit key, including fields given as towers.
 import math
 a,b=uv;ambient=len(primevec(a));ds=[e for e in range(1,ambient+1)if ambient%e==0];d=math.lcm(next(e for e in ds if a**(2**e)==a),next(e for e in ds if b**(2**e)==b));proper=[e for e in range(1,d)if d%e==0];gamma=next(c for c in[a,b,a+b]if all(c**(2**e)!=c for e in proper));base=matrix(GF(2),[primevec(gamma**i)for i in range(d)]);assert base.rank()==d
 pol=tuple(map(int,base.solve_left(primevec(gamma**d))))+(1,);return(pol,tuple(map(int,base.solve_left(primevec(a)))),tuple(map(int,base.solve_left(primevec(b)))))
for N,tag,ell,selected in[(127,'ss127',3,{22,23,24,25})]:
 M=Model(N);s=compact((W/tag/'hecke_jets.m').read_text());meta=lit(s,'SourceMetadata');sr=lit(s,'SourceRecords');tr=lit(s,'SourceHeckeRecords');checked=0;targets=0
 for md,src,trs in zip(meta,sr,tr):
  if md[0]not in selected:continue
  for ri,rec in enumerate([src]+[r[3]for r in trs]):
   print('S21_SS_JET_RECORD_START',tag,md[0],ri,flush=True)
   r=decode_record(rec);F=GF(2**r['F'].d,'a',modulus=P2(ZZ(r['F'].p).digits(2)));cv=lambda z:F(P2(ZZ(z).digits(2)));aa=[cv(v)for v in r['ainv']];E=EllipticCurve(aa);P=E([cv(v)for v in r['point']]);assert N*P==E(0)and P!=E(0);n=len(r['xjet']);PS=PowerSeriesRing(F,'u',default_prec=n,implementation='generic');u=PS.gen();xx=PS([cv(v)for v in r['xjet']]);yy=PS([cv(v)for v in r['yjet']]);ap=[PS(v)for v in aa];ap[0]+=u;assert aa[0]==0 and aa[2]!=0
   assert psi(xx,ap,N).valuation()>=n
   PX=PolynomialRing(F,'X',implementation='generic');ours=PX(psi(PX.gen(),[PX(v)for v in aa],N));theirs=PX(E.division_polynomial(N,x=PX.gen()));assert ours==theirs,(N,ri,ours.degree(),theirs.degree(),ours.leading_coefficient(),theirs.leading_coefficient(),ours.monic()==theirs.monic())
   assert psi(PS(P[0])+u,[PS(v)for v in aa],N)[1]!=0
   assert (yy**2+ap[0]*xx*yy+ap[2]*yy+xx**3+ap[1]*xx**2+ap[3]*xx+ap[4]).valuation()>=n
   uv=units(ap,xx,yy);assert [v[0]for v in uv]==[cv(v)for v in r['units']];Z=matrix(F,[[cv(v)for v in row]for row in r['jets']]);assert Z.ncols()==n and Z.nrows()==M.g;assert Z.column(0)==M.cv(F,[v[0]for v in uv]);ki=next(i for i,v in enumerate(Z.column(0))if v);assert Z[ki,0]==1 and all(Z[ki,j]==0 for j in range(1,n));assert any(Z[i,1]for i in range(M.g))
   for R,U in[(M.RX,uv[0]),(M.RY,uv[1])]:
    A=R[:,:M.g].change_ring(F);B=R[:,M.g:].change_ring(F)
    AZ=A*Z;BZ=B*Z
    for j in range(n):assert AZ.column(j)+sum((U[k]*BZ.column(j-k)for k in range(j+1)),vector(F,B.nrows()))==0
   if ri==0:source=(F,E,P)
   checked+=1
  F,E,P=source;expected=collections.Counter();factors=E.division_polynomial(ell).factor();assert all(e==1 for f,e in factors)and sum(f.degree()for f,e in factors)==(ell*ell-1)//2
  # The chosen SS cases have every cyclic kernel defined over the source field.
  for f,e in factors:
   if ell==3:
    deg=f.degree()
    if deg==1:K=F;root=-f[0]/f[1];EL=E;PL=P
    else:
     K=F.extension(f,'c');root=K.gen();EL=E.change_ring(K);PL=EL([K(P[0]),K(P[1])])
    R=PolynomialRing(K,'X');phi=EL.isogeny(R.gen()-root);Q=phi(PL);expected[keyuv(units(phi.codomain().a_invariants(),Q[0],Q[1]))]+=deg
   else:
    assert f.degree()==(ell-1)//2;phi=E.isogeny(f);Q=phi(P);expected[keyuv(units(phi.codomain().a_invariants(),Q[0],Q[1]))]+=1
  assert sum(expected.values())==ell+1
  actual=collections.Counter()
  for e,td,mul,rec in trs:
   r=decode_record(rec);K=GF(2**r['F'].d,'b',modulus=P2(ZZ(r['F'].p).digits(2)));actual[keyuv([K(P2(ZZ(v).digits(2)))for v in r['units']])]+=e
  assert actual==expected,(tag,md[0],actual,expected);targets+=len(trs)
  print('S21_SS_JETS_HECKE_SOURCE_PASS',tag,md[0],checked,round(time.monotonic()-start,1),flush=True)
 out.append({'case':tag,'sources':sorted(selected),'records':checked,'hecke_targets':targets,'all_jet_coefficients_verified':True,'independent_isogenies_verified':True})
(W/'ss_jets_extra_T3_verified.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n');print('S21_SS_JETS_EXTRA_T3_COMPLETE',flush=True)
