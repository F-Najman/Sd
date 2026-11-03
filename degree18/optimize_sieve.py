from pathlib import Path
W=Path(__file__).resolve().parent
s=(W/'full_sieve.py').read_text()
a=s.index('families={};keys={}')
b=s.index("print('AUDIT_ALL_ACTUAL_POINT_ORBITS'",a)
old=s[a:b]
new='''# Only the translates appearing in the integral annihilator are needed.
# The complete diamond orbit census was independently performed on actual (E,P).
log3=next(k for k in range(m)if pow(root,k,N)in[3,N-3]);dk=(-log3)%m
alpha={61:{6:1,0:-1},97:{12:1,0:-1},101:{6:1,5:-1,1:1,0:-1}}.get(N,{1:1,0:-1})
if N in[41,47,59,71]:alpha={0:1}
identity=[1<<i for i in range(g)];powers={0:identity,1:D}
def matmul(A,B):return[xorrows(row,B)for row in A]
def dpow(k):
 k%=m
 if k not in powers:
  if k%2:powers[k]=matmul(dpow(k-1),D)
  else:
   half=dpow(k//2);powers[k]=matmul(half,half)
 return powers[k]
# Verify the entire diamond action has its asserted order.
DM=identity[:];power=D[:];exponent=m
while exponent:
 if exponent&1:DM=matmul(DM,power)
 power=matmul(power,power);exponent//=2
assert DM==identity
source_shifts=sorted(set(k%m for k in alpha)|set((k+dk)%m for k in alpha));target_shifts=sorted(k%m for k in alpha)
for k in set(source_shifts+target_shifts):dpow(k)
families={};keys={}
def orbit(rec,d,shifts):
 v=decode_record(rec);F=v['F'];z=v['jets'];assert len(z)==g and all(len(row)==len(z[0])for row in z)and 1<=len(z[0])<=8 and F.normalize(z)==z
 o={}
 for k in shifts:
  zz=z if k==0 else transform(F,z,dpow(k));key=F.key(zz,d)
  if key not in keys:
   fid=len(keys)+1;keys[key]=fid;families[fid]={'F':F,'degree':d,'jets':zz,'evals':{}}
  fid=keys[key];assert families[fid]['degree']==d;o[k]=fid
 return o
S=[];TS=[]
for md,s,targets in zip(meta,sr,tr):
 si,d,orb,jpol=md;assert orb>0 and m%orb==0;so=orbit(s,d,source_shifts);S.append(so)
 ts=[(mult,orbit(r,td,target_shifts))for e,td,mult,r in targets];assert sum(mult*families[o[0]]['degree']for mult,o in ts)==4*d;TS.append(ts)
'''
s=s[:a]+new+s[b:]
(W/'full_sieve.py').write_text(s)
