from pathlib import Path
import json,re,ast,sys,math
from sage.all import GF,QQ,matrix
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import lit
q=json.load(open(W/'dyadic_jets.json'));assert q['m']==32 and q['M']==157 and q['p_cutoff']==10048<66049
for a in q['classes']:
 u=a['u'];rr=[sum((int(n*k%157>78)^int(n*u*pow(k,-1,157)%157>78))<<(k-1)for k in range(1,157))for n in range(1,33)];assert rr==[int(z,16)for z in a['rows']];assert matrix(GF(2),[[z>>k&1 for k in range(156)]for z in rr]).rank()==32
print('S16_DYADIC_SAGE_PASS',flush=True)
ns=[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
for n in ns:
 stem='FI97_i8'if n==97 else f'FI{n}';ls=(W/'FI'/(stem+'.compressed.txt')).read_text().splitlines();p,ind,tn,root,nr,nc,d,rk=map(int,ls[0].split());assert p==n and d==16
 rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]];assert len(rows)==nr
 A=matrix(GF(2),[[z>>j&1 for j in range(512)]for z in rows]);assert A.rank()==rk
 core=rows[:16]+[v for k in range(ind-1)for v in rows[16+8*k:16+8*k+6]];C=matrix(GF(2),[[z>>j&1 for j in range(512)]for z in core]);a=json.load(open(W/f'FI/FI{n}_verified.json'));assert a['status']=='PASS'and a['rank_cap6']==C.rank()and a['kernel_dimension']==len(core)-C.rank()and not a['exceptional_failures']
 if 'PASS relations='in a['detail']:
  ll=(W/f'FI/FI{n}_cap6.relations.txt').read_text().splitlines();ii,dd,k=map(int,ll[0].split());rels=[sum(int(z)<<(64*j)for j,z in enumerate(l.split()))for l in ll[1:]];assert (ii,dd,k)==(ind,16,C.nrows()-C.rank())
  R=matrix(GF(2),[[z>>j&1 for j in range(len(core))]for z in rels]);assert R.rank()==k and R*C==0
 print('S16_FI_SAGE_PASS',n,flush=True)
# Actual Jacobian rational2-torsion upper bounds.
def load_mat(s,name):
 a=re.search(re.escape(name)+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);assert a,name
 return matrix(GF(2),int(a[1]),int(a[2]),ast.literal_eval(a[3]))
s=(W/'two43_h7_data.m').read_text();K=load_mat(s,'Aq3Z').left_kernel().intersection(load_mat(s,'Aq5Z').left_kernel()).intersection(load_mat(s,'Aq7Z').left_kernel());D=load_mat(s,'DaZ');assert all(v*(D-1)==0 for v in K.basis())
for n,old,qs in[(53,B/'work/degree13/two53_data.m',[3,5]),(61,B/'work/degree15/two61_data.m',[3,5,7])]:
 s=old.read_text();K0=load_mat(s,f'Aq{qs[0]}Z').left_kernel()
 for q in qs[1:]:K0=K0.intersection(load_mat(s,f'Aq{q}Z').left_kernel())
 assert K0.dimension()==0
s=(B/'work/audit11/two73_data.m').read_text();K73=load_mat(s,'Aq3Z').left_kernel().intersection(load_mat(s,'Aq5Z').left_kernel());D=load_mat(s,'D2Z');assert all(v*(D-1)==0 for v in K73.basis())
# Exact odd degrees on both Betti signs, independent of integral lattice choice.
anti=[]
for p,ind,sg,g,r,det,cs in lit((W/'odd_anti_data.m').read_text(),'OddAntiData'):
 A=matrix(QQ,r,r,[QQ(a)/b for a,b in cs]);assert A.det()==det and det%2;anti.append({'N':p,'index':ind,'sign':sg,'dimension':r,'determinant':str(det)})
assert len(anti)==4
# Correct period-basis winding inclusions, including the full index12 quotient at193.
for p,ind,g,r,ws,us in lit((W/'new_finite_data.m').read_text(),'NewFiniteData'):
 A=matrix(QQ,g,g,[QQ(a)/b for a,b in ws]);U=matrix(QQ,g,g,[QQ(a)/b for a,b in us]);assert A.rank()==r and A.stack(U).rank()==r
for p,ind,n,pol,g,ws,us in lit((B/'work/degree15/finite_FI_data.m').read_text(),'FiniteFIData'):
 A=matrix(QQ,g,g,[QQ(a)/b for a,b in ws]);U=matrix(QQ,g,g,[QQ(a)/b for a,b in us]);assert A.stack(U).rank()==A.rank()
# All 210 cusp complements for the degree14 lift at41.
s=(W/'known41_tangents.m').read_text();ms=re.findall(r'Append\(~TangentMatrices,(.*?)\);',s,re.S);assert len(ms)==210
for a in ms:assert matrix(GF(2),ast.literal_eval(a)).rank()==16
# All 231 cusp complements for the ordinary degree14 lift at43.
records=lit((W/'known43_cot_data.m').read_text(),'Known43CotangentData');si,d,rr,js=next(v for v in records if v[0]==91);assert d==14
cnt=0
for j in range(21):
 for k in range(j,21):
  rows=[a+(js[j][i][:2]if j==k else[js[j][i][0],js[k][i][0]])for i,a in enumerate(rr)];assert matrix(GF(2),rows).rank()==16;cnt+=1
assert cnt==231
# Rational gonality53: complete rational-prefix rank and nonrational additions.
a=json.load(open(W/'gonality53.json'));b=json.load(open(W/'gonality53_nonrat.json'));assert a['status']==b['status']=='PASS'and a['gonality_lower_bound']==b['gonality_lower_bound']==20
ls=(W/'gon53.compressed.txt').read_text().splitlines();rr=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in ls[1:]];assert matrix(GF(2),[[z>>j&1 for j in range(92)]for z in rr]).rank()==66
# Independently verify every finite-field Frobenius CM exclusion.
for p,j,w,q,tr in lit((W/'cm_small_data.m').read_text(),'CMData'):
 F=matrix(GF(p),[[0,-q],[1,tr]]);assert all((F**(w*k)-1).det()!=0 for k in range(1,17))
# All degree2 rational cusp patterns at the quotient for193.
ls=(W/'FI/FI193.txt').read_text().splitlines();rr=[int(s,2)for s in ls[1:]];assert len(rr)==13
for js in [[0,1]]+[[0,k]for k in range(2,13)]:assert matrix(GF(2),[[rr[i]>>j&1 for j in range(int(ls[0].split()[5]))]for i in js]).rank()==2
out={'status':'PASS','degree':16,'dyadic_ranks':156,'formal_immersion_levels':18,'known41_cusp_patterns':210,'known43_cusp_patterns':231,'gonality53_lower_bound':20,'new_finite_image_inclusions':2,'old_finite_image_inclusions':16,'odd_anti_certificates':anti,'rational_two43_upper_dimension':int(K.dimension()),'cm_frobenius_certificates':9,'quotient193_cusp_patterns':12}
(W/'auxiliary_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S16_AUXILIARY_INDEPENDENT_CHECKS_PASS',flush=True)
