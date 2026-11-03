from pathlib import Path
import json
from sage.all import QQ,PolynomialRing,NumberField
W=Path(__file__).resolve().parent;L=Path('/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/models_X1_n/FFFc31.txt');R=PolynomialRing(QQ,'x');x=R.gen();K=R.fraction_field();S=PolynomialRing(K,'y');y=S.gen()
text=''.join(L.read_text().replace('\\','').split()).replace('^','**');F=S(eval(text,{'x':S(x),'y':y}));B=x*x*y-x*y*y+y-1-2*(x-y)*x*x*y
res=F.resultant(B).numerator();print('RESULTANT_FACTORS',[(f.degree(),m)for f,m in res.factor()],flush=True)
f=next(f.monic()for f,m in res.factor()if f.degree()==12);N=NumberField(f,'a');a=N.gen();T=PolynomialRing(N,'Y');Y=T.gen();G=T(eval(text,{'x':a,'y':Y}));H=a*a*Y-a*Y*Y+Y-1-2*(a-Y)*a*a*Y;g=G.gcd(H);assert g.degree()==1;v=-g[0]/g[1]
dat={'N':31,'polynomial':[str(c)for c in f.list()],'y_numerator':[str(c)for c in v.polynomial().list()],'y_denominator':['1']};out=json.loads((W/'small_witnesses.json').read_text());out.append(dat);(W/'small_witnesses.json').write_text(json.dumps(out,indent=2)+'\n');print(dat,flush=True)
def expr(cs):return '('+'+'.join(f'({c})*t^{i}'for i,c in enumerate(cs))+')'
p=W/'verify_small_witnesses.m';s=p.read_text();s=s[:s.index('print "S12_SMALL_EXPLICIT_OCCURRENCES_COMPLETE"')];s+=f"f:={expr(dat['polynomial'])};assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq 12;x:=z;y:=Evaluate({expr(dat['y_numerator'])},z);r:=(x^2*y-x*y+y-1)/(x^2*y-x);s:=(x*y-y+1)/(x*y);b:=r*s*(r-1);c:=s*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and 31*P eq E!0;print \"S12_OCCURRENCE_VERIFIED prime=31 exact_field_degree=12 exact_point_order=true\";\n";s+='print "S12_SMALL_EXPLICIT_OCCURRENCES_COMPLETE";quit;\n';p.write_text(s)
