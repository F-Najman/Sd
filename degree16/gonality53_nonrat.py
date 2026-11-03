from pathlib import Path
import sys,json
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import matbits,xorrows,lit,decode_record,transform
s=(W/'full53/units_data.m').read_text();Q=matbits(s,'qcoeffs');D=matbits(s,'DiamondMatrix');g=len(Q);assert g==92
first=[int(v>>1&1)for v in Q];rat=[]
for k in range(26):
 rat.append(sum(v<<i for i,v in enumerate(first)));first=[xorrows(r,first)for r in D]
base={}
def add(bs,x):
 while x:
  j=x.bit_length()-1
  if j in bs:x^=bs[j]
  else:bs[j]=x;return True
 return False
for v in rat:assert add(base,v)
s=(W/'full53/hecke_jets.m').read_text();meta=lit(s,'SourceMetadata');rs=lit(s,'SourceRecords');counts={9:0,10:0}
for md,rec in zip(meta,rs):
 d=md[1]
 if d not in[9,10]:continue
 a=decode_record(rec);F=a['F'];z=a['jets'];assert F.d==d
 for k in range(26):
  cols=[sum(((row[0]>>j)&1)<<i for i,row in enumerate(z))for j in range(d)];bs=base.copy()
  for v in cols:assert add(bs,v),(md,k,'point')
  if d==9:
   # The excess rational condition is the SECOND jet, since C_all
   # already contains each rational cusp once.
   second=[int(v>>2&1)for v in Q]
   for aidx in range(26):
    bb=bs.copy();assert add(bb,sum(v<<i for i,v in enumerate(second))),(md,k,aidx)
    second=[xorrows(r,second)for r in D]
  counts[d]+=1;z=transform(F,z,D)
assert counts[9] and counts[10]
out={'status':'PASS','nonrational_configurations':counts,'rational_cusp_base_rank':26,'gonality_lower_bound':20,'excess_degree':10}
(W/'gonality53_nonrat.json').write_text(json.dumps(out,indent=2)+'\n');print('S16_GONALITY53_NONRATIONAL_PASS',out)
