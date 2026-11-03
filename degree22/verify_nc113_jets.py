from pathlib import Path
import json,hashlib
from sage.all import GF,PolynomialRing,PowerSeriesRing,ZZ,matrix,vector
from compact_records import compact
from unit_arithmetic import lit,decode_record
from intrinsic_model import Model,units
W=Path(__file__).resolve().parent;P2=PolynomialRing(GF(2),'t');M=Model(113)
def psi(xx,aa,N):
 a1,a2,a3,a4,a6=aa;b2=a1*a1;b4=a1*a3;b6=a3*a3;b8=a1*a1*a6+a1*a3*a4+a2*a3*a3+a4*a4;v=a1*xx+a3;R=xx.parent();pp=[R.zero(),R.one(),v,xx**4+b2*xx**3+b4*xx**2+b6*xx+b8,v*(b2*xx**5+b4*xx**4+(b2*b8+b4*b6)*xx+b4*b8+b6*b6)]
 for n in range(5,N+1):
  m=n//2;pp.append(pp[m+2]*pp[m]**3+pp[m-1]*pp[m+1]**3 if n%2 else pp[m]/v*(pp[m+2]*pp[m-1]**2+pp[m-2]*pp[m+1]**2))
 return pp[N]

s=compact((W/'nc113_jets.m').read_text());meta=lit(s,'SourceMetadata');recs=lit(s,'SourceRecords');assert len(meta)==len(recs)==1 and meta[0][:3]==(1,14,4)
r=decode_record(recs[0]);F=GF(2**r['F'].d,'a',modulus=P2(ZZ(r['F'].p).digits(2)));assert r['F'].d==28
cv=lambda z:F(P2(ZZ(z).digits(2)));aa=[cv(z)for z in r['ainv']];assert aa==[1,0,0,0,0]
dat=(W/'relative113_nc_data.m').read_text();assert P2(lit(dat,'Relative113NCField'))==P2(ZZ(r['F'].p).digits(2));zeta=F(P2(lit(dat,'Relative113NCZeta')));assert zeta.multiplicative_order()==113
assert [cv(z)for z in r['point']]==[zeta/(1+zeta)**2,zeta**2/(1+zeta)**3]
n=len(r['xjet']);assert n==8;PS=PowerSeriesRing(F,'u',default_prec=n,implementation='generic');u=PS.gen();xx=PS([cv(v)for v in r['xjet']]);yy=PS([cv(v)for v in r['yjet']]);ap=[PS(v)for v in aa];ap[4]+=u
assert psi(xx,ap,113).valuation()>=n and psi(PS(xx[0])+u,[PS(v)for v in aa],113)[1]!=0
assert (yy**2+xx*yy+xx**3+u).valuation()>=n
uv=units(ap,xx,yy);assert [v[0]for v in uv]==[cv(v)for v in r['units']];Z=matrix(F,[[cv(v)for v in row]for row in r['jets']]);assert(Z.nrows(),Z.ncols())==(477,8)
assert Z.column(0)==M.cv(F,[v[0]for v in uv]);ki=next(i for i,v in enumerate(Z.column(0))if v);assert Z[ki,0]==1 and all(Z[ki,j]==0 for j in range(1,n))and any(Z[i,1]for i in range(477))
for R,U in [(M.RX,uv[0]),(M.RY,uv[1])]:
 A=R[:,:M.g].change_ring(F);B=R[:,M.g:].change_ring(F);AZ=A*Z;BZ=B*Z
 for j in range(n):assert AZ.column(j)+sum((U[k]*BZ.column(j-k)for k in range(j+1)),vector(F,B.nrows()))==0
assert all(v**(2**14)==v for v in Z.list())
z=Z.column(0);normal=lambda v:v/next(x for x in v if x)
closed=lambda v:frozenset(tuple(x**(2**j)for x in v)for j in range(14))
orbits=[]
for k in range(5):
 v=normal(M.D.change_ring(F)**k*z);o=closed(v);assert len(o)==14
 if k<4:assert all(o.isdisjoint(a)for a in orbits);orbits.append(o)
 else:assert o==orbits[0]
for scalar,k in [(pow(M.root,-1,113),1),(3,-M.log(3))]:
 w=zeta**scalar;x=w/(1+w)**2;y=w*w/(1+w)**3;assert normal(M.D.change_ring(F)**k*z)==M.cv(F,units(aa,x,y))
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
out={'status':'PASS','N':113,'degree':14,'ambient_field_degree':28,'jets':8,'all_jet_coefficients_and_unit_relations_independently_verified':True,'normalized_nonzero_tangent':True,'canonical_jets_descend_to_degree14':True,'closed_diamond_orbit':4,'T3_NC_divisor':'3*C+delta3(C); hence A3(C)=2*C-2*delta3(C)','point_diamond_and_delta3_orientation_independently_checked':True,'local_parameter':'a6=u on the nodal model; discriminant=u and j=1/u','native_data_sha256':sha(W/'nc113_jets.m'),'native_source_sha256':sha(W/'build_nc113_jets.m'),'verifier_source_sha256':sha(Path(__file__))};(W/'nc113_jets_independent.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_NC113_NODAL_CUSP_JETS_INDEPENDENT_PASS',flush=True)
