"""Every possible degree22 special support, with explicit even-degree arguments."""
from pathlib import Path
import json
from fractions import Fraction
W=Path(__file__).resolve().parent;a=json.loads((W/'support_inventory.json').read_text());out=[]
def strict(p,c,k):assert k*(22+c)<Fraction(325*(p*p-1),65536),(p,c,k)
for lev in a['levels']:
 n=lev['p']
 for r in lev['cases']:
  s=r['support'];c=r['cusp_complement'];oo=[d for t,d in s if t=='O'];other=[(t,d)for t,d in s if t!='O'];total=22-c
  if not s:
   reason='anti_H27 cusp immersion, minimum relation degree27>22'if n==163 else('odd quotient cusp immersion plus intrinsic relative ranks21'if n in[103,131]else'absolute cusp immersion')
  elif len(oo)==3:
   assert not other and (oo==[7,7,7]and n in[59,61,71,73]or oo==[7,7,8]and n in[59,61,71]);reason='inherited ordinary7 triples'if total==21 else'new degree22 ordinary triples, complete diamond orbit enumeration'
  elif len(oo)==2:
   if other:assert n==73 and oo==[7,7]and other==[('SS',6)];reason='inherited ordinary pair delta2 obstruction; SS block fixed as divisor'
   elif n==163:assert oo==[10,10];reason='new level163 ordinary pair obstruction, all relative positions'
   elif n==113 and oo==[8,8]:strict(n,c,2);assert all(22%v for v in[8,4]);reason='inherited ordinary-pair obstructions except the H8 pair; H8 invariance gives orbit lengths8 or4, neither dividing22'
   elif n==127 and oo==[9,9]:strict(n,c,2);assert all(22%v for v in[9,3]);reason='H9 invariance; geometric orbit lengths9 or3 do not divide22'
   else:reason='new degree22 ordinary pair obstruction'if total==22 else'inherited ordinary pair obstruction'
  elif oo:
   assert len(oo)==1;d=oo[0]
   if not other:
    if n==163:reason='new ordinary principal-divisor obstruction on fresh genus1027 model'
    elif n==61 and d==20:reason='H5 ordinary pullback relative immersion plus fixed cusp remainder2'
    elif n==113 and d==8:reason='H8 ordinary pullback relative immersion plus fixed cusp remainder'
    elif n==127 and d==9:strict(n,c,2);reason='H9 invariance, no geometric orbit length divides22'
    elif n==137 and d==17:strict(n,c,2);reason='H17 invariance,17 does not divide22'
    else:reason='new degree22 ordinary obstruction'if d==22 else'inherited ordinary obstruction'
   elif n==61:
    assert d==7 and other==[('SS',15)]and c==0;reason='inherited ordinary7 (D6-1)A3 obstruction; SS15 fixed by H5 as divisor'
   elif n==73:
    assert other in[[('SS',6)],[('NC',9)],[('SS',6),('SS',6)],[('SS',6),('NC',9)]]
    if other==[('SS',6)]:assert d in[7,10,11,12,13,14,15,16]
    elif other==[('NC',9)]:assert d in[7,10,11,12,13]
    elif other==[('SS',6),('SS',6)]:assert d in[7,10]
    else:assert d==7
    reason='delta2 ordinary obstruction; every SS6 andNC9 block is fixed as divisor'
   elif n==89:assert other==[('NC',11)]and d in[9,10,11];reason='delta2 ordinary obstruction, NC11 term fixed'
   elif n==109:assert other==[('SS',9)]and d in[11,12,13];reason='delta2 ordinary obstruction, SS9 term fixed'
   elif n==113:
    if d==8:
     if other==[('SS',7)]:strict(n,c,2);assert c==7;reason='forced H2 invariance of rational cusp complement of odd degree7, impossible'
     elif other==[('SS',7),('SS',7)]:assert c==0;reason='generic O8 orbit: all10 combined A3 pair obstructions; exceptional H8 orbit: all3 SS-pair obstructions'
     else:assert other==[('NC',14)]and c==0;reason='generic O8 orbit: all4 combined NC14 A3 obstructions; exceptional H8 orbit: relative immersion rank21 with fixed cusp14'
    else:assert other==[('SS',7)]and d in[11,12,13,14,15];reason='delta2 ordinary obstruction; SS7 term fixed'
   else:
    assert n==127 and (other==[('NC',7)]and d in[8,9,10,11,12,13,14,15]or other==[('NC',7),('NC',7)]and d==8 or other==[('SS',14)]and d==8)
    reason='two-pullback relative immersion, rank20 and fixed cusp6'if d==9 else'delta2 ordinary obstruction; all NC7 andSS14 blocks fixed'
  elif n==61:assert s in[[['SS',15]],[['SS',20]]];reason='H5 pullback relative immersion, nonzero cusp remainder modulo5'
  elif n==73:
   if total==6:reason='tame H3-fixed lift plus relative cusp fibers, fixed remainder'
   elif total==9:reason='H9 pullback relative immersion, fixed cusp remainder'
   elif total==12:assert s==[['SS',6],['SS',6]];reason='double tame H3-fixed lift, all10 positions and cusp10 profiles'
   elif total==15:reason='SS6 plusNC9 relative immersion, all16 positions and cusp7 profiles'
   else:assert total in[18,21];strict(n,c,1);assert all(22%v for v in[9,3]);reason='H9 invariance using actual rational2-torsion control; orbit lengths9 or3 do not divide22'
  elif n==89:assert s in[[['NC',11]],[['NC',11],['NC',11]],[['SS',22]]];reason='new H11 quotient Sym2 argument, all cusp andSS22 disks resolved'
  elif n==97:assert s==[['SS',16]];reason='sharper relative maps; tame H3-fixed lifts and cusp6, mixed stabilizer excludes full cusp fibers'
  elif n==109:
   if total==9:reason='H9 pullback relative immersion and fixed cusp remainder4'
   elif total==12:reason='inherited direct SS12 T3 obstruction'
   else:assert total in[18,21];strict(n,c,2);assert all(22%v for v in[18,9,6]);reason='H18 invariance, geometric orbit lengths18,9,6 do not divide22'
  elif n==113:
   if total==7:reason='inherited direct SS7 T3 obstruction'
   else:assert total in[14,21];strict(n,c,2);assert all(22%v for v in[14,7]);reason='H14 invariance, orbit lengths14 or7 do not divide22'
  elif n==127:
   assert all(t in['SS','NC']for t,d in s);strict(n,c,2);assert 22%7;reason='H7 invariance; action free and7 does not divide22'
  else:assert n==137 and s==[['SS',17]];strict(n,c,2);assert all(22%v for v in[34,17]);reason='H34 invariance, orbit lengths34 or17 do not divide22'
  out.append({'p':n,**r,'argument':reason})
assert len(out)==a['support_types']==514
z={'status':'STRUCTURAL_COVERAGE_COMPLETE','degree':22,'support_types':514,'odd_degree_real_diamond_lemma_used':False,'records':out};(W/'support_coverage_plan.json').write_text(json.dumps(z,indent=2)+'\n');print('S22_ALL514_SUPPORT_TYPES_CLASSIFIED',flush=True)
