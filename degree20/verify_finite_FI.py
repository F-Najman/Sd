from pathlib import Path
import json,math
from sage.all import QQ,matrix
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;B=W.parents[1];data=lit((W/'finite_FI_data.m').read_text(),'FiniteFIData');out=[]
for p,ind,n,poly,g,ww,uu in data:
 def mat(a):return matrix(QQ,g,g,[QQ(x)/QQ(y)for x,y in a])
 A,U=mat(ww),mat(uu);r=A.rank();assert A.stack(U).rank()==r;out.append({'p':p,'index':ind,'hecke_index':n,'J0_genus':g,'winding_rank':r,'polynomial_image_in_winding_space':True})
orders={};ps=None
for line in(B/'work/audit11/derickx_stoll_table2.txt').read_text().splitlines():
 if ' p&'in line:ps=[int(v)for v in line.split(' p&',1)[1].split('\\\\',1)[0].split('&')if v]
 elif '\\ord(\\chi)&'in line:
  a=[[int(t)for t in v.split(',')]for v in line.split('\\ord(\\chi)&',1)[1].split('\\\\',1)[0].split('&')if v];assert len(a)==len(ps);orders.update(zip(ps,a))
active={(67,11,2),(67,11,3),(67,11,5),(73,12,2),(73,12,3),(73,12,5),(79,39,2),(83,41,2),(89,11,2),(97,8,5),(103,17,2)}
assert active<={(r['p'],r['index'],r['hecke_index'])for r in out}
for p,i,n in active:assert all(i%c!=0 for c in orders.get(p,[]))
(W/'finite_FI_verified.json').write_text(json.dumps({'status':'PASS','exact_J0_matrix_checks':out,'active_quotient_polynomials':len(active),'all_nontrivial_positive_rank_characters_absent_from_active_quotients':True,'method':'correct dual-period T2 winding action; exact polynomial-image containment; proved strange-character table'},indent=2)+'\n');print('S20_FINITE_FI_INDEPENDENT_PASS',len(active),'active quotient polynomials',flush=True)
