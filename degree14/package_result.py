from pathlib import Path
import json,hashlib,zipfile
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';L=Path('/home/fnajman/degree9_torsion/nonic-torsion');A=Path('/home/fnajman/Documents/Codex/2026-10-21/on-this-computer-there-are-files/work/asymptotic_torsion')
assert json.load(open(W/'final_coverage.json'))['status']=='PASS'
files={}
def add(p,arc=None):
 p=Path(p);assert p.is_file(),p;files[arc or str(p.relative_to(B))]=p
skip={'setup_models_new.py','prepare_ss127.py','unit_poles.m','unit_poles.log','check_127_fi.py','check_97_fi.py','check_67_fi.py','package_result.log','package_verified.json','check_packet.log','packet_portability.json'}
for p in W.rglob('*'):
 if not p.is_file()or '__pycache__'in p.parts or 'full127'in p.parts or p.name in skip:continue
 if p.parent.name=='FI'and(p.name.startswith('FI127')or p.name in['FI97.txt','FI97.compressed.txt','FI97_export.log']):continue
 if p.suffix in['.m','.py','.cpp','.txt','.json','.gz','.log']:add(p)
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
for n in ns:
 # The exact earlier jets, their generators, and the matching canonical bases.
 for name in['units_data.m','hecke_jets.m','stage2.m','stage2.log']:add(B/f'work/degree13/full{n}'/name)
 add(B/f'work/degree13/sources{n}.m')
 old=B/('work/degree13'if n==113 else'work/degree12'if n in[107,109]else'work/audit11')/f'full{n}'
 for name in['build.m','build.log']:add(old/name)
for name in['census_sources.m','census_sources.log','two53_data.m','two53.log']:add(B/'work/degree13'/name)
for name in['stabilizers.m','stabilizers.log','unit_poles.m','unit_poles.log']:add(B/'work/degree12'/name)
for name in['rational_two.m','two73_data.m','two73.log','unit_poles.m','unit_poles.log','unit_poles_last.m','unit_poles_last.log','derickx_stoll_table2.txt']:add(B/'work/audit11'/name)
for name in['S14_proof.txt','S14_proof.pdf','S14_result.json','S10_S11_independent_audit.txt']:add(O/name)
for name in['asymptotic_prime_bound.tex','review.json','README.txt','arithmetic_check.py']:add(A/name,'prior_dyadic_theorem/'+name)
add(Path('/home/fnajman/degree5_torsion/refs/1707.00364/main.tex'),'references/DKSS_main.tex')
add(Path('/home/fnajman/Documents/Codex/2026-10-21/on-this-computer-there-are-files/work/degree9/prime_orders/derickx_stoll_2505.14109v1.html'),'references/Derickx_Stoll_2505.14109v1.html')
for sub in['mdmagma','common']:
 for p in(L/sub).rglob('*'):
  if p.is_file()and not any(v in p.parts for v in['.git','__pycache__']):add(p,'library/nonic-torsion/'+str(p.relative_to(L)))
readme='''S(14) = Primes(43), with computer assistance.

Start with outputs/S14_proof.pdf or .txt. The dyadic bound is 16641;
all 1924 primes below it are covered in work/degree14/final_coverage.json.
The proof uses rank28 modulo2, with M=157, and the corrected dyadic
cotangent/doubling argument. No assertion of a saturated optimal-quotient
cotangent lattice at2 is used.

Requirements: Magma V2.30-1, Sage's Python, and a C++17 compiler.
Extract this packet and run python relocate.py from this root before
running the commands below. The manifest gives the original SHA256
hashes before relocation. Numeric arrays are unchanged by relocation.

Check the stored exact certificates:
 g++ -O3 -std=c++17 work/degree14/check_prefixes.cpp -o work/degree14/check_prefixes
 g++ -O3 -std=c++17 work/degree14/relation_check.cpp -o work/degree14/relation_check
 g++ -O3 -std=c++17 work/degree14/gon_prefixes.cpp -o work/degree14/gon_prefixes
 python work/degree14/check_fi.py
 python work/degree14/gonality53.py
 python work/degree14/verify_auxiliary.py
 python work/degree14/verify_ranks.py
 python work/degree14/verify_coverage.py
The final command must print S14_FINAL_COVERAGE PASS 1924 / 1924.
The rank checker verifies 1018 ordinary,137 pair,1 mixed matrices.
The auxiliary checker verifies the156 dyadic rank28 matrices, the16
selected formal-immersion matrices, every balanced7+7 cusp pair,
the spanning relation bases, and the earlier zero2-torsion bound at53.

For arithmetic regeneration use a copy, since output files are replaced:
 magma -b work/degree14/census_sources.m
 magma -b work/degree14/verify_occurrences.m
 magma -b work/degree14/classify_supports.m
 magma -b work/degree14/quotient127.m
 magma -b work/degree14/stabilizers.m
 python work/degree14/prepare_bound.py
 python work/degree14/run_fi.py
 python work/degree14/prepare_ordinary.py
 python work/degree14/run_ordinary.py
 python work/degree14/prepare_pairs.py
 python work/degree14/run_pairs.py
The ordinary generator verifies all old source-orbit matches against
the new census, and computes degree14 jets afresh. To regenerate the
cached degree<=13 jets first, run the supplied degree13/stage2.m files
against the supplied degree13 census. Each canonical model must use the
same integral basis; the two copies are checked equal by SHA256.
Canonical builders are included. Run them with cwd library/nonic-torsion;
copy their output units_data.m into the two degree13/degree14 locations.
The model at113 was built in degree13. The older small-level builders
write under work/audit11 or work/degree12.

Important explicit exceptional input:
At113 the degree8 ordinary orbit of size7 is not asserted nonprincipal.
Its order8 diamond stabilizer excludes it. Every other single ordinary
orbit, all137 ordinary-pair orbits, and the73 mixed orbit are excluded
by the stored matrices. The proof spells out all supersingular cases.

At127 there is full rational127-torsion in characteristic2, so the
census enumerates all128 cyclic subgroups. Its48 supersingular closed
points of degree14 descend to48 degree2 points on the intermediate
curve. The point-count gonality bound, followed by the second published
orbit criterion, excludes127. No level127 canonical model, Hecke-jet,
formal-immersion or nonprincipality certificate is a proof input here.

At53 gonality53.py proves gonality>=16 using26 rational cusps and
absence of other places through degree6, with76256 complete prefix
tests. The only changed formal-immersion index from the initial
experiments is97:index8 is the successful selected certificate.

The earlier dyadic theorem and the S(10)/S(11) independent audit are
included for their borrowed mathematical inputs. No separate agent
audit of the whole S(14) proof is claimed.
'''
relocate='''from pathlib import Path
root=Path(__file__).resolve().parent
replacements={OLD_B:str(root),OLD_L:str(root/'library/nonic-torsion')}
n=0
for p in root.rglob('*'):
 if p.is_file()and p.name!='relocate.py'and p.suffix in['.py','.m','.magma','.txt','.json','.tex','.html']:
  try:s=p.read_text()
  except UnicodeDecodeError:continue
  t=s
  for a,b in replacements.items():t=t.replace(a,b)
  if t!=s:p.write_text(t);n+=1
print('Relocated',n,'text files; numerical arrays unchanged.')
'''.replace('OLD_B',repr(str(B))).replace('OLD_L',repr(str(L)))
manifest={name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for name,p in sorted(files.items())}
zpath=O/'S14_certificates.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for name,p in sorted(files.items()):z.write(p,name)
 z.writestr('README.txt',readme);z.writestr('relocate.py',relocate);z.writestr('manifest.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(zpath)as z:assert z.testzip()is None
out={'status':'PASS','bytes':zpath.stat().st_size,'files':len(files),'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'crc_verified':True};(W/'package_verified.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
