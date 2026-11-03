from pathlib import Path
import re,ast,gzip,json,concurrent.futures,time
from sage.all import matrix,GF,ZZ,identity_matrix
W=Path(__file__).resolve().parent

def one(N):
 H=W/f'full{N}';s=json.loads((H/'sieve.json').read_text());ms=json.loads(gzip.open(H/'matrices.json.gz','rt').read());assert len(ms)==s['nonprincipal'];n=s['dimension']
 for dat in ms:
  rows=[int(x,16)for x in dat['rows']];c=dat['columns'];assert len(rows)==n and all(x.bit_length()<=c for x in rows);assert matrix(GF(2),[[v>>j&1 for j in range(c)]for v in rows]).rank()==n,(N,dat['source'])
 print('AUDIT_INDEPENDENT_M4RI',N,len(ms),'rank',n,flush=True);return {'N':N,'matrices':len(ms),'rank':n,'status':'PASS'}
if __name__=='__main__':
 Ns=[37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
 with concurrent.futures.ProcessPoolExecutor(max_workers=4)as ex:rs=list(ex.map(one,Ns))
 def mat(s,name,ring=ZZ):
  m=re.search(name+r':=Matrix\(Integers\(\),(\d+),(\d+),(\[.*?\])\);',s,re.S);r,c=map(int,m.group(1,2));return matrix(ring,r,c,ast.literal_eval(m[3]))
 two=[]
 for N,dim in[(37,0),(43,6),(67,2),(71,0),(73,6)]:
  s=(W/f'two{N}_data.m').read_text();A=mat(s,'Aq3Z',GF(2)).augment(mat(s,'Aq5Z',GF(2)));D=mat(s,'DaZ',GF(2));K=A.left_kernel();assert K.dimension()==dim and(K.basis_matrix()*(D-identity_matrix(GF(2),D.nrows()))).rank()==0
  two.append({'N':N,'upper_bound_dimension':dim,'diamond_action_trivial':True})
 s=(W/'decic37_jets.m').read_text()
 def m2(name):
  m=re.search(name+r':=Matrix\(GF\(2\),(\d+),(\d+),(\[.*?\])\);',s,re.S);r,c=map(int,m.group(1,2));return matrix(GF(2),r,c,ast.literal_eval(m[3]))
 C=m2('CartierMatrix');D=m2('DiamondMatrix');I=identity_matrix(GF(2),40);U=m2('ImageBasis');T=m2('DecicJets');assert U.rank()==38 and U.row_space()==(D-I).row_space() and U.row_space()==((C-I)*(D-I)).row_space()
 cs=re.findall(r'Append\(~CuspJets,Matrix\(GF\(2\),38,1,(\[.*?\])\)\);',s,re.S);assert len(cs)==18
 for csj in cs:assert T.augment(matrix(GF(2),38,1,ast.literal_eval(csj))).rank()==11
 out={'status':'PASS','ordinary_obstruction_matrices':sum(r['matrices']for r in rs),'results':rs,'rational_two_bounds':two,'decic_cusp_matrices':18,'decic_cusp_rank':11}
 (W/'independent_matrices.json').write_text(json.dumps(out,indent=2)+'\n');print('AUDIT_ALL_MATRICES_AND_RATIONAL_TWO_REPLAY_COMPLETE',out['ordinary_obstruction_matrices'],flush=True)
