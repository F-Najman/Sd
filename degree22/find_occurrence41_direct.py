from pathlib import Path
import json
from sage.all import QQ,PolynomialRing
W=Path(__file__).resolve().parent;R=PolynomialRing(QQ,'t');t=R.gen();S=PolynomialRing(QQ,('x','y'));x,y=S.gens();src=Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/models_X1_n/FFFc41.txt').read_text();F=S(''.join(src.replace('\\','').split()).replace('^','**'));print('degrees',F.degree(x),F.degree(y),flush=True)
for c in [2,-1,3,-2,4,-3]:
 f=R(sum(v*c**i*t**j for(i,j),v in F.dict().items()))
 for h,e in f.factor():
  if h.degree()==22:
   a={'N':41,'polynomial':list(map(str,h.monic().list())),'x_numerator':[str(c)],'x_denominator':['1'],'y_numerator':['0','1'],'y_denominator':['1']};(W/'occurrence41.json').write_text(json.dumps(a,indent=2)+'\n');print('S22_EXACT_OCCURRENCE41_FOUND',c,flush=True);raise SystemExit(0)
raise RuntimeError('No degree22 specialization at tested constants')
