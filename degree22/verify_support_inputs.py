"""Independent complete pair/triple orbit counts and source-input coverage."""
from pathlib import Path
import json,math,collections,time
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;P=W.parent/'degree21'
while not(W/'small_sieves_results.json').exists():time.sleep(15)
z=json.loads((W/'small_sieves_results.json').read_text());assert all(v['status']=='PASS'for v in z)
Ns=json.loads((W/'local_levels.json').read_text())['levels'];sets=json.loads((W/'small_jet_jobs.json').read_text())['degree_sets'];out=[]
def src(w,n):return lit((w/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
for n in Ns+[163]:
 r=src(W,n)
 if n!=163:
  old=src(P,n);assert r[:len(old)]==old
 H=W/f'full{n}';md=lit((H/'small_hecke_jets.m').read_text(),'SourceMetadata')
 if n==163:md=[v for v in md if v[1]==10];assert len(md)==2
 else:assert {v[0]for v in md}>={i+1 for i,v in enumerate(r)if v[6]and v[0]in sets[str(n)]}
 assert len({v[0]for v in md})==len(md)
 for v in md:assert (r[v[0]-1][0],r[v[0]-1][5],r[v[0]-1][4])==v[1:]and r[v[0]-1][6]
 tasks=set()
 for i,u in enumerate(md):
  for j in range(i,len(md)):
   v=md[j]
   if u[1]+v[1]!=(20 if n==163 else 22):continue
   for off in range(math.gcd(u[2],v[2])):
    if i==j and off>u[2]//2:continue
    tasks.add((u[0],v[0],off))
 a=json.loads((H/'pair_sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions'];pairs=[v for v in a['results']if not isinstance(v['source'][0],list)];triples=[v for v in a['results']if isinstance(v['source'][0],list)];assert{tuple(v['source'])for v in pairs}==tasks and len(pairs)==len(tasks)
 m=(n-1)//2;orb={v[0]:v[2]for v in md if v[1]in[7,8]};degs={v[0]:v[1]for v in md};seen=set()
 for rec in triples:
  key=tuple(tuple(v)for v in rec['source']);assert len(key)==3 and sorted(degs[v[0]]for v in key)==[7,7,8]and all(si in orb and 0<=j<orb[si]for si,j in key)
  first=min(si for si,j in key);normal=[]
  for si,j in key:
   if si==first:
    for t in range(-j,m-j,orb[first]):normal.append(tuple(sorted((sj,(q+t)%orb[sj])for sj,q in key)))
  canonical=min(normal);assert canonical not in seen;seen.add(canonical)
 if n in[59,61,71]:
  fixed=0
  for t in range(m):
   cycles={7:collections.Counter(),8:collections.Counter()}
   for v in md:
    if v[1]in[7,8]:cycles[v[1]][v[2]//math.gcd(t,v[2])]+=math.gcd(t,v[2])
   aa,bb=cycles[7][1],cycles[7][2];cc=cycles[8][1];fixed+=(math.comb(aa+1,2)+bb)*cc
  assert fixed%m==0 and fixed//m==len(triples),(n,fixed//m,len(triples))
 else:assert not triples
 out.append({'p':n,'pair_orbits':len(pairs),'triple_orbits':len(triples),'degree7_7_8_Burnside_complete':n in[59,61,71]});print('S22_SUPPORT_INPUTS_PASS',out[-1],flush=True)
for n,ds in[(73,{13,16}),(89,{11}),(109,{13}),(113,{15}),(127,{15})]:
 a=json.loads((W/f'full{n}/mixed_sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions'];r=src(W,n);assert{v['source']for v in a['results']}=={i+1 for i,v in enumerate(r)if v[6]and v[0]in ds}
# The new61 mixed support reuses the unique ordinary7 orbit obstruction.
a=json.loads((W.parent/'degree17/full61/sieve.json').read_text());assert a['alpha_coefficients']=={'6':1,'0':-1};assert [(v['source'],v['status'])for v in a['results']if v['degree']==7]==[(1,'NONPRINCIPAL')];r=src(W,61);assert sum(v[6]and v[0]==7 for v in r)==1
(W/'support_inputs_verified.json').write_text(json.dumps({'status':'PASS','degree':22,'source_prefixes':17,'pair_and_triple_cases':out,'mixed_new_levels':[73,89,109,113,127],'new61_O7_SS15_ordinary_obstruction_reused':True},indent=2)+'\n');print('S22_SUPPORT_INPUTS_COMPLETE',sum(v['pair_orbits']+v['triple_orbits']for v in out),flush=True)
