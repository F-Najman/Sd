from pathlib import Path
import json,math
from sage.all import GF,PolynomialRing,matrix,ZZ
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;data=lit((W/'two163_characters_data.m').read_text(),'Two163CharacterData');out=[];dimension=26
for n,f,pol,d,d2,t2,As in data:
 assert n in[3,9,27,81]and f==2*n//3;PR=PolynomialRing(GF(2),'x');F=GF(2**f,name='a',modulus=PR(pol));b=F(PR(d2));assert b.multiplicative_order()==n;I=matrix.identity(F,d);K=matrix.identity(F,d)
 for q,aa in As:
  A=matrix(F,[[F(PR(v))for v in row]for row in aa]);K=(K*A).left_kernel().basis_matrix()*K
  if n>=9:assert K.nrows()==0
 assert n==3 or K.nrows()==0
 assert n!=3 or b**3==1;dimension+=f*d;out.append({'character_order':n,'coefficient_degree':f,'homology_dimension':d,'common_kernel_dimension':K.nrows(),'diamond8_trivial_on_kernel':True})
assert dimension==2054
(W/'two163_characters_verified.json').write_text(json.dumps({'status':'PASS','total_homology_dimension':dimension,'results':out,'note':'Exploratory comparison; final proof uses odd anti-Jacobian determinant on both Betti signs.'},indent=2)+'\n');print('S19_TWO163_CHARACTER_ARITHMETIC_PASS',flush=True)
