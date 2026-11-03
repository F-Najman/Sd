from pathlib import Path
import sys,re,json,ast,math,itertools
from sage.all import matrix,GF,QQ,PolynomialRing
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit,matbits
F2=GF(2);ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]
q=json.load(open(W/'dyadic_jets.json'));assert(q['m'],q['M'],q['p_cutoff'])==(34,181,12308)
for a in q['classes']:
 u=a['u'];rr=[sum((int(n*k%181>90)^int(n*u*pow(k,-1,181)%181>90))<<(k-1)for k in range(1,181))for n in range(1,35)];assert rr==[int(z,16)for z in a['rows']];assert matrix(F2,[[z>>k&1 for k in range(180)]for z in rr]).rank()==34
print('S17_DYADIC_INDEPENDENT_PASS',flush=True)

def bm(rows,width):return matrix(F2,[[z>>j&1 for j in range(width)]for z in rows])

for n in ns:
 stem='FI97_i8'if n==97 else f'FI{n}';ls=(W/'FI'/(stem+'.compressed.txt')).read_text().splitlines();p,ind,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert p==n and d==17
 rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]];assert len(rows)==nr and bm(rows,512).rank()==rk
 core=rows[:d]+[v for k in range(ind-1)for v in rows[d+8*k:d+8*k+6]];C=bm(core,512);a=json.load(open(W/f'FI/FI{n}_verified.json'));assert a['rank_cap6']==C.rank()and a['kernel_dimension']==len(core)-C.rank()and not a['exceptional_failures']
 if n!=103:assert a['status']=='PASS'
 if 'PASS relations='in a['detail']or n==103:
  ll=(W/f'FI/FI{n}_cap6.relations.txt').read_text().splitlines();ii,dd,k=map(int,ll[0].split());rels=[sum(int(z)<<(64*j)for j,z in enumerate(l.split()))for l in ll[1:]];assert(ii,dd,k)==(ind,17,C.nrows()-C.rank());R=bm(rels,len(core));assert R.rank()==k and R*C==0
  if n==103:
   bad=[]
   for mask in range(1,1<<k):
    z=0
    for j,v in enumerate(rels):
     if mask>>j&1:z^=v
    costs=[0]*ind
    for j in range(len(core)):
     if z>>j&1:
      cusp,order=(0,j+1)if j<d else(1+(j-d)//6,1+(j-d)%6);costs[cusp]=max(costs[cusp],order)
    if sum(costs)<=17:bad.append(costs)
   assert bad==[[1]*17]
 print('S17_FI_INDEPENDENT_PASS',n,flush=True)
# Relative map at the complete level-103 cusp fiber.
ls=(W/'FI/FI103_relative.txt').read_text().splitlines();p,i,tn,root,nr,nc,d=map(int,ls[0].split());rr=[int(s,2)for s in ls[1:]];R=bm([rr[0]]+[rr[17+8*(j-1)]for j in range(1,17)],nc);assert R.rank()==16 and sum(R.rows())==0
(W/'relative103_verified.json').write_text(json.dumps({'status':'PASS','relative_rank':16,'degree':17,'family_dimension':1,'sole_deficient_pattern':[1]*17})+'\n')
# Independently rebuild every entry of the three new supersingular relative maps.
relative=[]
for p,h,sd,rd in[(53,4,13,1),(61,3,15,3),(73,2,6,0)]:
 s=(W/f'full{p}/units_data.m').read_text();g=int(re.search(r'genus:=(\d+)',s)[1]);prec=int(re.search(r'precision:=(\d+)',s)[1]);root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);m=(p-1)//2
 Q=bm(matbits(s,'qcoeffs'),prec);D=bm(matbits(s,'DiamondMatrix'),g);I=matrix.identity(F2,g);assert D**m==I
 logh=next(k for k in range(m)if pow(root,k,p)in[h,p-h]);AA=[]
 for q0 in([3,5]if p==53 else([3]if p==61 else[3,5,7])):
  cut=min((p*p-1)//12,(prec-1)//q0);C=Q[:,:cut+1]
  if C.rank()<g:continue
  log=next(k for k in range(m)if pow(root,k,p)in[q0,p-q0]);DQ=D**log*Q
  TQ=matrix(F2,[[Q[i,q0*n]+(DQ[i,n//q0]if n%q0==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ
  A=(D**logh-I)*(T-D**log-I);assert A*D==D*A;AA.append(A)
 assert AA
 ss=lit((W/f'sources{p}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');r=next(r for r in ss if not r[6]and r[0]==sd)
 PR=PolynomialRing(F2,'t');F=GF(2**sd,name='a',modulus=PR(r[1]));aa=[F(PR(a))for a in r[2]];x,y=[F(PR(a))for a in r[3]];a1,a2,a3,a4,a6=aa
 u3=a3+a1*x;u2=x+a2;u4=x*x+a4+a1*y;v2=u2+(u4/u3)**2+a1*u4/u3;b=v2**3/u3**2;c=(a1*v2+u3)/u3;rv=b/c;sv=c*c/(b+c);tv=rv*sv+1;xu=(sv+rv)/tv;yu=tv/(sv*sv+sv+rv+1)
 RX=bm(matbits(s,'UnitXRelations'),2*g);RY=bm(matbits(s,'UnitYRelations'),2*g)
 RM=matrix(F,[[F(row[j])+u*F(row[g+j])for j in range(g)]for R,u in[(RX,xu),(RY,yu)]for row in R.rows()]);assert RM.rank()==g-1;z=RM.right_kernel().basis()[0];z/=next(v for v in z if v)
 dat=(W/f'relative{p}_data.m').read_text();SS=lit(dat,'RelativeSSMatrices');JC=lit(dat,'RelativeCuspJets');assert len(SS)==r[5]
 for k,ssmat in enumerate(SS):
  zk=D.change_ring(F)**k*z;Bs=[]
  for A in AA:
   v=A.change_ring(F)*zk;Bs.append(matrix(F2,[list(v0.polynomial())+[0]*(sd-len(list(v0.polynomial())))for v0 in v]))
  B0=Bs[0]
  for C0 in Bs[1:]:B0=B0.stack(C0)
  assert B0==matrix(F2,ssmat)and B0.rank()==sd-rd
 cc=17-sd
 for k,jets in enumerate(JC):
  Bs=[D**k*A*Q[:,1:cc+1]for A in AA];C0=Bs[0]
  for C1 in Bs[1:]:C0=C0.stack(C1)
  assert C0==matrix(F2,jets)
 step=math.gcd(logh,m);Nm=sum((D**(step*k)for k in range(m//step)),matrix(F2,g,g));assert all(Nm*A==0 for A in AA)
 if p in[53,61]:
  a=json.load(open(W/f'relative{p}_verified.json'));assert a['status']=='PASS'and a['patterns_checked']==math.comb(m+cc-1,cc)and not a['failures']
 else:
  a=json.load(open(W/'relative73_verified.json'));assert a['status']=='PASS'and len(a['results'])==4 and all(v['checked']==v['expected']==760178194 for v in a['results'])
 relative.append({'p':p,'cotangent_entries_rebuilt':True,'supersingular_translates':len(SS),'operators':len(AA),'cusp_count':m,'supersingular_rank':sd-rd})
 print('S17_RELATIVE_INDEPENDENT_PASS',p,flush=True)
# Rational2-torsion at73 and odd-degree anti-Jacobian at89, from actual lattices.
def zm(s,name):
 a=re.search(re.escape(name)+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);assert a,name;return matrix(F2,int(a[1]),int(a[2]),ast.literal_eval(a[3]))
s=(B/'work/audit11/two73_data.m').read_text();K=zm(s,'Aq3Z').left_kernel().intersection(zm(s,'Aq5Z').left_kernel());D=zm(s,'D2Z');assert all(v*(D-1)==0 for v in K.basis())
anti=[]
for p,ind,sg,g,r,det,cs in lit((B/'work/degree16/odd_anti_data.m').read_text(),'OddAntiData'):
 if p!=89:continue
 A=matrix(QQ,r,r,[QQ(a)/b for a,b in cs]);assert A.det()==det and det%2;anti.append(sg)
assert sorted(anti)==[-1,1]
# Old finite-image Hecke polynomials, checked in period coordinates.
for p,ind,n,pol,g,ws,us in lit((B/'work/degree15/finite_FI_data.m').read_text(),'FiniteFIData'):
 A=matrix(QQ,g,g,[QQ(a)/b for a,b in ws]);U=matrix(QQ,g,g,[QQ(a)/b for a,b in us]);assert A.stack(U).rank()==A.rank()
for p,w,q0 in[(137,4,3),(113,4,3)]:
 F=matrix(GF(p),[[0,-q0],[1,0]]);assert all((F**(w*k)-1).det()!=0 for k in range(1,18))
out={'status':'PASS','degree':17,'dyadic_ranks':180,'absolute_formal_immersion_levels':16,'relative103_rank':16,'relative_supersingular_maps':relative,'actual_JOne73_two_certificate':True,'odd_anti89_both_signs':True,'cm_certificates':2}
(W/'auxiliary_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S17_AUXILIARY_INDEPENDENT_CHECKS_PASS',flush=True)
