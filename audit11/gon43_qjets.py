"""Holomorphic differential jets at every rational cusp from exact q-forms."""
from pathlib import Path
import re,ast,json
from sage.all import GF,matrix,identity_matrix
W=Path(__file__).resolve().parent;s=(W/'full43/units_data.m').read_text()
def get(name):
 m=re.search(name+r':=Matrix\(GF\(2\),(\d+),(\d+),(\[.*?\])\);',s,re.S);r,c=map(int,m.group(1,2));return matrix(GF(2),r,c,ast.literal_eval(m[3]))
Q=get('qcoeffs');D=get('DiamondMatrix');assert Q.nrows()==57 and D**21==identity_matrix(GF(2),57)and all(Q[i,0]==0 for i in range(57))
caps=[13]+[5]*20;blocks=[];M=identity_matrix(GF(2),57)
for cap in caps:
 # omega_i = sum_{n>=1} a_i(n) q^(n-1) dq; transports by diamonds.
 blocks.append(M*Q.matrix_from_columns(list(range(1,cap+1))));M=M*D.inverse()
J=blocks[0]
for block in blocks[1:]:J=J.augment(block)
assert J.ncols()==113 and J.rank()==57
(W/'gon43_dual_data.m').write_text('Caps:='+str(caps)+';HolomorphicJetMatrix:=Matrix(GF(2),57,113,'+str([int(x)for x in J.list()])+');\n')
print('AUDIT_GON43_ALL_RATIONAL_CUSP_DIFFERENTIAL_JETS_COMPLETE rank57=true qbasis=true diamond_order21=true')
