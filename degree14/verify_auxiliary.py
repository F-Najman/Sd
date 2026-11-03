from pathlib import Path
import json,re,math,sys,ast,gzip
from sage.all import GF,matrix
W=Path(__file__).resolve().parent;B=W.parents[1];sys.path.insert(0,str(W));from unit_arithmetic import matbits
q=json.load(open(W/'dyadic_jets.json'));assert q['m']==28 and q['M']==157 and q['p_cutoff']==8792<16641
for v in q['classes']:
 u=v['u'];rows=[sum((int(n*a%157>78)^int(n*u*pow(a,-1,157)%157>78))<<(a-1)for a in range(1,157))for n in range(1,29)];assert rows==[int(x,16)for x in v['rows']];assert matrix(GF(2),[[z>>j&1 for j in range(156)]for z in rows]).rank()==28
table=(B/'work/audit11/derickx_stoll_table2.txt').read_text();listed=[]
for v in re.findall(r'(?<![A-Za-z])p&([^\\]+)',table):listed.extend(int(z)for z in v.split('&')if z.strip())
assert 127 not in listed and 113 not in listed
print('S14_DYADIC_MATRICES_INDEPENDENTLY_VERIFIED',156,flush=True)
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113];out=[]
for n in ns:
 stem='FI97_i8'if n==97 else f'FI{n}';p=W/'FI'/(stem+'.compressed.txt');lines=p.read_text().splitlines();h=list(map(int,lines[0].split()));lev,i,t,root,nr,nc,d,rk=h;assert lev==n and d==14
 rs=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in lines[1:]];assert len(rs)==nr;A=matrix(GF(2),[[v>>j&1 for j in range(512)]for v in rs]);assert A.rank()==rk
 for j in range(i-1):assert matrix(GF(2),[[v>>k&1 for k in range(512)]for v in rs[:7]+rs[d+7*j:d+7*j+7]]).rank()==14
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
(W/'formal_immersion.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n');print('S14_SELECTED_FI_AND_BALANCED_PAIRS_SAGE_VERIFIED',len(ns),flush=True)
# The previously audited zero bound on rational 2-torsion at53 is checked again.
s=(B/'work/degree13/two53_data.m').read_text()
def lm(n):
 v=re.search(re.escape(n)+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);return matrix(GF(2),int(v[1]),int(v[2]),ast.literal_eval(v[3]))
assert lm('Aq3Z').left_kernel().intersection(lm('Aq5Z').left_kernel()).dimension()==0
# Independently verify the full canonical matrix used in the gonality-53 test.
s=(W/'gon53.compressed.txt').read_text().splitlines();h=list(map(int,s[0].split()));rows=[sum(int(z)<<(64*k)for k,z in enumerate(l.split()))for l in s[1:]];assert matrix(GF(2),[[v>>j&1 for j in range(92)]for v in rows]).rank()==h[-1]==66
(W/'auxiliary_verified.json').write_text(json.dumps({'status':'PASS','dyadic_matrices':156,'formal_immersion_levels':16,'gonality53_rank':66,'rational_two53_upper_dimension':0},indent=2)+'\n');print('S14_AUXILIARY_CHECKS_PASS',flush=True)
