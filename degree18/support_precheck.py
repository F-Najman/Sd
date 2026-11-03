from pathlib import Path
import sys,json,math
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131];ledger=[]
def classify(n,s,c):
 o=[d for t,d in s if t=='O'];a=[(t,d)for t,d in s if t!='O']
 if not s:return 'cuspidal formal immersion, relative at103 and131'
 if len(o)==2:
  assert not a
  if n==131:return 'new ordinary pairs of totals16,17,18, with cusp complements'
  if n==113:return 'inherited pair obstruction, with the order8 stabilizer argument for the exceptional repeated O8 case'
  return 'ordinary pair: inherited if total<=17, new if total=18;127 exceptional9+9 descends to quadratic quotient'
 if len(o)==1:
  d=o[0]
  if not a:return 'ordinary obstruction;113 exceptional8 by order8;127 exceptional9 by quadratic quotient'
  assert len(a)==1
  t,e=a[0]
  allowed={(73,'SS',6,x)for x in[7,10,11,12]}|{(73,'NC',9,7),(113,'SS',7,8),(113,'SS',7,11)}|{(127,'NC',7,x)for x in[8,9,10,11]}
  assert(n,t,e,d)in allowed,(n,s,c)
  if n==113 and d==8:return 'involution, parity at supersingular fixed points, and CM exclusion'
  if n==127 and d==9:return 'two-quotient relative immersion with two fixed cusps'
  return 'mixed Hecke obstruction: new73O12,113O11,127O11; otherwise inherited'
 assert not o
 if n==53:assert s==[('SS',13)];return 'relative order13 pullback, five fixed cusps'
 if n==61:assert s==[('SS',15)];return 'relative order5 pullback of cubic divisor, three fixed cusps'
 if n==73:
  total=sum(d for t,d in s)
  if s==[('SS',6)]:return 'relative fixed supersingular locus plus twelve cusp directions'
  if s==[('NC',9)]:return 'relative order9 pullback plus nine cusp directions; quadratic quotient if residual fixed divisor=0'
  assert total in[12,15,18]
  return 'actual rational2-torsion control;order9 invariance;noninvariant cusp complement or quadratic quotient and CM exclusions'
 if n==89:assert s==[('NC',11)];return 'order11 invariance via odd-degree anti-Jacobian annihilator'
 if n==97:assert s==[('SS',16)];return 'order4 invariance and CM1728 exclusion'
 if n==109:assert sum(d for t,d in s)in[9,12,18];return 'order18 invariance, rational point on quotient maps toX0(109), CM branch exclusions'
 if n==113:assert sum(d for t,d in s)in[7,14];return 'order14 invariance;orbit lengths7 or14 do not divide18'
 if n==127:assert sum(d for t,d in s)in[7,14];return 'order7 invariance;7 does not divide18'
 raise AssertionError((n,s,c))
for n in ns:
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');O=sorted({r[0]for r in rs if r[6]});SS=sorted({r[0]for r in rs if not r[6]});nc=next(k for k in range(1,n)if pow(2,k,n)in[1,n-1]);types=[('O',d)for d in O]+[('SS',d)for d in SS]+([('NC',nc)]if nc<=18 else[])
 def walk(i,left,s):
  reason=classify(n,s,left);ledger.append({'p':n,'support':s,'rational_cusp_complement':left,'planned_or_verified_argument':reason})
  for j in range(i,len(types)):
   if types[j][1]<=left:walk(j,left-types[j][1],s+[types[j]])
 walk(0,18,[])
out={'status':'ALL_SUPPORT_TYPES_HAVE_AN_IDENTIFIED_ARGUMENT','cases':ledger};(W/'support_precheck.json').write_text(json.dumps(out,indent=2)+'\n');print('S18_SUPPORT_PRECHECK',len(ledger),'types')
