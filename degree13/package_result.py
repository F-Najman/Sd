from pathlib import Path
import json,hashlib,zipfile
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';L=Path('/home/fnajman/degree9_torsion/nonic-torsion');A=Path('/home/fnajman/Documents/Codex/2026-10-21/on-this-computer-there-are-files/work/asymptotic_torsion')
assert json.load(open(W/'final_coverage.json'))['status']=='PASS'
files={}
def add(p,arc=None):
 p=Path(p);assert p.is_file(),p;files[arc or str(p.relative_to(B))]=p
# Include the complete new computation, excluding redundant executables and bytecode.
for p in W.rglob('*'):
 if p.is_file()and '__pycache__'not in p.parts and p.suffix in['.m','.magma','.py','.cpp','.txt','.json','.gz','.log']:add(p)
# Earlier audited inputs and their generation scripts.
for n in[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109]:
 old=B/('work/degree12'if n in[107,109]else'work/audit11')/f'full{n}'
 for name in['build.m','build.log']:add(old/name)
for name in['P41_NC5_clean.m','P41_NC5_clean.log','P41_cusps.m','P41_cusps.log','supersingular41.log','supersingular41_inputs.m','supersingular43.log','prime_good48.m','rational_two.m','two73.log','two73_data.m','unit_poles.m','unit_poles.log','unit_poles_last.m','unit_poles_last.log','derickx_stoll_table2.txt']:add(B/'work/audit11'/name)
for name in['stabilizers.m','stabilizers.log','occurrence43.m','occurrence43.log','unit_poles.m','unit_poles.log']:add(B/'work/degree12'/name)
# The earlier independent audit and exact dyadic theorem.
for name in['S13_proof.txt','S13_proof.pdf','S13_result.json','S10_S11_independent_audit.txt']:add(O/name)
for name in['asymptotic_prime_bound.tex','README.txt','review.json','arithmetic_check.py']:add(A/name,'prior_dyadic_theorem/'+name)
add(Path('/home/fnajman/degree5_torsion/refs/1707.00364/main.tex'),'references/DKSS_main.tex')
add(Path('/home/fnajman/Documents/Codex/2026-10-21/on-this-computer-there-are-files/work/degree9/prime_orders/derickx_stoll_2505.14109v1.html'),'references/Derickx_Stoll_2505.14109v1.html')
for sub in['mdmagma','common']:
 for p in(L/sub).rglob('*'):
  if p.is_file()and not any(v in p.parts for v in['.git','__pycache__']):add(p,'library/nonic-torsion/'+str(p.relative_to(L)))
readme='''S(13) = Primes(37), with computer assistance.

Start with outputs/S13_proof.pdf or .txt. The global bound is 8374,
proved by the dyadic doubling/Raynaud argument and the 156 rank-26
intersection matrices at M=157. All 1048 primes below the bound are
accounted for in work/degree13/final_coverage.json.

Requirements: Magma V2.30-1, Sage's Python, and a C++17 compiler.
No ordinary-prime character computation above 8374 is used.

For a portable copy, extract and first run python relocate.py from this
root. It replaces the original workspace and library paths. Run all
commands below from this extracted root. The manifest records the
original files before relocation. Numerical arrays and ranks are not
changed by relocation.

Checking the stored arithmetic certificates:
 g++ -O3 -std=c++17 work/degree13/check_prefixes.cpp -o work/degree13/check_prefixes
 g++ -O3 -std=c++17 work/degree13/relation_check.cpp -o work/degree13/relation_check
 python work/degree13/verify_dyadic.py
 python work/degree13/check_selected_fi.py
 python work/degree13/verify_auxiliary.py
 python work/degree13/verify_ranks.py
 python work/degree13/verify_coverage.py
The last command must print S13_FINAL_COVERAGE PASS 1048 / 1048.

The FI checker replays all normalized degree-13 cusp tuples or all
binary relations, depending on the size of the kernel. At 79 it
recomputes the 25 kernel generators and checks every nonzero relation.
The auxiliary checker independently verifies their spanning property,
all 18 selected ranks, the three mixed-support obstruction matrices,
the 21 tangent matrices at P12+c on X_1(43), and JOne(53)'s 2-torsion
bound. verify_ranks.py checks the 663 ordinary obstruction ranks.

For regeneration use a copy, since numerical output files are replaced.
Magma commands are:
 magma -b work/degree13/census_sources.m
 magma -b work/degree13/verify_occurrences.m
 magma -b work/degree13/classify_supports.m
 magma -b work/degree13/stabilizers_new.m
 magma -b work/degree13/cusp43.m
 magma -b work/degree13/mixed43_lifting.m
 python work/degree13/run_ordinary.py
 python work/degree13/mixed_sieve.py 41
 python work/degree13/mixed_sieve.py 73
Ordinary stage2.m scripts and full_sieve.py may also be run one level
at a time. The two unresolved ordinary tests are explicit proof inputs:
43: degree 12, orbit size 7 (known lift and formal immersion);
113: degree 8, orbit size 7 (order-8 stabilizer and gonality).
They are not assumed nonprincipal. The other 663 ordinary tests pass.

The FI generator run_fi.py records the initial jobs. Its initial
matrices at 43 and 79 fail. They are excluded from the final proof;
regenerate the selected alternatives by:
 magma -b P:=43 Ind:=21 Tn:=2 Q:=3,5,7,11 Out:=work/degree13/FI/FI43_combined.txt work/degree13/export_combined_alpha.m
 magma -b P:=79 Ind:=39 Tn:=2 Q:=3 Out:=work/degree13/FI/FI79_i39.txt work/degree13/export_FI_fast.m
 python work/degree13/compress_FI.py work/degree13/FI/FI43_combined.txt
 python work/degree13/compress_FI.py work/degree13/FI/FI79_i39.txt
The selected successful files are listed in formal_immersion_final.json.
Failed preliminary logs and the abandoned slow 79 prefix enumeration
are retained for transparency and are not proof inputs.

For canonical model generation run build.m with cwd library/nonic-torsion.
Earlier builders write under work/audit11 or work/degree12; copy their
units_data.m into work/degree13/fullN afterward. The new 113 builder
writes directly under degree13. Its two modular-unit pole degrees
167 and 175 are proved by work/degree13/unit_poles.m.

The dyadic theorem and its earlier reviews are reproduced separately.
The S(10)/S(11) audit supplies the borrowed small-level native tests.
There has been no separate agent audit of the complete S(13) proof.
'''
relocate='''from pathlib import Path
root=Path(__file__).resolve().parent
replacements={OLD_B:str(root),OLD_L:str(root/'library/nonic-torsion')}
count=0
for p in root.rglob('*'):
 if p.is_file()and p.name!='relocate.py'and p.suffix in['.py','.m','.magma','.txt','.json','.tex','.html']:
  try:s=p.read_text()
  except UnicodeDecodeError:continue
  t=s
  for a,b in replacements.items():t=t.replace(a,b)
  if t!=s:p.write_text(t);count+=1
print('Relocated',count,'text files; numerical arrays unchanged.')
'''.replace('OLD_B',repr(str(B))).replace('OLD_L',repr(str(L)))
manifest={arc:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for arc,p in sorted(files.items())}
zipname=O/'S13_certificates.zip'
with zipfile.ZipFile(zipname,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for arc,p in sorted(files.items()):z.write(p,arc)
 z.writestr('README.txt',readme);z.writestr('relocate.py',relocate);z.writestr('manifest.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(zipname)as z:assert z.testzip()is None
out={'status':'PASS','file':str(zipname),'bytes':zipname.stat().st_size,'included_files':len(files),'sha256':hashlib.sha256(zipname.read_bytes()).hexdigest(),'crc_verified':True};(W/'package_verified.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
