from pathlib import Path
import json
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs'
if(W/'final_coverage.json').exists()and(O/'S20_result.json').exists():
 print((O/'S20_result.json').read_text());raise SystemExit(0)
s=json.loads((W/'large_selected_orders.json').read_text());done=[];pade=[]
for j in s['jobs']:
 stem=f"p{j['p']}_n{j['order']}";p=W/'large_orders'/(stem+'.json')
 if p.exists():
  a=json.loads(p.read_text())
  if a.get('status')=='PASS':done.append(j)
 if(W/'large_orders'/(stem+'_independent_pade.json')).exists():pade.append(j)
ns=json.loads((W/'local_levels.json').read_text())['levels'];ordinary=[]
for n in ns:
 p=W/f'full{n}/sieve.json'
 if p.exists():ordinary.append(json.loads(p.read_text()))
a={'status':'IN_PROGRESS','degree':20,'verified_lower_bound':[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,61],'proved_dyadic_upper_bound':525313,'dyadic_M':229,'dyadic_coefficient_rank':40,'local_levels':ns,'ordinary_levels_completed':len(ordinary),'new_ordinary_sources_checked':sum(v['source_orbits']for v in ordinary),'new_characters_completed':len(done),'new_characters_required':len(s['jobs']),'inherited_characters':len(s['reused']),'independent_pade_certificates':len(pade),'notes':'Lower bound proved. Upper determination awaits all source, character, and final independent coverage checks.'}
(O/'S20_status.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a,indent=2))
