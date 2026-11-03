"""Independent Sage ranks of complete relation spaces on every profile."""
from pathlib import Path
import json,time,sys
from sage.all import GF,matrix,ZZ
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
F=GF(2);start=time.monotonic();out=[]
def bits(x,n):return ZZ(x).digits(2,padto=n)
def independent(A,B,rec,groups,cap,c,loc):
 n=len(loc);br=B.rank();M=B.augment(A);assert M.rank()==br+rec['rank']
 ix={v:i for i,v in enumerate(loc)}
 fib=[sum(1<<ix[k,j]for k in orb)for orb in groups for j in range(cap)]
 qb=[int(x,16)for x in rec['quotient_basis']];rr=fib+qb
 if rr:
  R=matrix(F,[bits(x,n)for x in rr]);assert R.rank()==len(rr)==n+br-M.rank()
  assert(A*R.transpose()).column_space().is_subspace(B.column_space())
 else:assert M.rank()==n+br
 assert len(fib)==rec['known_fiber_relations']and len(qb)==rec['quotient_kernel_dimension']
 # Enumerate cosets in binary order, independently of the producer's Gray code.
 vs=[0]
 for b in qb:vs += [v^b for v in vs]
 minimum=None;covered={k for orb in groups for k in orb}
 for v in vs[1:]:
  cf=[0]*(max(k for k,j in loc)+1)
  while v:
   low=v&-v;k,j=loc[low.bit_length()-1];cf[k]|=1<<j;v-=low
  cost=sum(cf[k].bit_length()for k in range(len(cf))if k not in covered)
  for orb in groups:cost+=min(sum((cf[k]^mask).bit_length()for k in orb)for mask in range(1<<cap))
  assert cost>c;minimum=cost if minimum is None else min(minimum,cost)
 assert len(vs)-1==rec['classes_checked']and minimum==rec['min_unexpected_cost']
def check_case(name,c,bd,br,step,cap):
 dat=(W/f'{name}_data.m').read_text();JC=lit(dat,'RelativeCuspJets');SS=lit(dat,'RelativeSSMatrices');m=len(JC);groups=[list(range(o,m,step))for o in range(step)]if step else[]
 if not bd:SS=[[[]for r in JC[0]]]
 records=json.loads((W/f'{name}_profiles_verified.json').read_text());assert records['status']=='PASS';recs=records['profiles'];count=0
 # Every column occurs in this master matrix.  Independent row selection is
 # injective on its column space and avoids enormous repeated native row lists.
 J=matrix(F,[[JC[k][i][j]for k in range(m)for j in range(c)]for i in range(len(JC[0]))])
 for si,rr in enumerate(SS):
  B=matrix(F,rr);assert B.rank()==br;master=B.augment(J);ri=master.transpose().pivots();B=B.matrix_from_rows(ri);J0=J.matrix_from_rows(ri)
  for rec in [r for r in recs if r['translate']==si]:
   loc=[(k,j)for k,n in enumerate(rec['caps'])for j in range(n)];A=J0.matrix_from_columns([k*c+j for k,j in loc]);independent(A,B,rec,groups,cap,c,loc);count+=1
   if count%10000==0:print('S21_PROFILE_SPACES_PROGRESS',name,count,round(time.monotonic()-start,1),flush=True)
 assert count==len(recs);out.append({'case':name,'status':'PASS','profiles':count,'entire_relation_spaces':True});print('S21_PROFILE_SPACES_PASS',name,count,round(time.monotonic()-start,1),flush=True)
cases=[('full_cusps71',21,0,0,0,4),('full_cusps127',21,0,0,1,5),('relative53',8,13,12,2,3),('full_cusps53',21,0,0,2,3),('relative61',6,15,12,6,3),('relative61_ss20',1,20,16,6,1),('relative73',15,6,6,4,5),('relative73_nc',12,9,8,4,5),('relative109',12,9,8,6,5),('relative113_ordinary',13,8,7,7,5),('relative97_sharp',5,16,16,16,3),('full_cusps101_sharp',21,0,0,1,6)]
for args in cases:check_case(*args)
for p in [59,79,83,89,97,103,107,109,113,131,137,139]:
 stem='FI97_i8'if p==97 else f'FI{p}';ls=(W/'FI'/f'{stem}.compressed.txt').read_text().splitlines();pp,m,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert pp==p and d==21
 vals=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]]
 cols=[vals[:d]]+[vals[d+10*(k-1):d+10*k]for k in range(1,m)]
 J=matrix(F,[[v>>i&1 for cc in cols for v in cc]for i in range(rk)]);offsets=[0]
 for cc in cols:offsets.append(offsets[-1]+len(cc))
 records=json.loads((W/'FI'/f'FI{p}_verified.json').read_text());assert records['status']in['PASS','PASS_RELATIVE'];groups=records['known_groups'];cap=4 if p==59 else 5
 for rec in records['profiles']:
  loc=[(k,j)for k,n in enumerate(rec['caps'])for j in range(n)];A=J.matrix_from_columns([offsets[k]+j for k,j in loc]);independent(A,matrix(F,rk,0),rec,groups,cap,21,loc)
 out.append({'case':stem,'status':'PASS','profiles':len(records['profiles']),'entire_relation_spaces':True});print('S21_PROFILE_SPACES_PASS',stem,len(records['profiles']),round(time.monotonic()-start,1),flush=True)
dat=(W/'relative73_multiple_data.m').read_text();SS=lit(dat,'SS73ClosedJets');NC=lit(dat,'SS73NC');JC=lit(dat,'SS73CuspJets');recs=json.loads((W/'relative73_multiple_verified.json').read_text())['profiles'];groups=[list(range(i,36,4))for i in range(4)]
for rec in recs:
 name=rec['case'];pos=rec['positions'];c=rec['cusp_degree'];cap=rec['cap'];br=rec['base_rank']
 if name=='SS_NC':base=[SS[pos[0]][r][:6]+NC[pos[1]][r]for r in range(len(SS[0]))]
 else:
  counts={i:pos.count(i)for i in set(pos)};base=[[a for i,m in counts.items()for a in SS[i][r][:6*m]]for r in range(len(SS[0]))]
 B=matrix(F,base);assert B.rank()==br;J=matrix(F,[[JC[k][i][j]for k in range(36)for j in range(c)]for i in range(len(JC[0]))]);ri=B.augment(J).transpose().pivots();B=B.matrix_from_rows(ri);J=J.matrix_from_rows(ri);loc=[(k,j)for k,n in enumerate(rec['caps'])for j in range(n)];A=J.matrix_from_columns([k*c+j for k,j in loc]);independent(A,B,rec,groups,cap,c,loc)
out.append({'case':'relative73_multiple','status':'PASS','profiles':len(recs),'entire_relation_spaces':True})
(W/'profile_spaces_independent.json').write_text(json.dumps({'status':'PASS','degree':21,'results':out},indent=2)+'\n');print('S21_PROFILE_SPACES_INDEPENDENT_COMPLETE',sum(r['profiles']for r in out),flush=True)
