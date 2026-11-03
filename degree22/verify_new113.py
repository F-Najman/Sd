from pathlib import Path
import json,gzip,hashlib
from sage.all import GF,matrix,vector,ZZ,PolynomialRing
from intrinsic_model import Model,units,PR,F2,stack,coeff
from unit_arithmetic import lit,decode_record
from compact_records import compact
W=Path(__file__).resolve().parent;M=Model(113);s=(W/'relative113_nc_data.m').read_text();AA=[]
for q in[2,3,5]:
 T=M.hecke(q)
 if T is not None:
  Dq=M.D**M.log(q);AA.append((M.D**7-M.I)*(T-Dq-F2(q)*M.I)*(T-M.I-F2(q)*Dq))
assert len(AA)==2
F,zo,orb=M.point(8,True,7);assert orb==7;assert zo==vector(F,[F(PR(v))for v in lit(s,'Relative113NCOrdZ')]);K=GF(2**28,'a',modulus=PR(lit(s,'Relative113NCField')));zeta=K(PR(lit(s,'Relative113NCZeta')));assert zeta.multiplicative_order()==113
zn=M.cv(K,units([K(1),K(0),K(0),K(0),K(0)],zeta/(1+zeta)**2,zeta*zeta/(1+zeta)**3));assert zn==vector(K,[K(PR(v))for v in lit(s,'Relative113NCZ')])and all(v**(2**14)==v for v in zn)
gamma=K(PR(lit(s,'Relative113NCSmallImage')));assert list(gamma.minpoly())==list(PR(lit(s,'Relative113NCSmallField')));basis=matrix(F2,[list((gamma**i)._vector_())for i in range(14)]);assert basis.rank()==14
BB=[]
for A in AA:
 O=coeff(A.change_ring(F)*zo,8);v=A.change_ring(K)*zn;NC=matrix(F2,[basis.solve_left(vector(F2,x._vector_()))for x in v]);BB.append(O.augment(NC))
B=stack(BB);assert B==matrix(F2,lit(s,'Relative113NCBase'))and B.rank()==21 and B[:,:8].rank()==7 and B[:,8:].rank()==14
# The ordinary H8 orbit is free, and the NC closed orbit has length4.
H=M.D.change_ring(F)**7;v=zo
for k in range(1,9):
 v=H*v;v/=next(a for a in v if a)
 assert(v==zo)==(k==8)
nc_closed=[]
for k in range(1,5):
 v=M.D.change_ring(K)**k*zn;v/=next(a for a in v if a);fixed=any(v==vector(K,[z**(2**j)for z in zn])for j in range(14));assert fixed==(k==4);nc_closed.append(fixed)
# gcd(7,4)=1 makes this representative cover every relative closed position.
H=W/'ss_pair113'
census=next(v for v in json.loads((W/'census_counts_independent.json').read_text())['results']if v['p']==113)
assert [v for v in census['supersingular_closed_diamond_orbits']if v[0]==7]==[[7,4]]
native=compact((H/'hecke_jets.m').read_text());md=lit(native,'SourceMetadata');ss=lit(native,'SourceRecords');assert len(md)==len(ss)==1 and md[0][:3]==(1,7,4)
r=decode_record(ss[0]);K=GF(2**r['F'].d,'b',modulus=PR(ZZ(r['F'].p).digits(2)));cv=lambda z:K(PR(ZZ(z).digits(2)));assert r['F'].d==7
z=vector(K,[cv(v)for v in r['z']]);assert z==M.cv(K,units([cv(v)for v in r['ainv']],*[cv(v)for v in r['point']]))
orb=lambda v:frozenset(tuple(x**(2**j)for x in v)for j in range(7))
closed=[]
for k in range(5):
 v=M.D.change_ring(K)**k*z;v/=next(x for x in v if x);o=orb(v);assert len(o)==7
 if k<4:assert all(o.isdisjoint(prev)for prev in closed);closed.append(o)
 else:assert o==closed[0]
# The single independent closed diamond orbit contains exactly four points.
# Under simultaneous diamond translation, unordered pairs have offsets0,1,2.
a=json.loads((H/'pair_sieve.json').read_text());assert [v['source']for v in a['results']]==[[1,1,0],[1,1,1],[1,1,2]]
sscheck=json.loads((W/'ss113_jets_independent.json').read_text());assert sscheck['status']=='PASS'and sscheck['results'][0]['sources']==[1]and sscheck['results'][0]['all_jet_coefficients_verified']and sscheck['results'][0]['independent_isogenies_verified']
assert a['status']=='PASS'and not a['exceptions']and a['tasks']==3;ms=json.load(gzip.open(H/'pair_matrices.json.gz','rt'));assert len(ms)==3
for z in ms:
 A=matrix(F2,[ZZ(int(r,16)).digits(2,padto=z['columns'])for r in z['rows']]);assert A.rank()==477==z['rank']
out={'status':'PASS','degree':22,'N':113,'O8_plus_NC14':{'rank':21,'family_dimension':1,'ordinary_block_rank':7,'NC_block_rank':14,'all_entries_independently_rebuilt':True,'ordinary_H8_geometric_orbit':8,'ordinary_closed_orbit':7,'NC_closed_orbit':4,'all_relative_positions':True,'zero_family':'H8 ordinary pullback plus a fixed degree14 cuspidal divisor; contradicts noncuspidal support'},'O8_plus_two_SS7':{'SS_pair_relative_positions':[0,1,2],'principal_obstruction_matrices':3,'independent_rank':477,'annihilator':'(D^7-1)A3','ordinary_H8_block_zero_as_divisor':True},'NC_data_sha256':hashlib.sha256((W/'relative113_nc_data.m').read_bytes()).hexdigest(),'SS7_closed_points_independently_complete':4,'SS7_unordered_pair_offsets_complete':[0,1,2],'SS113_independent_jet_certificate_sha256':hashlib.sha256((W/'ss113_jets_independent.json').read_bytes()).hexdigest(),'SS_pair_matrix_archive_sha256':hashlib.sha256((H/'pair_matrices.json.gz').read_bytes()).hexdigest()};(W/'new113_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_NEW_113_SUPPORTS_INDEPENDENTLY_RESOLVED',flush=True)
