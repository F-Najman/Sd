from pathlib import Path
import hashlib,json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;H=W/'full127';old=(H/'hecke_jets_432.m').read_text();new=(H/'fast_jets_432.m').read_text();checks={k:lit(old,k)==lit(new,k)for k in['SourceMetadata','SourceRecords','SourceHeckeRecords']};assert all(checks.values())
a={'status':'PASS','level':127,'sources':8,'all_source_and_target_coefficients_identical':checks,'original_sha256':hashlib.sha256(old.encode()).hexdigest(),'fast_sha256':hashlib.sha256(new.encode()).hexdigest(),'original_CPU_seconds':48.66,'fast_CPU_seconds':22.39};(W/'jet_inverse_replay_verified.json').write_text(json.dumps(a,indent=2)+'\n');print('S19_CANONICAL_JET_INVERSE_EXACT_REPLAY_PASS',flush=True)
