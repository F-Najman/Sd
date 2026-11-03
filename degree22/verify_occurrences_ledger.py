"""Bind all fresh exact-degree22 occurrence runs to their native sources."""
from pathlib import Path
import json,hashlib,re
W=Path(__file__).resolve().parent
parts=[('verify_small_occurrences',[2,3,5,7],r'S22_SMALL_OCCURRENCE_VERIFIED prime=(\d+) exact_field_degree=22','S22_SMALL_OCCURRENCES_AND_RIEMANN_ROCH_BOUND_VERIFIED'),('verify_extension_occurrences',[11,13,17,19,23,29,31],r'S22_EXTENSION_OCCURRENCE_VERIFIED prime=(\d+) field_degree=22','S22_ALL_DEGREE11_TO22_EXTENSIONS_COMPLETE'),('verify_occurrences',[37,41,43,47,53,67],r'S22_EXACT_OCCURRENCE_VERIFIED prime=(\d+) field_degree=22','S22_ALL_NEW_OCCURRENCES_COMPLETE')]
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest();records=[];primes=[]
for stem,expect,pattern,marker in parts:
 source=W/(stem+'.m');log=W/(stem+'.log');s=log.read_text();assert marker in s and not any(k in s for k in ['Runtime error','User error','Assertion failed','Traceback']);got=sorted(map(int,re.findall(pattern,s)));assert got==expect,(stem,got);text=source.read_text();assert 'IsIrreducible'in text and 'P ne E!0'in text and ('Degree(K)'in text or 'AbsoluteDegree(K)'in text);assert not re.search(r'\bload\b',text), 'Record any additional source dependency before use.'
 records.append({'source':source.name,'source_sha256':sha(source),'log':log.name,'log_sha256':sha(log),'verified_prime_orders':got,'absolute_degree':22});primes+=got
expected=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,67];assert primes==expected
out={'status':'PASS','degree':22,'proved_lower_bound':primes,'small_exact':parts[0][1],'quadratic_extension_exact':parts[1][1],'new_exact':parts[2][1],'no_upper_bound_claim':True,'records':records};p=W/'occurrences_verified.json';tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(out,indent=2)+'\n');tmp.replace(p);print('S22_FRESH_OCCURRENCE_LEDGER_PASS',primes,flush=True)
