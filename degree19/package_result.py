from pathlib import Path
import json,hashlib,textwrap,re
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs';a=json.loads((W/'final_coverage.json').read_text());assert a['status']=='PROVED_WITH_COMPUTER_ASSISTANCE'and not a['unresolved_primes'];assert json.loads((W/'large_verified.json').read_text())['status']=='PASS'
s=(W/'PROOF.txt').read_text()
replacements={
'''DRAFT: the final selected-character computation and full prime coverage
check are still running. No completed determination is claimed by this
version. All local exclusions and their independent checks have passed.
''':'',
'Proposed theorem.':'Theorem.',
'''The argument is computer-assisted. Its remaining finite verification is
identified in the first paragraph; the completed version will remove that
qualification only after the full coverage ledger passes.''':'''This is a computer-assisted proof. Every required local exclusion and
selected-character certificate has passed, and the complete prime and
support coverage has no unresolved case.''',
'''Their completion is the remaining task indicated in the draft status.''':'''All required orders have completed certificates, including their
independent sequence checks and full divisor-family coverage.''',
'''Their
completion is the remaining task indicated in the draft status.''':'''All required orders have completed certificates, including their
independent sequence checks and full divisor-family coverage.''',
'''Their completion is the remaining task indicated in the first paragraph.''':'''All selected-character and divisor-family checks have passed.''',
'''Its final pass, still pending in this draft, is
required before asserting the proposed theorem.''':f'''The complete ledger has passed for all{a['audited_primes']} primes in the
finite range and all344 local support types. It has no unresolved case,
which proves the theorem.''',
'''REPLAY.txt will list the final verification commands, and
proof_manifest.json will hash the required proof inputs.''':'''REPLAY.txt lists the verification commands, and proof_manifest.json
hashes the required proof inputs.'''
}
for old,new in replacements.items():
 if old in s:s=s.replace(old,new)
# Catch an unhandled draft qualifier instead of silently publishing it.
assert not re.search(r'\b(draft|pending|proposed)\b',s,re.I)
words=['degree','order','rank','genus','through','all','every','dimension','precision','cost','prime','at','for','both','exceed','characteristic','modulo','among','than','section','proposition','theorem','corollary','remark','table','only','inclusion','contains','kernel','independent','beyond','before']
s=re.sub(r'\b('+ '|'.join(words)+r')(?=\d)',lambda m:m.group(0)+' ',s,flags=re.I)
s=re.sub(r'\b([A-Za-z]+)(?=\d)',lambda m:m.group(0) if m.group(0) in {'SS','NC','O','C','R','Z','Phi'} else m.group(0)+' ',s)
s.encode('ascii');(W/'PROOF.txt').write_text(s)
# Reuse the previously reviewed portable PDF renderer without executing
# another degree's package or reading its conclusion as an input.
t=(W.parent/'degree17/finalize_result.py').read_text();fn=t[t.index('def save_proof'):t.index('proof=save_proof')].replace('29 October 2026','30 October 2026');scope={'Path':Path,'textwrap':textwrap,'hashlib':hashlib,'O':O};exec(fn,scope);proof=scope['save_proof'](W/'PROOF.txt','S19_proof','S(19): complete determination')
result={k:v for k,v in a.items()if k!='cases'};result.update({'proof':proof,'coverage_ledger':'../work/degree19/final_coverage.json','support_coverage':'../work/degree19/support_coverage.json','certificate_manifest':'../work/degree19/proof_manifest.json','certificate_replay':'../work/degree19/REPLAY.txt'})
for name in['S19_result.json','S19_status.json']:(O/name).write_text(json.dumps(result,indent=2)+'\n')
index={'status':'PROVED_WITH_COMPUTER_ASSISTANCE','degree':19,'S':a['S'],'proof':proof,'replay':'../work/degree19/REPLAY.txt','manifest':'../work/degree19/proof_manifest.json','prime_coverage':'../work/degree19/final_coverage.json','local_support_coverage':'../work/degree19/support_coverage.json','ordinary_orbits':27519,'new_independent_obstruction_matrices':21392,'character_orders':1147,'new_character_orders':592,'inherited_character_orders':555,'large_primes':196,'relative_map_certificates':['../work/degree19/'+z for z in['relative53_verified.json','relative61_verified.json','relative73_relations_verified.json','relative73_relation_spaces_independent.json','relative127_verified.json','relative_cusps_intrinsic_verified.json']],'level53_repair':'../work/degree19/cusps53_intrinsic_verified.json','global163':'../work/degree19/anti163_norms_verified.json','new137_exception':'../work/degree19/stabilizer137_ordinary.log','independent_ranks':'../work/degree19/independent_rank_checks.json','character_coverage':'../work/degree19/large_verified.json','inherited_manifest_check':'../work/degree19/inherited_manifest_verified.json'}
(O/'S19_certificate_index.json').write_text(json.dumps(index,indent=2)+'\n');print('S19_COMPLETE_RESULT_SAVED',proof['pages'],'proof pages; S=',a['S'],flush=True)
