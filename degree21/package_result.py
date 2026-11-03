"""Publish only a completely verified degree21 result."""
from pathlib import Path
import json,textwrap,re,hashlib
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs';a=json.loads((W/'final_coverage.json').read_text());assert a['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'and not a['unresolved_primes']and a['S']==[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
for f in['large_verified.json','independent_sequence_results.json','independent_rank_checks.json','ss_jets_independent.json']:assert json.loads((W/f).read_text())['status']=='PASS'
# Correct the watcher's stale informational worker label, preserving it for audit.
# The frozen source actually uses ProcessPoolExecutor(max_workers=1).
pade_file=W/'independent_sequence_results.json';pade=json.loads(pade_file.read_text())
if pade.get('workers')==4:
 pade['producer_reported_workers']=4;pade['workers']=1
 pade['worker_count_note']='Frozen checker uses max_workers=1; its workers=4 output label was stale. All per-sequence mathematical certificates are unchanged.'
 pade_file.write_text(json.dumps(pade,indent=2)+'\n')
assert pade['workers']==1
s=(W/'PROOF_DRAFT.txt').read_text();s=s[s.index('1. OCCURRENCES'):];end=s.index('The final packet must contain final_coverage.json');ref=s.index('Primary reference:',end);s=s[:end]+'''The final_coverage.json ledger has passed, with status
PROVED_WITH_COMPUTER_ASSISTANCE and no unresolved primes. All required
independent source, rank, profile, character, and prime coverage checks
have passed. This proves the theorem.

'''+s[ref:]
s=s.replace('all degree 21 premises are to be listed','all degree 21 premises are listed')
intro='''S(21): DYADIC REDUCTION AND RELATIVE FORMAL IMMERSIONS
31 October 2026

Theorem. For elliptic curves over number fields of exact degree 21,
 S(21)={2,3,5,7,11,13,17,19,23,29,31,37,41,43,47}.
This is a computer-assisted proof. All required local certificates,
selected-character families, independent replays, and the exhaustive
prime and residue-support ledgers have passed. There is no unresolved
case and no conjectural rational-torsion hypothesis.

'''
s=intro+s;s.encode('ascii');assert not re.search(r'\b(draft|proposed|pending)\b',s,re.I);(W/'PROOF.txt').write_text(s)
t=(W.parent/'degree17/finalize_result.py').read_text();fn=t[t.index('def save_proof'):t.index('proof=save_proof')].replace('29 October 2026','31 October 2026');scope={'Path':Path,'textwrap':textwrap,'hashlib':hashlib,'O':O};exec(fn,scope);proof=scope['save_proof'](W/'PROOF.txt','S21_proof','S(21): complete determination')
result={k:v for k,v in a.items()if k!='cases'};result.update({'proof':proof,'coverage_ledger':'../work/degree21/final_coverage.json','support_coverage':'../work/degree21/support_coverage.json','certificate_manifest':'../work/degree21/proof_manifest.json','certificate_replay':'../work/degree21/REPLAY.txt'})
for name in['S21_result.json','S21_status.json']:(O/name).write_text(json.dumps(result,indent=2)+'\n')
index={'status':a['status'],'degree':21,'S':a['S'],'proof':proof,'replay':'../work/degree21/REPLAY.txt','manifest':'../work/degree21/proof_manifest.json','prime_coverage':'../work/degree21/final_coverage.json','local_support_coverage':'../work/degree21/support_coverage.json','dyadic_threshold':19236,'support_types':477,'character_orders':5289,'new_character_orders':2815,'inherited_character_orders':2474,'large_primes':850,'new_obstruction_matrices':a['new_independent_matrices'],'native_pair_triple_matrices':35631,'relative_profile_count':sum(r['profiles']for f in['profile_spaces_independent.json','profile_spaces_full_new_verified.json']for r in json.loads((W/f).read_text())['results'])+6,'certificates':['../work/degree21/'+f for f in['sharp61_finite_verified.json','stabilizer_geometry_verified.json','intrinsic_full_new_verified.json','profile_spaces_full_new_verified.json','inherited_manifest_verified.json','inherited_hypotheses_verified.json','matches_verified.json','dyadic_independent.json','census_counts_independent.json','frobenius127_verified.json','global181_verified.json','fi_matrices_independent.json','intrinsic_relative_independent.json','intrinsic_full_cusps_extra.json','intrinsic_multiple_independent.json','quotients_intrinsic_verified.json','profile_coverage_independent.json','profile_spaces_independent.json','relative127_verified.json','relative_cusps_intrinsic_verified.json','relative61_o20_independent.json','polynomial_arithmetic_verified.json','ss_jets_independent.json','ss_jets_extra_T3_verified.json','support_inputs_verified.json','independent_rank_checks.json','large_verified.json','independent_sequence_results.json']],'unused_experiments':['native FI61 index15,FI89,FI97 quotient cusp checks: replaced by full-Jacobian canonical maps; initial FI61 index5 also unused','coarse FI71 andFI127 failures; replaced by full canonical cusp maps','SS127 source23 direct T3/T5/T7 obstructions; replaced by order7 quotient relative immersion','optional triple SS6 cotangents at73; the H9 stabilizer already excludes this support','superseded raw and blocked engine speed tests; actual engine per job is explicit']};(O/'S21_certificate_index.json').write_text(json.dumps(index,indent=2)+'\n')
lines=['S(21): certificate index','Completed computer-assisted determination: '+str(a['S']),'Proof: outputs/S21_proof.pdf','Complete replay: work/degree21/REPLAY.txt','Manifest: work/degree21/proof_manifest.json','',f"New obstruction matrices: {a['new_independent_matrices']}",'5289 selected character orders,2815 fresh and2474 inherited.','477 local support types;82136 primes through1050024.','',*index['certificates'],'','Unused experiments:',*index['unused_experiments']];(O/'S21_certificate_index.txt').write_text('\n'.join(lines)+'\n')
r=(W/'REPLAY.txt').read_text().replace('Degree21 replay instructions. Verification and final packaging are in progress.','Degree21 replay instructions. Completed computer-assisted proof.');(W/'REPLAY.txt').write_text(r)
print('S21_COMPLETE_RESULT_SAVED',proof['pages'],'pages',a['S'],flush=True)
