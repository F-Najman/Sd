from pathlib import Path
import json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,163];ledger=[]
def classify(n,s,c):
 o=[d for t,d in s if t=='O'];a=[(t,d)for t,d in s if t!='O']
 if not s:return 'cuspidal formal immersion; relative fibers at103,131; full diamond repair at53'
 if len(o)==2:
  assert not a
  if n==137:return 'new low pairs with totals16,17,18'
  return 'inherited pairs of total<=18 or new total19; exceptional113 repeatedO8 and127 repeatedO9 excluded by stabilizers'
 if len(o)==1:
  d=o[0]
  if not a:return 'ordinary nonprincipal divisor obstruction; exceptional113O8 and127O9 by stabilizers'
  if len(a)>1:
   assert n==73 and d==7 and a==[('SS',6),('SS',6)],(n,s,c)
   return 'inherited mixed O7 obstruction; order9 diamond fixes both SS6 divisors'
  t,e=a[0];allowed={(73,'SS',6,x)for x in[7,10,11,12,13]}|{(73,'NC',9,7),(73,'NC',9,10),(113,'SS',7,8)}|{(113,'SS',7,x)for x in[11,12]}|{(127,'NC',7,x)for x in[8,9,10,11,12]}
  assert(n,t,e,d)in allowed,(n,s,c)
  if n==113 and d==8:return 'order2 stabilizer and odd degree exclude free orbits; CM1728 excluded'
  if n==127 and d==9:return 'two quotient relative immersion with three fixed cusps'
  return 'mixed Hecke obstruction, new73O13,113O12,127O12; lower totals inherited'
 assert not o
 if n==53:assert s==[('SS',13)];return 'relative H13 pullback plus6 fixed cusps'
 if n==61:assert s==[('SS',15)];return 'relative H5 pullback of cubic divisor plus4 fixed cusps'
 if n==73:
  total=sum(d for t,d in s)
  if s==[('SS',6)]:return 'relative fixed SS divisor plus13 cusps, relation-space certificate'
  if s==[('NC',9)]:return 'relative H9 pullback plus10 cusps, relation-space certificate'
  assert total in[12,15,18]
  return 'rational2-torsion control, H9 invariance, orbit lengths3 or9 do not divide19'
 if n==89:assert s==[('NC',11)];return 'odd anti-Jacobian degree, H11 invariance, orbits do not divide19'
 if n==97:assert s==[('SS',16)];return 'H4 invariance, orbit lengths2 or4 do not divide19'
 if n==109:assert sum(d for t,d in s)in[9,12,18];return 'H18 invariance, orbit lengths6,9,18 do not divide19'
 if n==113:assert sum(d for t,d in s)in[7,14];return 'H14 invariance, orbit lengths7,14 do not divide19'
 if n==127:assert sum(d for t,d in s)in[7,14];return 'H7 invariance, orbit length7 does not divide19'
 if n==137:assert s==[('SS',17)];return 'H34 invariance, orbit lengths17,34 do not divide19'
 raise AssertionError((n,s,c))
for n in ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');O=sorted({r[0]for r in rs if r[6]});SS=sorted({r[0]for r in rs if not r[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',d)for d in O]+[('SS',d)for d in SS]+([('NC',nc)]if nc<=19 else[])
 def walk(i,left,s):
  reason=classify(n,s,left);ledger.append({'p':n,'support':s,'cusp_complement':left,'argument':reason})
  for j in range(i,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],s+[types[j]])
 walk(0,19,[])
(W/'support_precheck.json').write_text(json.dumps({'status':'ALL_SUPPORT_TYPES_HAVE_AN_IDENTIFIED_ARGUMENT','degree':19,'cases':ledger},indent=2)+'\n');print('S19_SUPPORT_PRECHECK',len(ledger),flush=True)
