from pathlib import Path
import sys
P=Path(sys.argv[1]);ls=P.read_text().splitlines();v=list(map(int,ls[0].split()));piv={};rows=[];basis=[];original=[]
for s in ls[1:]:
 x=int(s,2);original.append(x);c=0
 while x:
  k=x.bit_length()-1
  if k in piv:a,b=piv[k];x^=a;c^=b
  else:
   bit=1<<len(piv);piv[k]=(x,c^bit);basis.append(original[-1]);c=bit;break
 rows.append(c)
assert len(piv)<=256
for a,c in zip(original,rows):
 r=0
 for k,b in enumerate(basis):
  if (c>>k)&1:r^=b
 assert a==r
out=P.with_suffix('.compressed.txt')
with out.open('w')as f:
 f.write(' '.join(map(str,v+[len(piv)]))+'\n')
 for c in rows:f.write(' '.join(str(c>>(64*k)&((1<<64)-1))for k in range(4))+'\n')
print('COMPRESSED',P.name,'rank',len(piv))
