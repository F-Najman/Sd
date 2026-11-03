from pathlib import Path
import json,re,math,sys,ast,gzip
from sage.all import GF,matrix,QQ
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import matbits,lit
q=json.load(open(W/'dyadic_jets.json'));assert q['m']==30 and q['M']==157 and q['p_cutoff']==9420<33131
for v in q['classes']:
 u=v['u'];rows=[sum((int(n*a%157>78)^int(n*u*pow(a,-1,157)%157>78))<<(a-1)for a in range(1,157))for n in range(1,31)];assert rows==[int(x,16)for x in v['rows']];assert matrix(GF(2),[[z>>j&1 for j in range(156)]for z in rows]).rank()==30
table=(B/'work/audit11/derickx_stoll_table2.txt').read_text();listed=[]
for v in re.findall(r'(?<![A-Za-z])p&([^\\]+)',table):listed.extend(int(z)for z in v.split('&')if z.strip())
assert 127 not in listed and 113 not in listed
print('S15_DYADIC_MATRICES_INDEPENDENTLY_VERIFIED',156,flush=True)
ns=[41,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113];out=[]
for n in ns:
 stem='FI97_i8'if n==97 else f'FI{n}';p=W/'FI'/(stem+'.compressed.txt');lines=p.read_text().splitlines();h=list(map(int,lines[0].split()));lev,i,t,root,nr,nc,d,rk=h;assert lev==n and d==15
 rs=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in lines[1:]];assert len(rs)==nr;A=matrix(GF(2),[[v>>j&1 for j in range(512)]for v in rs]);assert A.rank()==rk
 for j in range(i-1):assert matrix(GF(2),[[v>>k&1 for k in range(512)]for v in rs[:8]+rs[d+7*j:d+7*j+7]]).rank()==15
 for j in range(i-1):
  for k in range(i-1):
   if j!=k:assert matrix(GF(2),[[v>>t&1 for t in range(512)]for v in rs[:7]+rs[d+7*j:d+7*j+7]+[rs[d+7*k]]]).rank()==15
 core=rs[:d]+[v for j in range(i-1)for v in rs[d+7*j:d+7*j+6]];R=matrix(GF(2),[[v>>k&1 for k in range(512)]for v in core]);rkc=R.rank();a=json.load(open(W/f'FI/FI{n}_verified.json'));assert a['status']=='PASS'and a['rank_cap6']==rkc and a['kernel_dimension']==len(core)-rkc
 pp=W/f'FI/FI{n}_cap6.relations.txt'
 if pp.exists()and'PASS relations='in a['detail']:
  ll=pp.read_text().splitlines();ii,dd,kk=map(int,ll[0].split());assert (ii,dd,kk)==(i,d,len(core)-rkc);relations=[sum(int(v)<<(64*k)for k,v in enumerate(l.split()))for l in ll[1:]];assert len(relations)==kk
  assert matrix(GF(2),[[v>>j&1 for j in range(len(core))]for v in relations]).rank()==kk
  for v in relations:
   z=0
   for j,row in enumerate(core):
    if v>>j&1:z^=row
   assert z==0
 a['selected_stem']=stem;a['independent_full_rank']=int(rk);out.append(a)
(W/'formal_immersion.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n');print('S15_SELECTED_FI_AND_BALANCED_PAIRS_SAGE_VERIFIED',len(ns),flush=True)
# The previously audited zero bound on rational 2-torsion at53 is checked again.
s=(B/'work/degree13/two53_data.m').read_text()
def lm(n):
 v=re.search(re.escape(n)+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);return matrix(GF(2),int(v[1]),int(v[2]),ast.literal_eval(v[3]))
assert lm('Aq3Z').left_kernel().intersection(lm('Aq5Z').left_kernel()).dimension()==0
# Independently verify the full canonical matrix used in the gonality-53 test.
s=(W/'gon53.compressed.txt').read_text().splitlines();h=list(map(int,s[0].split()));rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in s[1:]];assert matrix(GF(2),[[v>>j&1 for j in range(92)]for v in rows]).rank()==h[-1]==66
# The actual JOne(73) 2-torsion upper bound is fixed by diamond 2.
s=(B/'work/audit11/two73_data.m').read_text();A3=lm('Aq3Z');A5=lm('Aq5Z');K=A3.left_kernel().intersection(A5.left_kernel());D=lm('D2Z');assert all(v*(D-1)==0 for v in K.basis())
# Twenty full cotangent matrices for the known irreducible degree-14 lift plus a cusp.
s=(W/'known41_tangents.m').read_text();records=re.findall(r'Append\(~TangentMatrices,(.*?)\);',s,re.S)
assert len(records)==20
for a in records:assert matrix(GF(2),ast.literal_eval(a)).rank()==15
# Independently check each recorded finite-image inclusion in the correct period basis.
a=lit((W/'finite_FI_data.m').read_text(),'FiniteFIData');assert len(a)==16
for p,ind,n,pol,g,ws,us in a:
 V=matrix(QQ,g,g,[QQ(z[0])/z[1]for z in ws]);U=matrix(QQ,g,g,[QQ(z[0])/z[1]for z in us]);assert V.stack(U).rank()==V.rank()
s=(W/'two61_data.m').read_text();K61=lm('Aq3Z').left_kernel().intersection(lm('Aq5Z').left_kernel()).intersection(lm('Aq7Z').left_kernel());assert K61.dimension()==0
(W/'auxiliary_verified.json').write_text(json.dumps({'status':'PASS','dyadic_matrices':156,'formal_immersion_levels':17,'gonality53_rank':66,'rational_two53_upper_dimension':0,'rational_two61_upper_dimension':0,'rational_two73_upper_dimension':int(K.dimension()),'known41_tangents':20,'finite_image_inclusions':16},indent=2)+'\n');print('S15_AUXILIARY_CHECKS_PASS',flush=True)
