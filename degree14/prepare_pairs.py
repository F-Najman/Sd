from pathlib import Path
W=Path(__file__).resolve().parent;s=(W/'full_sieve.py').read_text();a=s.index('for md,so,targets in zip(meta,S,TS):\n si,d,orb,jpol=md;dd={}');b=s.index(' bp,pw,pd,ps=conditions',a)
block='''import math
ss7=[j for j,v in enumerate(meta)if v[1]==7];tasks=[]
for aa in ss7:
 for bb in ss7:
  if aa>bb:continue
  oa,ob=meta[aa][2],meta[bb][2];shifts=range(oa//2+1)if aa==bb else range(math.gcd(oa,ob))
  for shift in shifts:tasks.append((aa,bb,shift))
for aa,bb,off in tasks:
 si=[meta[aa][0],meta[bb][0],off];d=14;orb=0;dd={}
 def add(fid,k):dd[fid]=dd.get(fid,0)+k
 for ix,offset in[(aa,0),(bb,off)]:
  so=S[ix];targets=TS[ix]
  for shift,c in alpha.items():
   for mult,o in targets:add(o[(shift+offset)%m],c*mult)
   add(so[(shift+offset)%m],-c);add(so[(dk+shift+offset)%m],-3*c)
'''
s=s[:a]+block+s[b:];s=s.replace("H/'sieve.json'","H/'pair_sieve.json'").replace("H/'matrices.json.gz'","H/'pair_matrices.json.gz'");(W/'pair_sieve.py').write_text(s)
# The mixed SS6+ordinary7 case at73 uses the already-audited sigma^4 test.
s=(W/'full_sieve.py').read_text().replace('if N in[41,47,59,71]:alpha={0:1}','if N in[41,47,59,71]:alpha={0:1}\nassert N==73;alpha={4:1,0:-1}');s=s.replace('for md,so,targets in zip(meta,S,TS):\n si,d,orb,jpol=md;dd={}', 'for md,so,targets in zip(meta,S,TS):\n si,d,orb,jpol=md\n if d!=7:continue\n dd={}')
s=s.replace("H/'sieve.json'","H/'mixed_sieve.json'").replace("H/'matrices.json.gz'","H/'mixed_matrices.json.gz'");(W/'mixed_sieve.py').write_text(s)
