"""Independent generic O8 obstruction and complete ordinary8 orbit split at113."""
from pathlib import Path
import json,gzip,re,hashlib,time
from sage.all import matrix,GF,ZZ
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;H=W/'full113';sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
while not ((H/'o8_delta2_sieve.json').exists()and'AUDIT_FULL_SIEVE_COMPLETE'in(H/'o8_delta2_sieve.log').read_text()):time.sleep(5)
a=json.loads((H/'o8_delta2_sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions']and a['nonprincipal']==a['source_orbits']==1
src=lit((W/'sources113.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ordinary=[(i+1,r[5])for i,r in enumerate(src)if r[0]==8 and r[6]];assert ordinary==[(2,7),(3,28)]
assert [(r['source'],r['degree'],r['orbit'],r['status'])for r in a['results']]==[(3,8,28,'NONPRINCIPAL')]
u=(H/'units_data.m').read_text();root=int(re.search(r'DiamondRoot:=(\d+)',u)[1]);log2=next(k for k in range(56)if pow(root,k,113)in[2,111]);assert a['alpha_coefficients']=={str(log2):1,'0':-1}
assert(a['section_degree'],a['dimension'],a['product_dimension'],a['precision'],a['Sturm_bound'])==(1,477,1428,2328,2128)
ms=json.load(gzip.open(H/'o8_delta2_matrices.json.gz','rt'));assert len(ms)==1;z=ms[0];assert z['source']==3 and z['rank']==477;A=matrix(GF(2),[ZZ(int(r,16)).digits(2,padto=z['columns'])for r in z['rows']]);assert A.rank()==477
out={'status':'PASS','N':113,'degree':22,'ordinary8_source_orbits':ordinary,'exceptional_H8_closed_diamond_orbit_size':7,'generic_closed_diamond_orbit_size':28,'generic_source':3,'annihilator':'(delta2-1)A3','independent_rank':477,'matrices':1,'added_SS7_and_NC14_blocks_fixed_by_delta2':True,'coverage':'generic O8 plus any delta2-invariant added SS7/NC14 blocks; the exceptional H8 O8 orbit is treated separately','sieve_sha256':sha(H/'o8_delta2_sieve.json'),'matrix_archive_sha256':sha(H/'o8_delta2_matrices.json.gz'),'native_input_sha256':sha(H/'small_hecke_jets.m'),'source_sha256':sha(W/'ordinary8_delta2_sieve.py')};(W/'o8_delta2_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_GENERIC_O8_113_DELTA2_OBSTRUCTION_PASS',477,flush=True)
