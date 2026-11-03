"""Serre-duality proof of the F_2 gonality lower bound 16."""
from pathlib import Path
import re,ast,json,itertools,time,sys
from sage.all import GF,matrix
W=Path(__file__).resolve().parent;t=time.monotonic();s=(W/'gon43_dual_data.m').read_text();caps=ast.literal_eval(re.search(r'Caps:=(\[.*?\]);',s,re.S)[1]);raw=ast.literal_eval(re.search(r'HolomorphicJetMatrix:=Matrix\(GF\(2\),57,113,(\[.*?\])\);',s,re.S)[1]);assert caps==[13]+[5]*20 and len(raw)==57*113
J=matrix(GF(2),57,113,raw);assert J.rank()==57
cols=[sum(int(J[i,j])<<i for i in range(57))for j in range(113)];offset=list(itertools.accumulate([0]+caps))
def kernel(rows):
 p={};k=[]
 for i,x in enumerate(rows):
  c=1<<i
  while x:
   j=x.bit_length()-1
   if j in p:y,v=p[j];x^=y;c^=v
   else:p[j]=(x,c);break
  else:k.append(c)
 return k
def partitions(n,cap=None):
 if not n:yield[];return
 for v in range(min(n,cap or n),0,-1):
  for rest in partitions(n-v,v):yield[v]+rest
# Normalize the largest pole to rational cusp 1 using the diamond action.
parts=[p for p in partitions(15)if len(p)>=7];classes={};
for p in parts:
 if max(p)<=3:kind='max3'
 elif sum(x>1 for x in p)<=2:kind='two';assert p[0]<=9 and(p+[1])[1]<=5
 elif sum(x>2 for x in p)==1:kind='onebig';assert p[0]<=7 and all(x<=2 for x in p[1:])
 elif sum(x>2 for x in p)==2:kind='twobig';assert p[0]<=6 and p[1]<=4 and all(x<=2 for x in p[2:])
 else:kind='threebig';assert sum(x>2 for x in p)==3 and p[0]<=5 and p[1]<=4 and p[2]<=4 and all(x<=2 for x in p[3:])
 classes[tuple(p)]=kind
cases=[('max3',[0]+[3]*20)]
for P in range(21):
 e=[1]*21;e[0]+=8;e[P]+=4;cases.append(('two',e))
e=[2]*21;e[0]+=5;cases.append(('onebig',e))
for P in range(21):
 e=[2]*21;e[0]+=4;e[P]+=2;cases.append(('twobig',e))
for P,Q in itertools.combinations(range(1,21),2):
 e=[2]*21;e[0]+=3;e[P]+=2;e[Q]+=2;cases.append(('threebig',e))
results=[]
for kind,e in cases:
 assert all(0<=a<=b for a,b in zip(e,caps));inds=[offset[i]+j for i,a in enumerate(e)for j in range(a)];kk=kernel([cols[i]for i in inds]);assert len(kk)==len(inds)-J.matrix_from_columns(inds).rank()
 assert len(kk)<=18,(kind,e,len(kk));vectors=[0]
 for v in kk:vectors +=[a^v for a in vectors]
 records=[]
 for v in vectors[1:]:
  assert all(sum(((v>>j)&1)*int(J[i,ix])for j,ix in enumerate(inds))%2==0 for i in range(57))
  pos=0;deg=0
  for cap in e:deg+=((v>>pos)&((1<<cap)-1)).bit_length();pos+=cap
  assert deg>15,(kind,e,len(kk),hex(v),deg);records.append([hex(v),deg])
 results.append({'class':kind,'envelope':e,'principal_part_dimension':len(kk),'nonconstant_pole_degrees':[a[1]for a in records],'kernel_basis':[hex(v)for v in kk]})
for k in range(1,9):
 ss=(W/f'gon43_nonrat_{k}.log').read_text();assert f'AUDIT_GON43_NONRATIONAL_COMPLETE case={k} RR_dimension=1'in ss and not any(x in ss for x in['Runtime error','User error'])
out={'status':'PASS','conclusion':'gon_F2(X1(43)) >= 16; hence gon_Q(X1(43)) >= 16','rational_points':21,'missing_closed_degrees':[2,3,4,5,6],'partitions_15_with_length_at_least_7':len(parts),'envelopes':len(cases),'largest_principal_part_dimension':max(r['principal_part_dimension']for r in results),'partition_classes':[{'partition':list(p),'class':k}for p,k in classes.items()],'results':results,'elapsed':time.monotonic()-t}
(W/'gonality43.json').write_text(json.dumps(out,indent=2)+'\n');print('AUDIT_GON43_RIGOROUS_LOWER_BOUND_16_COMPLETE envelopes',len(cases),'partitions',len(parts),'max_dimension',out['largest_principal_part_dimension'],flush=True)
