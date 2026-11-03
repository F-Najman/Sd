"""Independent combinatorial completeness of all multiplicity profiles."""
from pathlib import Path
import json,itertools,re,math,hashlib
from functools import lru_cache
from sage.all import Partitions,PolynomialRing,ZZ,GF,matrix
W=Path(__file__).resolve().parent;out=[]
@lru_cache(None)
def expected(m,c,cap):
 ans={tuple([c]+[cap]*(m-1))}
 for pp in Partitions(c):
  h=len(pp)
  if h<2 or min(pp)<=cap:continue
  groups=[(v,list(pp[1:]).count(v))for v in sorted(set(pp[1:]),reverse=True)]
  def place(i,available,row):
   if i==len(groups):ans.add(tuple(row));return
   value,count=groups[i]
   for positions in itertools.combinations(available,count):
    rr=row[:]
    for j in positions:rr[j]=value
    rest=tuple(j for j in available if j not in positions);place(i+1,rest,rr)
  row=[cap]*m;row[0]=int(pp[0]);place(0,tuple(range(1,m)),row)
 return frozenset(ans)
cases=[('relative61_o20', 2, 1, 6), ('full_cusps61_sharp', 22, 4, 1), ('full_cusps89', 22, 5, 1), ('full_cusps97_sharp', 22, 5, 1), ('full_cusps71', 22, 4, 1), ('full_cusps127', 22, 5, 1), ('relative61', 7, 3, 1), ('relative61_ss20', 2, 1, 1), ('relative73', 16, 5, 4), ('relative73_nc', 13, 5, 4), ('relative109', 13, 5, 3), ('relative113_ordinary', 14, 5, 7), ('relative97_sharp', 6, 3, 2), ('full_cusps101_sharp', 22, 6, 1)]
for name,c,cap,translates in cases:
 a=json.loads((W/f'{name}_profiles_verified.json').read_text());assert a['status']=='PASS';p=int(re.search(r'\d+',name)[0]);m=(p-1)//2;want=expected(m,c,cap);rr=a['profiles'];assert{r['translate']for r in rr}==set(range(translates))
 for i in range(translates):assert{tuple(r['caps'])for r in rr if r['translate']==i}==want,name
 out.append({'case':name,'records':len(rr),'unique_profiles_per_translate':len(want),'translates':translates,'status':'PASS'})
for p in[59,79,83,103,107,109,113,131,137,139]:
 stem='FI97_i8'if p==97 else f'FI{p}';head=list(map(int,(W/'FI'/f'{stem}.compressed.txt').read_text().splitlines()[0].split()));m=head[1];cap=4 if p==59 else 5;a=json.loads((W/'FI'/f'FI{p}_verified.json').read_text());assert a['status']in['PASS','PASS_RELATIVE'];want=expected(m,22,cap);assert{tuple(r['caps'])for r in a['profiles']}==want,p;out.append({'case':f'FI{p}','records':len(a['profiles']),'unique_profiles':len(want),'status':'PASS'})
a=json.loads((W/'relative73_multiple_verified.json').read_text());assert a['status']=='PASS';keys={(r['case'],tuple(r['positions']))for r in a['profiles']};wantkeys={('SS2',v)for v in itertools.combinations_with_replacement(range(4),2)}|{('SS_NC',v)for v in itertools.product(range(4),repeat=2)};assert keys==wantkeys
for key in keys:
 rr=[r for r in a['profiles']if(r['case'],tuple(r['positions']))==key];c,cap=rr[0]['cusp_degree'],rr[0]['cap'];assert{tuple(r['caps'])for r in rr}==expected(36,c,cap)
out.append({'case':'relative73_multiple','records':len(a['profiles']),'all_positions_complete':True,'status':'PASS'})
direct=[];R=PolynomialRing(ZZ,'x');x=R.gen()
for p in[73]:
 a=json.loads((W/'FI'/f'FI{p}_verified.json').read_text());ls=(W/'FI'/f'FI{p}.compressed.txt').read_text().splitlines();head=list(map(int,ls[0].split()));m,d,rk=head[1],head[6],head[7];assert d==22 and a['status']=='PASS'and not a['exceptional_failures'];powers={u:sum(x**j for j in range(u+1))**(m-1)for u in range(1,7)};cnt=sum(int(powers[min(first,6)][22-first])for first in range(1,23));assert cnt==a['normalized_tuples_cap6']
 log=(W/'FI'/f'FI{p}_prefix.log').read_text();assert re.search(f'DECIC_PREFIX_CHECK level={p} degree=22 rank='+str(a['rank_cap6'])+' checked='+str(cnt)+' status=PASS',log)
 stats={}
 for total in range(14,23):
  for pp in Partitions(total,length=2,min_part=7):
   aa,bb=map(int,pp);rem=22-total;stats[f'{aa}+{bb}+rest{rem}']=(m-1)*math.comb(m+rem-3,rem)
 assert stats==a['exceptional_counts']
 rows=[sum(int(v)<<(64*j)for j,v in enumerate(line.split()))for line in ls[1:]]
 def block(j,n):return rows[:n]if j==0 else rows[d+11*(j-1):d+11*(j-1)+n]
 core=rows[:d]+[v for j in range(1,m)for v in block(j,6)];cl=(W/'FI'/f'FI{p}_cap6.compressed.txt').read_text().splitlines();assert[sum(int(v)<<(64*j)for j,v in enumerate(line.split()))for line in cl[1:]]==core
 triples=0
 for j,k in itertools.combinations(range(1,m),2):
  for lens in[(8,7,7),(7,8,7),(7,7,8)]:
   rr=block(0,lens[0])+block(j,lens[1])+block(k,lens[2]);assert matrix(GF(2),[ZZ(v).digits(2,padto=rk)for v in rr]).rank()==22;triples+=1
 direct.append({'p':p,'cap6_tuples':cnt,'all_high_partition_counts_complete':True,'triple7_matrices_independently_ranked':triples})
(W/'profile_coverage_independent.json').write_text(json.dumps({'status':'PASS','records':sum(r['records']for r in out),'direct_cap6':direct,'method':'Sage integer partitions with independent placement of multiplicity groups; set equality after removing producer duplicates','results':out},indent=2)+'\n');print('S22_ALL_PROFILE_ENUMERATIONS_COMPLETE',sum(r['records']for r in out),flush=True)
