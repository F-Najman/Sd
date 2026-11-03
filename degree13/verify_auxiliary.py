from pathlib import Path
import re,json,sys,gzip,ast,subprocess
from sage.all import matrix,GF
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
s=(W/'mixed43_tangents.m').read_text();vs=re.findall(r'Append\(~TangentMatrices,(.*?)\);',s,re.S);assert len(vs)==21
for v in vs:assert matrix(GF(2),ast.literal_eval(v)).rank()==13
for N in[41,73]:
 a=json.load(open(W/f'full{N}/mixed_sieve.json'));assert a['status']=='PASS'and not a['exceptions'];ms=json.load(gzip.open(W/f'full{N}/mixed_matrices.json.gz','rt'))
 for v in ms:assert matrix(GF(2),[[int(row,16)>>j&1 for j in range(v['columns'])]for row in v['rows']]).rank()==a['dimension']
print('S13_SAGE_MIXED_MATRICES_VERIFIED',21,'tangents;',3,'nonprincipality',flush=True)
(W/'mixed_ranks_verified.json').write_text(json.dumps({'status':'PASS','degree12_plus_cusp_at43_tangents':21,'supersingular_ordinary_obstructions':3},indent=2)+'\n')
out=[]
for N in[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]:
 stem={43:'FI43_combined',79:'FI79_i39'}.get(N,f'FI{N}');ls=(W/'FI'/(stem+'.compressed.txt')).read_text().splitlines();lev,ind,tn,r,nr,nc,d,rk=map(int,ls[0].split());assert lev==N and d==13 and len(ls)==nr+1
 rows=[sum(int(v)<<(64*j)for j,v in enumerate(line.split()))for line in ls[1:]];assert matrix(GF(2),[[v>>j&1 for j in range(rk)]for v in rows]).rank()==rk
 if N==43:
  a=json.load(open(W/'FI/FI43_verified.json'));assert a['status']=='PASS'
 elif N==79:
  lsrel=(W/'FI/FI79_i39.compressed.relations.txt').read_text().splitlines();ii,dd,rr=map(int,lsrel[0].split());assert (ii,dd,rr)==(ind,d,nr-rk)==(39,13,25)
  rs=[sum(int(v)<<(64*j)for j,v in enumerate(line.split()))for line in lsrel[1:]];assert len(rs)==rr
  assert matrix(GF(2),[[c>>j&1 for j in range(nr)]for c in rs]).rank()==rr
  for c in rs:
   z=0
   for j,v in enumerate(rows):
    if c>>j&1:z^=v
   assert z==0
  r=subprocess.run([str(W/'relation_check'),str(W/'FI/FI79_i39.compressed.relations.txt')],capture_output=True,text=True,check=True);assert 'PASS relations=25 tested=33554431'in r.stdout;a={'N':N,'status':'PASS','method':'complete binary relation enumeration in C++','relations':25,'tested_relations':33554431}
 else:
  a=json.load(open(W/'FI'/f'FI{N}_verified.json'));assert a['status']=='PASS'
 out.append(a|{'selected_stem':stem,'rank_independently_verified':rk,'cusp_index':ind})
(W/'formal_immersion_final.json').write_text(json.dumps({'status':'PASS','degree':13,'results':out},indent=2)+'\n');print('S13_SAGE_FI_RANKS_VERIFIED',len(out),flush=True)
s=(W/'two53_data.m').read_text()
def loadmat(name):
 m=re.search(re.escape(name)+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);return matrix(GF(2),int(m[1]),int(m[2]),ast.literal_eval(m[3]))
D=loadmat('DaZ');K=loadmat('Aq3Z').left_kernel().intersection(loadmat('Aq5Z').left_kernel());assert K.dimension()==0
(W/'two53_verified.json').write_text(json.dumps({'status':'PASS','exact_JOne_homology':True,'dimension':D.nrows(),'rational_two_torsion_upper_dimension':0},indent=2)+'\n');print('S13_SAGE_TWO53_KERNEL_ZERO_VERIFIED',D.nrows(),flush=True)
