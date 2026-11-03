from pathlib import Path
import json,time,hashlib
from unit_arithmetic import matbits,xorrows
from profile_kernels import profiles,check_profile,kernel
W=Path(__file__).resolve().parent;tt=time.monotonic();s=(W/'full163/units_data.m').read_text();D=matbits(s,'DiamondMatrix');Q=matbits(s,'qcoeffs');g=len(D);assert g==1027
mul=lambda A,B:[xorrows(r,B)for r in A]
I=[1<<i for i in range(g)];D3=mul(mul(D,D),D);A=[v^u for v,u in zip(D3,I)];P=I
for _ in range(27):P=mul(P,D3)
assert P==I
# A3 has odd degree on im(h-1), hence preserves this complete mod-2 cotangent image.
# q-coefficients are coefficients of q*f(q)*dq/q at the rational Tate cusp.
AQ=mul(A,Q);rows=[];cols=[]
for k in range(81):
 vals=[v>>1&((1<<22)-1)for v in AQ];cols.append([sum(((v>>j)&1)<<i for i,v in enumerate(vals))for j in range(22)]);AQ=mul(D,AQ)
 print('S22_CUSP163_COLUMNS',k,round(time.monotonic()-tt,1),flush=True)if k%10==0 else None
G=[list(range(a,81,3))for a in range(3)];out=[]
for pi,pr in enumerate(profiles(81,22,8)):
 a=check_profile(cols,pr,22,G,8);a.update({'profile':pi,'caps':pr});out.append(a)
 if pi%25==0 or a['status']!='PASS':print('S22_CUSP163_PROFILE',pi,a['quotient_kernel_dimension'],a['min_unexpected_cost'],a['status'],round(time.monotonic()-tt,1),flush=True)
 assert a['status']=='PASS'
p=W/'FI/cusps163_columns.json';p.write_text(json.dumps([[hex(z)for z in row]for row in cols]))
z={'status':'PASS','N':163,'degree':22,'method':'anti_H27 complete cotangent system; A3 odd on image','known_fibers':G,'minimum_fiber_degree':27,'profiles':out,'columns_sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(W/'FI/cusps163_verified.json').write_text(json.dumps(z,indent=2)+'\n');print('S22_CUSPS163_COMPLETE',len(out),flush=True)
