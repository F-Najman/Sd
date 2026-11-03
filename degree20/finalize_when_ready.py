from pathlib import Path
import subprocess,json,time
W=Path(__file__).resolve().parent;B=W.parents[1];jobs=json.loads((W/'large_selected_orders.json').read_text())['jobs'];last=0
while True:
 ready=True
 for name in ['large_native_results.json','independent_sequence_results.json']:
  if not(W/name).exists():ready=False;continue
  a=json.loads((W/name).read_text());ready &= a['status']=='PASS'and(a.get('characters',a.get('checked'))==1951)
 if ready:break
 if time.monotonic()-last>=60:
  total=sum((W/'large_orders'/f"p{j['p']}_n{j['order']}.json").exists()for j in jobs);pade=sum((W/'large_orders'/f"p{j['p']}_n{j['order']}_independent_pade.json").exists()for j in jobs);print('S20_WAITING_FOR_CHARACTERS',total,'/1951; independent Pade',pade,flush=True);last=time.monotonic()
 time.sleep(5)
for args,name in [(['sage','-python',str(W/'verify_large.py')],'verify_large.log'),(['sage','-python',str(W/'verify_coverage.py')],'verify_coverage.log'),(['python3',str(W/'package_result.py')],'package_result.log'),(['python3',str(W/'build_manifest.py')],'build_manifest.log'),(['python3',str(W/'verify_manifest.py')],'verify_manifest.log')]:
 print('S20_FINAL_STEP_STARTED',name,flush=True)
 with(W/name).open('w')as f:r=subprocess.run(args,cwd=B,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(name,(W/name).read_text()[-2500:]);print('S20_FINAL_STEP_PASS',name,flush=True)
print('S20_PROVED_PACKAGED_AND_MANIFEST_VERIFIED',flush=True)
