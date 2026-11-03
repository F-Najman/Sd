from pathlib import Path
import json,hashlib,shutil,textwrap
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';a=json.loads((W/'final_coverage.json').read_text());assert a['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'and not a['unresolved_primes']and a['new_independent_matrices']==11854
# Freeze the exact character-library implementation used in the successful runs.
source=B/'work/degree11/large_orders/strange_primes.magma';target=W/'strange_primes.magma';shutil.copyfile(source,target);digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert digest(source)==digest(target)
for name in['large_order.m','large_order_special.m']:
 p=W/name;s=p.read_text();s=s.replace(str(source),str(target));p.write_text(s)
(W/'character_library_provenance.json').write_text(json.dumps({'status':'IDENTICAL_FROZEN_COPY','original_path':str(source),'frozen_path':str(target),'sha256':digest(target)},indent=2)+'\n')
for name in['check_prefixes.cpp','relative_prefixes.cpp','relation_check.cpp']:shutil.copyfile(W.parent/'degree17'/name,W/name)
# Retain superseded construction attempts separately from proof inputs.
E=W/'exploration';E.mkdir(exist_ok=True)
for name in['find_extension_occurrences.py','find_extension_occurrences.log','inherited_census_prefix.json']:
 p=W/name
 if p.exists():shutil.move(str(p),str(E/name))
s=(W/'PROOF_DRAFT.txt').read_text();s=s.split('\n',1)[1].replace('Target theorem.','Theorem.').replace('The final coverage checker must pass before this is asserted as proved.','This is a computer-assisted proof. The complete prime and support\ncoverage has passed, with no unresolved case.')
s=s.replace('That final check, together with the stored rank replays and character\ncoverage, is required before the target theorem is declared proved.','All checks have passed:23079 primes,284 support types,615 selected\ncharacter orders, and11854 new independent obstruction matrices.\nThe285-file inherited proof manifest also matches without change.\nTogether with the occurrence certificates, this proves the theorem.')
s+='''
REFERENCES AND RETAINED PROOF INPUTS

Derickx--Stoll, Prime order torsion on elliptic curves over number
fields, Part I: Asymptotics, Theorem1.2, Theorem3.3, Proposition4.1,
Remark4.4, Table2, and Corollary7.5:
 https://www.mathe2.uni-bayreuth.de/stoll/papers/asymptotics.pdf

Box, Quadratic points on modular curves with infinite Mordell--Weil
group, section4.7, completed list:
 https://arxiv.org/html/1906.05206

Adzaga--Keller--Michaud-Jacobs--Vukorepa, Computing quadratic points on
modular curves X_0(N), Table16:
 https://arxiv.org/html/2303.12566v2

The earlier dyadic lattice argument and the corrected inherited local
certificates are retained in outputs/S13_proof.pdf and
work/degree17/PROOF.txt. The latter's285-file proof manifest has been
checked against the actual inherited files. In particular, only the
corrected level97 operators are used.

The final machine-readable ledgers are final_coverage.json and
support_coverage.json. independent_rank_checks.json and
independent_rank_low131.json certify all11854 new obstruction matrices.
The relative-map replays and character-order coverage have their own
verified JSON files. REPLAY.txt gives exact verification commands;
proof_manifest.json gives SHA256 hashes of the retained proof inputs.
'''
s.encode('ascii');(W/'PROOF.txt').write_text(s)
# Use the existing research packet's simple portable PDF renderer.
t=(W.parent/'degree17/finalize_result.py').read_text();f=t[t.index('def save_proof'):t.index("proof=save_proof")].replace('29 October 2026','30 October 2026');scope={'Path':Path,'textwrap':textwrap,'hashlib':hashlib,'O':O};exec(f,scope);proof=scope['save_proof'](W/'PROOF.txt','S18_proof','S(18): complete determination')
result={k:v for k,v in a.items()if k!='cases'};result.update({'proof':proof,'coverage_ledger':'../work/degree18/final_coverage.json','support_coverage':'../work/degree18/support_coverage.json','certificate_manifest':'../work/degree18/proof_manifest.json','certificate_replay':'../work/degree18/REPLAY.txt','independent_rank_checks':['../work/degree18/independent_rank_checks.json','../work/degree18/independent_rank_low131.json']})
for name in['S18_result.json','S18_status.json']:(O/name).write_text(json.dumps(result,indent=2)+'\n')
print('S18_COMPLETE_RESULT_SAVED',proof['pages'],'proof pages; S =',a['S'],flush=True)
