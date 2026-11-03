from pathlib import Path
import json,re,datetime
W=Path(__file__).resolve().parent;bad=[];counts={}
for name,files,marker in [('characters',list((W/'large_orders').glob('p*_cpp.log')),'S22_PACKED_GRAPH_KRYLOV_COMPLETE'),('ordinary22',[f for h in W.glob('full*')for f in h.glob('chunk_*.log')if h.name!='full163'],'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'),('ordinary163',list((W/'full163').glob('chunk_*.log')),'AUDIT_ACTUAL_HECKE_JETS_COMPLETE')]:
 ok=0
 for f in files:
  s=f.read_text();ok+=(marker in s or (name=='characters'and'S22_SIMD_GRAPH_KRYLOV_COMPLETE'in s))
  if re.search(r'Runtime error|User error|Assertion.*failed|Traceback|Segmentation fault|std::bad_alloc',s):bad.append(str(f))
 counts[name]={'started':len(files),'complete':ok}
for name in ['run_characters_simd.log','verify_large_simd.log','run_new_ordinary.log','run_ordinary163.log','pipeline_sieves.log','run_full163_sieve.log','verify_ranks.log']:
 p=W/name
 if p.exists()and re.search(r'Runtime error|User error|Assertion.*failed|Traceback|Segmentation fault|std::bad_alloc',p.read_text()):bad.append(name)
counts['verified_characters']=json.loads((W/'large_verification_progress.json').read_text());counts['errors']=bad;counts['time_UTC']=str(datetime.datetime.now(datetime.timezone.utc));print(json.dumps(counts,indent=2),flush=True)
assert not bad
