from pathlib import Path
import json
from sage.all import matrix,GF,ZZ
from unit_arithmetic import xorrows
W=Path(__file__).resolve().parent;F=GF(2);out=[]
for n in[59, 61, 67, 73, 79, 83, 89, 97, 103, 107, 109, 113, 131, 137, 139]:
 stem='FI97_i8'if n==97 else f'FI{n}';p=W/'FI'/stem;cs=p.with_suffix('.compressed.txt').read_text().splitlines();head=list(map(int,cs[0].split()));lev,m,tn,root,nr,nc,d,rk=head;assert lev==n and d==21
 rr=[sum(int(x)<<(64*k)for k,x in enumerate(line.split()))for line in cs[1:]];assert len(rr)==nr;assert matrix(F,[ZZ(x).digits(2,padto=1024)for x in rr]).rank()==rk
 originals=[];basis={}
 with p.with_suffix('.txt').open()as f:
  assert list(map(int,next(f).split()))==head[:7]
  for c,line in zip(rr,f):
   line=line.strip();assert len(line)==nc;x=int(line,2);originals.append(x)
   if c and c.bit_count()==1:basis.setdefault(c.bit_length()-1,x)
 assert len(originals)==nr and set(basis)==set(range(rk));bs=[basis[k]for k in range(rk)]
 for c,x in zip(rr,originals):assert xorrows(c,bs)==x
 core=rr[:d]+[x for j in range(1,m)for x in rr[d+10*(j-1):d+10*(j-1)+6]];r=matrix(F,[ZZ(x).digits(2,padto=1024)for x in core]).rank();a=json.loads((W/f'FI/FI{n}_verified.json').read_text());assert a['status']in['PASS','PASS_RELATIVE'];
 if 'rank_cap6'in a:assert a['rank_cap6']==r and a['kernel_dimension']==len(core)-r and not a['exceptional_failures']
 out.append({'N':n,'status':'PASS','all_raw_rows_reconstructed':nr,'compressed_rank':rk,'rank_cap6':r});print('S21_FI_COMPRESSION_INDEPENDENT_PASS',n,flush=True)
(W/'fi_matrices_independent.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n')
