"""Independent ranks and exhaustive generic O8 mixed-support coverage at113."""
from pathlib import Path
import json,gzip,re,time,hashlib
from sage.all import GF,matrix,vector,ZZ,EllipticCurve
from intrinsic_model import Model,units,PR
from unit_arithmetic import lit,decode_record
from compact_records import compact
W=Path(__file__).resolve().parent;H=W/'generic113_mixed';sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
while not(W/'nc113_jets_independent.json').exists():time.sleep(5)
c=json.loads((W/'nc113_jets_independent.json').read_text());assert c['status']=='PASS'and c['native_data_sha256']==sha(W/'nc113_jets.m')and c['native_source_sha256']==sha(W/'build_nc113_jets.m')and c['verifier_source_sha256']==sha(W/'verify_nc113_jets.py')
assert'AUDIT_FULL_SIEVE_COMPLETE'in(H/'sieve.log').read_text();a=json.loads((H/'sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions']and a['tasks']==a['nonprincipal']==14 and a['alpha_coefficients']=={'1':1,'0':-1}
assert(a['section_degree'],a['dimension'],a['product_dimension'],a['precision'],a['Sturm_bound'])==(1,477,1428,2328,2128)
M=Model(113);ordinary=[(i+1,r[5])for i,r in enumerate(M.sources)if r[0]==8 and r[6]];assert ordinary==[(2,7),(3,28)]
count=next(v for v in json.loads((W/'census_counts_independent.json').read_text())['results']if v['p']==113)
assert [v for v in count['supersingular_closed_diamond_orbits']if v[0]==7]==[[7,4]]
assert all(v['rational_ordinary_points']==0 for v in count['ordinary_counts']if v['degree']<8)and next(v['rational_ordinary_points']for v in count['ordinary_counts']if v['degree']==8)==280
assert 280//8==7+28 and next(k for k in range(1,113)if pow(2,k,113)in[1,112])==14 and 56//14==4 and 28%4==0
b=compact((W/'full113/small_hecke_jets.m').read_text());md=lit(b,'SourceMetadata');sr=lit(b,'SourceRecords');idx=next(i for i,v in enumerate(md)if v[:3]==(3,8,28));r=decode_record(sr[idx]);F=GF(2**r['F'].d,'b',modulus=PR(ZZ(r['F'].p).digits(2)));assert r['F'].d==8;cv=lambda z:F(PR(ZZ(z).digits(2)));aa=[cv(v)for v in r['ainv']];E=EllipticCurve(aa);P=E([cv(v)for v in r['point']]);assert 113*P==E(0)and P!=E(0)
z=vector(F,[cv(v)for v in r['z']]);assert z==M.cv(F,units(aa,P[0],P[1]));normal=lambda v:v/next(x for x in v if x);closed=lambda v:frozenset(tuple(x**(2**j)for x in v)for j in range(8));seen=[]
for k in range(29):
 v=normal(M.D.change_ring(F)**k*z);o=closed(v);assert len(o)==8
 if k<28:assert all(o.isdisjoint(q)for q in seen);seen.append(o)
 else:assert o==seen[0]
expected={tuple(['O8_generic','NC14',k])for k in range(4)}|{tuple(['O8_generic','SS7_pair',i,j])for i in range(4)for j in range(i,4)}
assert {tuple(v['source'])for v in a['results']}==expected and all(v['degree']==22 and v['status']=='NONPRINCIPAL'and v['rank']==477 for v in a['results'])
ms=json.load(gzip.open(H/'matrices.json.gz','rt'));assert len(ms)==14 and{tuple(v['source'])for v in ms}==expected
for v in ms:
 A=matrix(GF(2),[ZZ(int(r,16)).digits(2,padto=v['columns'])for r in v['rows']]);assert A.rank()==v['rank']==477
out={'status':'PASS','N':113,'degree':22,'ordinary8_source_orbits':ordinary,'generic_ordinary_closed_orbit_independently_rebuilt':28,'independent_closed_ordinary8_count':35,'SS7_closed_points':4,'NC14_closed_points':4,'generic_stabilizer_acts_trivially_on_both_closed_orbits':True,'NC_relative_positions':4,'unordered_SS_pair_positions':10,'cases':14,'matrices':14,'independent_rank':477,'annihilator':'(D-1)A3','cusp_formula':'T3(C)=3*C+delta3(C); A3(C)=2*C-2*delta3(C)','matrix_archive_sha256':sha(H/'matrices.json.gz'),'sieve_sha256':sha(H/'sieve.json'),'native_input_sha256':{f:sha(W/f)for f in ['full113/small_hecke_jets.m','ss_pair113/hecke_jets.m','nc113_jets.m']},'NC_independent_certificate_sha256':sha(W/'nc113_jets_independent.json'),'producer_source_sha256':sha(W/'generic113_mixed_sieve.py'),'verifier_source_sha256':sha(Path(__file__))};(W/'generic113_mixed_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_GENERIC113_ALL14_MIXED_SUPPORTS_INDEPENDENT_PASS',flush=True)
