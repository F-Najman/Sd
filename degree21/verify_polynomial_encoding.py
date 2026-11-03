"""Exact validation of the NTL binary-series encoding used by every sieve."""
from pathlib import Path
import ast,re,json,hashlib,random
from functools import lru_cache
from sage.libs.ntl.ntl_GF2X import ntl_GF2X
W=Path(__file__).resolve().parent;names=['full_sieve.py','pair_sieve.py','mixed_new_sieve.py','ss_sieve.py','ss5_sieve.py','ss7_sieve.py','ss_nc127_sieve.py'];ref=None;hashes={}
for name in names:
 p=W/name;t=ast.parse(p.read_text());fs=[n for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in['as_ntl','pmul']];assert len(fs)==2;dump=ast.dump(ast.Module(body=fs,type_ignores=[]),include_attributes=False)
 if ref is None:ref=dump;code=ast.Module(body=fs,type_ignores=[])
 else:assert dump==ref,name
 hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
precisions={int(re.search(r'precision:=(\d+)',p.read_text())[1])for p in W.glob('full*/units_data.m')};top=max(precisions);env={'lru_cache':lru_cache,'ntl_GF2X':ntl_GF2X,'mask':(1<<top)-1};exec(compile(code,'actual_sieve_polynomial_functions','exec'),env);assert env['as_ntl'](0).list()==[]
for i in range(top):
 x=env['as_ntl'](1<<i);rr=list(map(int,x.list()));assert len(rr)==i+1 and rr[-1]==1 and not any(rr[:-1]);assert int(x.hex()[2:][::-1],16)==1<<i
# Independent schoolbook carryless multiplication on Python integers.
def mul(a,b):
 c=0
 while b:
  low=b&-b;c^=a<<(low.bit_length()-1);b^=low
 return c
rng=random.Random(20261031);cnt=0
for prec in sorted(precisions):
 env['mask']=(1<<prec)-1
 for a,b in[(0,0),(1,1),(1<<(prec-1),1),(1<<(prec-1),2),((1<<prec)-1,(1<<prec)-1)]+[(rng.getrandbits(prec),rng.getrandbits(prec))for _ in range(12)]:
  assert env['pmul'](a,b)==mul(a,b)&env['mask'];cnt+=1
(W/'polynomial_arithmetic_verified.json').write_text(json.dumps({'status':'PASS','all_binary_basis_vectors_checked':top,'precisions':sorted(precisions),'independent_carryless_products':cnt,'identical_arithmetic_function_AST':names,'source_sha256':hashes},indent=2)+'\n');print('S21_POLYNOMIAL_ENCODING_AND_PRODUCTS_PASS',top,cnt,flush=True)
