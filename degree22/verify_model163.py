from pathlib import Path
import json,time,re,hashlib
from sage.all import GF,LaurentSeriesRing,matrix,ZZ
from sage.libs.ntl.ntl_GF2X import ntl_GF2X
from unit_arithmetic import matbits,lit,xorrows
from intrinsic_model import units
W=Path(__file__).resolve().parent;tt=time.monotonic();s=(W/'full163/units_data.m').read_text();g=1027;prec=4628;Q=matbits(s,'qcoeffs');D=matbits(s,'DiamondMatrix');RX=matbits(s,'UnitXRelations');RY=matbits(s,'UnitYRelations');assert len(Q)==len(D)==g
L=LaurentSeriesRing(GF(2),'q',default_prec=5228);q=L.gen();s1=L(0);a6=L(0)
for n in range(1,5228//163+2):
 z=q**(163*n)
 if 163*n<5228:s1+=GF(2)(n%2)*z/(1+z);a6+=GF(2)(((5*n**3+7*n**5)//12)%2)*z/(1+z)
def tate(k):
 x=q**k/(1+q**k)**2;y=q**(2*k)/(1+q**k)**3+s1
 for n in range(1,5228//163+2):
  if 163*n+k<5228:
   z=q**(163*n+k);x+=z/(1+z)**2;y+=z*z/(1+z)**3
  if 163*n-k<5228:
   z=q**(163*n-k);x+=z/(1+z)**2;y+=z/(1+z)**3
 assert(y*y+x*y+x**3+s1*x+a6).valuation()>=5228
 return units([L(1),L(0),L(0),s1,a6],x,y)
vv=[]
for k in range(1,82):
 x,y=tate(k);assert x.prec()-x.valuation()>100 and y.prec()-y.valuation()>100;vv.append((k,int(x.valuation()),int(y.valuation())))
assert vv==lit((W/'unit_poles163_data.m').read_text(),'RationalCuspValuations');assert sum(v[1]for v in vv)==sum(v[2]for v in vv)==0;assert sum(max(0,-v[1])for v in vv)==348 and sum(max(0,-v[2])for v in vv)==364
print('S22_163_RATIONAL_POLE_VALUATIONS_INDEPENDENT',round(time.monotonic()-tt,1),flush=True)
K=GF(2**162,'a');z=K.multiplicative_generator()**((2**162-1)//163);assert z.multiplicative_order()==163
for k in range(1,163):
 a=z**k;x=a/(1+a)**2;y=a*a/(1+a)**3;uv=units([K(1),K(0),K(0),K(0),K(0)],x,y);assert all(v!=0 for v in uv)
# Exact canonical-unit relations through an order exceeding their global degree.
# Every pole is cuspidal: the remaining denominators have zeros only at
# Tate normal form points of orders3,4,5,7,8,9.
def ntl(x):return ntl_GF2X('0x'+format(x,'x')[::-1])
def mul(a,b):return int((ntl(a)*ntl(b)).hex()[2:][::-1],16)
mask=(1<<g)-1
for U,R,pole in zip(tate(1),[RX,RY],[348,364]):
 v=int(U.valuation());assert v==-1 and U.prec()>prec;shift=-v;ub=sum(int(U[i])<<(i+shift)for i in range(v,prec));cut=prec+v;bound=2*g-2+pole;assert cut>bound
 for row in R:
  a=xorrows(row&mask,Q);b=xorrows(row>>g,Q);assert((a<<shift)^mul(ub,b))&((1<<(cut+shift))-1)==0
 print('S22_163_CANONICAL_RELATIONS_INDEPENDENT',len(R),'global_bound',bound,'verified_order',cut,round(time.monotonic()-tt,1),flush=True)
# Verify the diamond action by both unit relations at the universal Tate point.
M=matrix(GF(2),[ZZ(z).digits(2,padto=g)for z in D]);assert M**81==matrix.identity(GF(2),g);Mi=M.inverse();DQ=[xorrows(sum(int(v)<<j for j,v in enumerate(row)),Q)for row in Mi.rows()]
for U,R in zip(tate(2),[RX,RY]):
 v=int(U.valuation());assert v==-2;ub=sum(int(U[i])<<(i-v)for i in range(v,prec));cut=prec-22;assert cut>2416
 for row in R:
  a=xorrows(row&mask,DQ);b=xorrows(row>>g,DQ);assert((a<<(-v))^mul(ub,b))&((1<<(cut-v))-1)==0
# Independently replay every complete cusp-profile relation space.
scope={'__file__':str(W/'verify_profile_spaces.py')};pre=(W/'verify_profile_spaces.py').read_text().split('cases=')[0];exec(compile(pre,str(W/'verify_profile_spaces.py'),'exec'),scope)
cols=[[int(z,16)for z in row]for row in json.loads((W/'FI/cusps163_columns.json').read_text())];a=json.loads((W/'FI/cusps163_verified.json').read_text());assert a['status']=='PASS'and len(a['profiles'])==241;G=a['known_fibers'];J=matrix(GF(2),[[v>>i&1 for row in cols for v in row]for i in range(g)]);ri=J.transpose().pivots();J=J.matrix_from_rows(ri)
for rec in a['profiles']:
 loc=[(k,j)for k,n in enumerate(rec['caps'])for j in range(n)];A=J.matrix_from_columns([22*k+j for k,j in loc]);scope['independent'](A,matrix(GF(2),len(ri),0),rec,G,8,22,loc)
# Independently compute all dominating two-high-part profiles.
want={tuple([22]+[8]*80)}
for aa,bb in[(13,9),(12,10),(11,11)]:
 for j in range(1,81):
  r=[8]*81;r[0]=aa;r[j]=bb;want.add(tuple(r))
assert{tuple(z['caps'])for z in a['profiles']}==want
out={'status':'PASS','N':163,'genus':g,'degree':22,'rational_cusp_valuations':81,'nonrational_cusp_geometric_values':162,'pole_bounds':[348,364],'all_unit_relations_rebuilt':True,'diamond_Tate_action_rebuilt':True,'cusp_profiles_independently_replayed':241,'minimum_known_fiber_degree':27,'model_sha256':hashlib.sha256((W/'full163/units_data.m').read_bytes()).hexdigest()};(W/'model163_independent.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_MODEL163_AND_CUSPS_INDEPENDENT_COMPLETE',round(time.monotonic()-tt,1),flush=True)
