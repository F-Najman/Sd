from pathlib import Path
import sys,re,json,itertools
from sage.all import GF,matrix
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import matbits
F=GF(2)
def bm(rr,n):return matrix(F,[[v>>j&1 for j in range(n)]for v in rr])
def rank(rr):
 b={}
 for x in rr:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return len(b)
out=[]
for p,ind in[(103,17),(131,13)]:
 s=(W/f'full{p}/units_data.m').read_text();g=int(re.search(r'genus:=(\d+)',s)[1]);prec=int(re.search(r'precision:=(\d+)',s)[1]);root=int(re.search(r'DiamondRoot:=(\d+)',s)[1]);m=(p-1)//2;Q=bm(matbits(s,'qcoeffs'),prec);D=bm(matbits(s,'DiamondMatrix'),g);I=matrix.identity(F,g)
 V=(D**ind-I).left_kernel().basis_matrix();q=3;cut=min((p*p-1)//12,(prec-1)//q);C=Q[:,:cut+1];assert C.rank()==g;k=next(k for k in range(m)if pow(root,k,p)in[q,p-q]);DQ=D**k*Q;TQ=matrix(F,[[Q[i,q*n]+(DQ[i,n//q]if n%q==0 else 0)for n in range(cut+1)]for i in range(g)]);T=C.solve_left(TQ);assert T*C==TQ;A=(D-I)*(T-D**k-I);assert A*D==D*A;assert V*A*D**ind==V*A
 CJ=[V*A*D**j*Q[:,1:23]for j in range(ind)];cols=[[sum(int(CJ[j][i,k])<<i for i in range(V.nrows()))for k in range(22)]for j in range(ind)];ranks={}
 for pos in itertools.combinations_with_replacement(range(ind),22-ind):
  mult=[1+pos.count(j)for j in range(ind)];rr=[v for j,c in enumerate(mult)for v in cols[j][:c]];r=rank(rr);assert r==21,(p,pos,r);ranks[r]=ranks.get(r,0)+1
 out.append({'p':p,'status':'PASS','intrinsic_quotient_genus':V.nrows(),'relative_rank':21,'cusp_patterns':sum(ranks.values()),'operator':'(diamond(root)-1)(T3-diamond3-3)'});print(out[-1],flush=True)
(W/'relative_cusps_intrinsic_verified.json').write_text(json.dumps({'status':'PASS','results':out},indent=2)+'\n')
