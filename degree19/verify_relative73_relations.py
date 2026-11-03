from pathlib import Path
import json
from sage.all import GF,matrix,ZZ
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;D=json.loads((W/'relative73_relations_verified.json').read_text());assert D['status']=='PASS';F=GF(2);checked=0
for name,c,bd,br in [('relative73',13,6,6),('relative73_nc',10,9,8)]:
 dat=(W/f'{name}_data.m').read_text();SS=lit(dat,'RelativeSSMatrices');JC=lit(dat,'RelativeCuspJets')
 for si,mat in enumerate(SS):
  B=matrix(F,mat);assert B.rank()==br
  for rec in[r for r in D['profiles']if r['case']==name and r['translate']==si]:
   pr=rec['caps'];loc=[(k,j)for k,n in enumerate(pr)for j in range(n)];A=matrix(F,[[JC[k][i][j]for k,j in loc]for i in range(len(mat))]);M=B.augment(A);assert M.rank()==br+rec['rank'];ix={v:i for i,v in enumerate(loc)}
   fib=[sum(1<<ix[k,j]for k in range(o,36,4))for o in range(4)for j in range(5)];qb=[int(z,16)for z in rec['quotient_basis']];R=matrix(F,[ZZ(z).digits(2,padto=len(loc))for z in fib+qb]);assert R.rank()==20+len(qb)==len(loc)+br-M.rank();assert (A*R.transpose()).column_space().is_subspace(B.column_space())
   # The known fiber vectors vanish after projection, and the retained quotient
   # basis spans every further relation, by the preceding independent rank test.
   cnt=0;smallest=None;v=0
   for j in range(1,1<<len(qb)):
    v^=qb[(j&-j).bit_length()-1];a=[0]*36
    for bit,(k,t)in enumerate(loc):
     if v>>bit&1:a[k]|=1<<t
    cost=sum(min(sum((a[k]^mask).bit_length()for k in range(o,36,4))for mask in range(32))for o in range(4));smallest=cost if smallest is None else min(smallest,cost);assert cost>c;cnt+=1
   assert cnt==rec['classes_checked']and smallest==rec['min_unexpected_cost'];checked+=1
out={'status':'PASS','profiles':checked,'all_relation_spaces_independently_verified':True};(W/'relative73_relation_spaces_independent.json').write_text(json.dumps(out,indent=2)+'\n');print('S19_REL73_RELATION_SPACES_INDEPENDENT_PASS',checked,flush=True)
