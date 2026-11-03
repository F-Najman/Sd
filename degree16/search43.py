from pathlib import Path
import json,itertools,random,re
from sage.all import QQ,GF,PolynomialRing,NumberField
W=Path(__file__).resolve().parent;L=Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/models_X1_n');R=PolynomialRing(QQ,'x');x=R.gen();S=PolynomialRing(QQ,('X','Y'));X,Y=S.gens();out=[];rng=random.Random(13)
for N in [43]:
 text=''.join((L/f'FFFc{N}.txt').read_text().replace('\\','').split()).replace('^','**');F=S(text.replace('x','X').replace('y','Y'));terms=F.dict();dy=int(F.degree(Y));found=False;tried=set();
 pairs=[(x**k+c,R.one())for k in range(1,9)for c in[-2,-1,0,1,2]]+[(R.one(),x**k+c)for k in range(1,9)for c in[-2,-1,0,1,2]]
 pairs +=[(a*x+b,c*x+d)for a,b,c,d in itertools.product(range(-2,3),repeat=4)if a*d-b*c]
 for k in range(20000):
  e=rng.randint(1,5);ee=rng.randint(0,5);pairs.append((R([rng.randint(-2,2)for _ in range(e+1)]),R([rng.randint(-2,2)for _ in range(ee+1)])))
 for P,Q in pairs:
  if not P or not Q or (P,Q)in tried:continue
  tried.add((P,Q));poly=sum(c*x**i*P**j*Q**(dy-j)for(i,j),c in terms.items())
  if poly.degree()<16:continue
  # A degree-13 factor must have a degree-13 factor or reducible factors mod a small prime; use full QQ factorization at low degrees.
  for f,m in poly.factor():
   if f.degree()!=16 or f.gcd(Q).degree():continue
   dat={'N':N,'polynomial':[str(c)for c in f.monic().list()],'y_numerator':[str(c)for c in P.list()],'y_denominator':[str(c)for c in Q.list()]};out.append(dat);(W/'search43_occurrences.json').write_text(json.dumps(out,indent=2)+'\n');print('S16_OCCURRENCE_FOUND',N,'trials',len(tried),flush=True);found=True;break
  if found:break
 print('S16_OCCURRENCE_SEARCH',N,'found',found,'trials',len(tried),flush=True)
 if not found:break

