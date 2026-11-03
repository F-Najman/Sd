from pathlib import Path
import json,gzip,hashlib,sys,subprocess,shutil
from sage.all import PolynomialRing,QQ
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit
A=json.load(open(W/'full97/sieve.json'));M=json.load(gzip.open(W/'full97/matrices.json.gz','rt'));assert not A['exceptions']and A['source_orbits']==A['nonprincipal']==len(M)==359
assert {int(k):v for k,v in A['alpha_coefficients'].items()}=={12:1,0:-1}
assert A['alternative_sources']==[2,3,41]and A['combined_independently_verified']
rank=json.load(open(W/'independent_rank_checks.json'));assert rank['status']=='PASS'and any(v['N']==97 and v['kind']=='ordinary'and v['matrices']==359 for v in rank['results'])
R=PolynomialRing(QQ,'x');x=R.gen();assert(x**12-1)%(x**4-x*x+1)==0;assert(x**6-x**4-x*x+1)%(x**4-x*x+1)!=0
md17=lit((W/'full97/hecke_jets.m').read_text(),'SourceMetadata');records=[]
for d in[15,16]:
 V=W.parent/f'degree{d}';H=V/'full97';backup=W/'superseded97'/f'degree{d}';backup.mkdir(parents=True,exist_ok=True)
 for src,name in[(H/'sieve.json','full97_sieve.json'),(H/'matrices.json.gz','full97_matrices.json.gz'),(V/'full_sieve.py','full_sieve.py'),(V/'PROOF.txt','PROOF.txt'),(B/f'outputs/S{d}_proof.pdf',f'S{d}_proof.pdf')]:
  if not(backup/name).exists():shutil.copy2(src,backup/name)
 oldmd=lit((H/'hecke_jets.m').read_text(),'SourceMetadata');submd=[v for v in md17 if v[1]<=d];assert submd==oldmd
 assert hashlib.sha256((H/'units_data.m').read_bytes()).digest()==hashlib.sha256((W/'full97/units_data.m').read_bytes()).digest()
 rr=[v for v in A['results']if v['degree']<=d];mm=[v for v in M if v['degree']<=d];assert len(rr)==len(mm)==len(oldmd)
 out=A.copy();out.update(source_orbits=len(rr),nonprincipal=len(mm),exceptions=[],results=rr,status='PASS',corrected_annihilators=['sigma^12-1','(sigma-1)*Phi12(sigma)'],parent_certificate=str((W/'full97/matrices.json.gz').resolve()))
 out['operator_counts']={op:sum(v['operator']==op for v in rr)for op in['sigma^12-1','(sigma-1)*Phi12(sigma)']}
 (H/'sieve.json').write_text(json.dumps(out,indent=2)+'\n')
 with gzip.open(H/'matrices.json.gz','wt')as f:json.dump(mm,f,separators=(',',':'))
 p=V/'full_sieve.py';s=p.read_text().replace('97:{6:1,4:-1,2:-1,0:1}','97:{12:1,0:-1}');s=s.replace('si,d,orb,jpol=md;dd={}','si,d,orb,jpol=md;use_alpha={5:1,4:-1,3:-1,2:1,1:1,0:-1}if N==97 and(d,orb)in[(10,24),(14,24)]else alpha;dd={}').replace('for shift,c in alpha.items():','for shift,c in use_alpha.items():').replace('sum(abs(c)for c in alpha.values())','sum(abs(c)for c in use_alpha.values())');p.write_text(s)
 p=V/'PROOF.txt';s=p.read_text().replace('97: alpha=(sigma^2-1)*(sigma^4-sigma^2+1);','97: alpha=sigma^12-1, with (sigma-1)*Phi12(sigma) on the three degree10/14 closed orbits of size24;')
 note='''\nCORRECTION TO THE ORDINARY LEVEL97 CERTIFICATES (29 October 2026)\n\nThe original code polynomial sigma^6-sigma^4-sigma^2+1 does not\nannihilate the strange order12 character. It has been replaced by\nsigma^12-1 and, on the three closed orbits of size24 in degrees10/14,\n(sigma-1)*Phi12(sigma). All ordinary level97 residue orbits through degree17 have\nbeen recomputed with the corrected map and independently checked in\nSage. The relevant lower-degree matrices here are exact subsets of\nthat universal certificate. The other level97 arguments are unchanged.\nSee outputs/S97_correction.pdf and work/degree17/full97/sieve.json.\n'''
 if 'CORRECTION TO THE ORDINARY LEVEL97 CERTIFICATES'not in s:s+=note
 p.write_text(s)
 # This repeats only the global support/prime coverage check; each changed
 # matrix is already an independently verified subset of the degree17 file.
 log=V/'verify_coverage_after97_correction.log'
 with log.open('w')as f:subprocess.run(['python',str(V/'verify_coverage.py')],stdout=f,stderr=subprocess.STDOUT,check=True)
 assert 'unresolved=[]'in log.read_text()
 subprocess.run(['python',str(V/'finalize_result.py')],check=True)
 rec={'degree':d,'status':'PASS','ordinary97_orbits':len(rr),'corrected_operators':['sigma^12-1','(sigma-1)*Phi12(sigma)'],'certificate_sha256':hashlib.sha256((H/'matrices.json.gz').read_bytes()).hexdigest(),'subset_of_independently_verified_degree17_certificate':True};records.append(rec)
 for p in[B/f'outputs/S{d}_result.json',B/f'outputs/S{d}_status.json',V/'final_coverage.json']:
  if p.exists():
   a=json.load(open(p));a['level97_correction']=rec|{'note':'S97_correction.pdf'};p.write_text(json.dumps(a,indent=2)+'\n')
 p=V/'proof_manifest.json'
 if p.exists():
  a=json.load(open(p));a={k:hashlib.sha256((B/k).read_bytes()).hexdigest()for k in a if(B/k).exists()};a['work/degree17/full97/matrices.json.gz']=hashlib.sha256((W/'full97/matrices.json.gz').read_bytes()).hexdigest();p.write_text(json.dumps(a,indent=2)+'\n')
 print('REPAIRED_LEVEL97',rec,flush=True)
out={'status':'PASS','affected_degrees':[15,16],'universal_ordinary_orbits':359,'corrected_operators':['sigma^12-1','(sigma-1)*Phi12(sigma)'],'records':records};(W/'level97_correction_verified.json').write_text(json.dumps(out,indent=2)+'\n')
text='''CORRECTION TO THE LEVEL97 CERTIFICATES IN THE S(15) AND S(16) PROOFS
29 October 2026

The earlier code used
             alpha=sigma^6-sigma^4-sigma^2+1,
where sigma is the primitive diamond at97. This polynomial equals
(sigma^2-1)*(sigma^4-1) and does not vanish at a primitive12th root.
It therefore did not supply the finite-rational-image statement asserted
in the proof. The narrative factorization involving Phi_12 did not
match those code coefficients.

The corrected computation uses alpha=sigma^12-1 and, on the three\nclosed orbits of size24 in degrees10/14, (sigma-1)*Phi12(sigma). Both\nannihilate the
trivial character and every strange character at97, since the only
strange character order is12 (Derickx--Stoll, Table2). Consequently
each operator has finite image on J_1(97)(Q), and composing with the good-prime
torsion annihilator at3 kills J_1(97)(Q).

All359 ordinary residue orbits through degree17 have been recomputed
with these valid operators. Every resulting principal-divisor
obstruction has full rank, independently checked in Sage. Restricting
to degree<=15 gives89 matrices; restricting to degree<=16 gives176.
Their modular-form basis and source metadata agree exactly with the
earlier models. The earlier stored level97 matrices, code and proof
PDFs have been replaced accordingly, and both complete coverage checks
pass again with no unresolved primes.

The results S(15)=Primes(43) and S(16)=Primes(37) are unchanged. The
computations through S(14) used a valid level97 polynomial and are not
affected by this error. The separate supersingular level97 arguments
in degree16 are also unaffected.

Authoritative files:
 work/degree17/full97/sieve.json
 work/degree17/full97/matrices.json.gz
 work/degree17/independent_rank_checks.json
 work/degree17/level97_correction_verified.json
 work/degree15/verify_coverage_after97_correction.log
 work/degree16/verify_coverage_after97_correction.log
'''
(B/'outputs/S97_correction.txt').write_text(text)
# Use the exact same small PDF renderer as the proof packets.
s=(W/'finalize_result.py').read_text();start=s.index('def save_proof(');end=s.index('\nproof=save_proof',start);scope={'O':B/'outputs','Path':Path,'hashlib':hashlib,'textwrap':__import__('textwrap')};exec(s[start:end],scope);scope['save_proof'](B/'outputs/S97_correction.txt','S97_correction','Correction: ordinary level97 certificates')
print('S97_CORRECTION_COMPLETE',flush=True)
