"""Require complete reference sequences and independent arithmetic fixtures."""
from pathlib import Path
import json,hashlib,re
O=Path(__file__).resolve().parent;W=O.parent
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
checks=[]
for tag,reference,terms in [('huge',O/'huge_benchmark_sequence.m',349866),('reference',O/'packed_benchmark_sequence.m',175000)]:
 out=O/f'simd_{tag}_full.m';log=(O/f'simd_{tag}_full.log').read_text();assert'S22_SIMD_GRAPH_KRYLOV_COMPLETE'in log and not any(k in log for k in ['Assertion','error','Traceback']);assert out.read_bytes()==reference.read_bytes()
 checks.append({'tag':tag,'all_terms_identical':terms,'reference':str(reference.relative_to(W)),'reference_sha256':sha(reference),'output_sha256':sha(out),'cpu_seconds':float(re.search(r'cpu_seconds=([0-9.]+)',log)[1])})
f=json.loads((O/'simd_fixtures_verified.json').read_text());assert f['status']=='PASS'and f['source_sha256']==sha(W/'krylov_simd.cpp')and f['binary_sha256']==sha(W/'krylov_simd')and len(f['tests'])==21
assert'S22_SIMD_EXACT_INTEGER_REDUCTION_PASS cases=7200000'in(O/'test_simd_arithmetic.log').read_text()
cert={'status':'PASS','source_sha256':sha(W/'krylov_simd.cpp'),'binary_sha256':sha(W/'krylov_simd'),'checks':checks,'fixture_sha256':sha(O/'simd_fixtures_verified.json'),'integer_arithmetic_tests':7200000,'arithmetic_test_source_sha256':sha(O/'test_simd_arithmetic.cpp'),'arithmetic':'Exact unsigned integers only; eight-lane reciprocal reduction at base2^B, each value strictly below2^B, multiplier below2^32, one correction; exact prior128-bit fallbacks unchanged. No coordinate change.'}
(O/'simd_full_replay_verified.json').write_text(json.dumps(cert,indent=2)+'\n');print('S22_SIMD_FULL_REFERENCE_REPLAYS_PASS',flush=True)
