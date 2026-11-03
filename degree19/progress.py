from pathlib import Path
import json
W=Path(__file__).resolve().parent;B=W.parents[1];final=W/'final_coverage.json'
if final.exists()and json.loads(final.read_text()).get('status')=='PROVED_WITH_COMPUTER_ASSISTANCE'and(B/'outputs/S19_result.json').exists():
 print((B/'outputs/S19_result.json').read_text());raise SystemExit(0)
js=json.loads((W/'large_selected_orders.json').read_text())['jobs'];completed=[]
for j in js:
 p=W/f"large_orders/p{j['p']}_n{j['order']}.json"
 if p.exists()and json.loads(p.read_text()).get('status')=='PASS':completed.append(j)
ordinary=[json.loads(p.read_text())for p in W.glob('full*/sieve.json')];ranks=W/'independent_rank_checks.json'
status={'status':'IN_PROGRESS','degree':19,'verified_lower_bound':[2,3,5,7,11,13,17,19,23,29,31,37,41,43],'proved_dyadic_upper_bound':525313,'local_exclusions_completed':19,'global_163_exclusion_certified':True,'ordinary_sources_checked':sum(a['source_orbits']for a in ordinary),'new_independent_rank_matrices':json.loads(ranks.read_text())['matrices']if ranks.exists()else None,'new_characters_completed':len(completed),'new_characters_required':len(js),'inherited_characters_verified':555,'independent_pade_certificates':len(list((W/'large_orders').glob('*_independent_pade.json'))),'notes':'All local cases resolved. Exact upper set awaits completion of selected-character screens and final coverage audit.'}
(B/'outputs/S19_status.json').write_text(json.dumps(status,indent=2)+'\n');print(json.dumps(status,indent=2))
