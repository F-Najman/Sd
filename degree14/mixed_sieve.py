"""Rebuild multiplication and principal-divisor obstructions from actual points."""
from pathlib import Path
import sys,re,json,gzip,random,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from unit_arithmetic import lit,matbits,bits,xorrows,Field,decode_record,transform
N=int(sys.argv[1]);W=Path(__file__).resolve().parent;H=W/f'full{N}';tt=time.monotonic();rng=random.Random(20261028+N)
a=(H/'units_data.m').read_text();b=(H/'hecke_jets.m').read_text();scalar=lambda k:int(re.search(r'\b'+k+r':=(\d+);',a)[1])
g=scalar('genus');prec=scalar('precision');m=scalar('DiamondOrder');root=scalar('DiamondRoot');D=matbits(a,'DiamondMatrix');Q=matbits(a,'qcoeffs');mask=(1<<prec)-1
assert len(Q)==g and prec>(N*N-1)//12
class Span:
 def __init__(self,rows=()):
  self.p={}
  for v in rows:self.add(v)
 def add(self,v):
  while v:
   k=(v&-v).bit_length()-1
   if k in self.p:v^=self.p[k]
   else:self.p[k]=v;return True
  return False
 def quotient(self,v):
  for k,x in sorted(self.p.items()):
   if v>>k&1:v^=x
  return v
 def __len__(self):return len(self.p)
def kernel(rows):
 p={};out=[]
 for i,x in enumerate(rows):
  c=1<<i
  while x:
   k=(x&-x).bit_length()-1
   if k in p:y,d=p[k];x^=y;c^=d
   else:p[k]=(x,c);break
  else:out.append(c)
 return out
def pmul(x,y):
 if x.bit_count()<y.bit_count():x,y=y,x
 z=0
 while y:k=y&-y;z^=x<<(k.bit_length()-1);y^=k
 return z&mask
def tensor(qs,expected):
 n=len(qs);piv={};basis=[];pairs=[];T=[[0]*n for _ in range(n)]
 for i in range(n):
  for j in range(i,n):
   orig=pmul(qs[i],qs[j]);v=orig;c=0
   while v:
    k=v.bit_length()-1
    if k in piv:x,y=piv[k];v^=x;c^=y
    else:
     ix=len(basis);piv[k]=(v,c^(1<<ix));basis.append(orig);pairs.append([i,j]);c=1<<ix;break
   T[i][j]=T[j][i]=c
 assert len(basis)==expected,(N,n,len(basis),expected)
 for i in range(n):
  for j in range(i,n):assert xorrows(T[i][j],basis)==pmul(qs[i],qs[j])
 return T,basis,pairs
if N<=53:
 degree=2;_,Q,monomials=tensor(Q,3*g-3);n=len(Q);nprod=7*g-7;sturm=(N*N-1)//3
else:degree=1;n=g;nprod=3*g-3;monomials=[[i]for i in range(g)];sturm=(N*N-1)//6
assert prec>sturm
T,prodq,_=tensor(Q,nprod);print('AUDIT_PRODUCT_TENSOR',N,'dimensions',n,nprod,'Sturm',sturm,'precision',prec,'seconds',time.monotonic()-tt,flush=True)
meta=lit(b,'SourceMetadata');sr=lit(b,'SourceRecords');tr=lit(b,'SourceHeckeRecords');assert len(meta)==len(sr)==len(tr)
families={};keys={}
def orbit(rec,d):
 v=decode_record(rec);F=v['F'];z=v['jets'];assert len(z)==g and all(len(row)==8 for row in z)and F.normalize(z)==z;original=z;o=[]
 for k in range(m):
  key=F.key(z,d)
  if key not in keys:
   fid=len(keys)+1;keys[key]=fid;families[fid]={'F':F,'degree':d,'jets':z,'evals':{}}
  fid=keys[key];assert families[fid]['degree']==d;o.append(fid);z=transform(F,z,D)
 assert z==original
 return o
S=[];TS=[]
for md,s,targets in zip(meta,sr,tr):
 si,d,orb,jpol=md;so=orbit(s,d);assert len(set(so))==orb,(N,md,len(set(so)));S.append(so)
 ts=[(mult,orbit(r,td))for e,td,mult,r in targets];assert sum(mult*families[o[0]]['degree']for mult,o in ts)==4*d;TS.append(ts)
print('AUDIT_ALL_ACTUAL_POINT_ORBITS',N,'sources',len(sr),'families',len(families),'seconds',time.monotonic()-tt,flush=True)
def evaluation(fid,k):
 v=families[fid];assert 1<=k<=8,(N,fid,k)
 if k not in v['evals']:
  F=v['F'];z=v['jets'];zs=[]
  for mon in monomials:
   row=[1]+[0]*(k-1)
   for i in mon:row=F.smul(row,z[i][:k],k)
   zs.append(sum(x<<(F.d*j)for j,x in enumerate(row)))
  v['evals'][k]=zs
 return v['evals'][k],v['F'].d*k
def conditions(dd,positive):
 rows=[0]*n;width=0;deg=0;support=[]
 for fid,c in sorted(dd.items()):
  c=c if positive else-c
  if c<=0:continue
  ev,w=evaluation(fid,c);rows=[x|(y<<width)for x,y in zip(rows,ev)];width+=w;deg+=families[fid]['degree']*c;support.append([fid,c])
 return rows,width,deg,support
log3=next(k for k in range(m)if pow(root,k,N)in[3,N-3]);dk=(-log3)%m
alpha={61:{6:1,0:-1},97:{5:1,4:-1,3:-1,2:1,1:1,0:-1},101:{6:1,5:-1,1:1,0:-1}}.get(N,{1:1,0:-1})
if N in[41,47,59,71]:alpha={0:1}
assert N==73;alpha={4:1,0:-1}
results=[];unresolved=[];matrices=[]
for md,so,targets in zip(meta,S,TS):
 si,d,orb,jpol=md
 if d!=7:continue
 dd={}
 def add(fid,k):dd[fid]=dd.get(fid,0)+k
 for shift,c in alpha.items():
  for mult,o in targets:add(o[shift%m],c*mult)
  add(so[shift%m],-c);add(so[(dk+shift)%m],-3*c)
 bp,pw,pd,ps=conditions(dd,True);bm,nw,nd,ns=conditions(dd,False);assert pd==nd and pd<=4*d*sum(abs(c)for c in alpha.values()) and n>pd,(N,si,pd,n)
 kk=kernel(bp);assert len(kk)>=n-pd
 if not pd:
  rec={'source':si,'degree':d,'orbit':orb,'status':'ZERO_DIVISOR','positive_degree':0};unresolved.append(rec);results.append(rec);continue
 fv=kk[0];assert fv and xorrows(fv,bp)==0
 V=Span([xorrows(fv,[row[j]for row in T])for j in range(n)]);assert len(V)==n
 free=[j for j in range(nprod)if j not in V.p];rprod=nprod-n;assert len(free)==rprod
 rows=bm[:];hh=[];rank=len(Span(rows))
 for _ in range(20):
  hv=xorrows(rng.getrandbits(len(kk)),kk)
  if not hv or hv==fv:continue
  assert xorrows(hv,bp)==0;hh.append(hex(hv))
  for i in range(n):
   v=V.quotient(xorrows(hv,T[i]));rows[i]|=sum(((v>>j)&1)<<k for k,j in enumerate(free))<<(nw+rprod*(len(hh)-1))
  rank=len(Span(rows))
  if rank==n:break
 rec={'source':si,'degree':d,'orbit':orb,'positive_degree':pd,'positive_support':ps,'negative_support':ns,'rank':rank,'columns':nw+rprod*len(hh),'F':hex(fv),'H':hh,'status':'NONPRINCIPAL'if rank==n else'UNRESOLVED'};results.append(rec)
 if rank!=n:unresolved.append(rec)
 else:matrices.append({'source':si,'degree':d,'rows':[hex(x)for x in rows],'columns':rec['columns'],'rank':rank})
 print('AUDIT_SOURCE_RESULT',N,si,d,orb,rec['status'],'rank',rank,'elapsed',time.monotonic()-tt,flush=True)
out={'N':N,'status':'PASS_WITH_EXPLICIT_EXCEPTIONS'if unresolved else'PASS','canonical_genus':g,'alpha_coefficients':alpha,'section_degree':degree,'dimension':n,'product_dimension':nprod,'Sturm_bound':sturm,'precision':prec,'source_orbits':len(sr),'nonprincipal':len(matrices),'exceptions':unresolved,'results':results,'elapsed':time.monotonic()-tt}
(H/'mixed_sieve.json').write_text(json.dumps(out,indent=2)+'\n')
with gzip.open(H/'mixed_matrices.json.gz','wt')as f:json.dump(matrices,f,separators=(',',':'))
print('AUDIT_FULL_SIEVE_COMPLETE',N,'sources',len(sr),'nonprincipal',len(matrices),'exceptions',[(r['source'],r['degree'],r['orbit'])for r in unresolved],flush=True)
