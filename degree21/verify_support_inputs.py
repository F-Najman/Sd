"""Independent pair/triple orbit coverage and all inherited source matches."""
from pathlib import Path
import json,math,itertools,collections
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;O=W.parent/'degree20';Ns=json.loads((W/'local_levels.json').read_text())['levels'];out=[]
def src(P,n):return lit((P/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources')
sets=json.loads((W/'small_jet_jobs.json').read_text())['degree_sets']
for n in Ns:
 r=src(W,n);P=O if n!=61 else W.parent/'degree19';old=src(P,n);matches=lit((W/f'inherited{n}.m').read_text(),'InheritedOrbitMatches');bound=20 if n!=61 else 19
 assert sorted(z[0]for z in matches)==[i+1 for i,z in enumerate(r)if z[6]and z[0]<=bound]
 assert sorted(z[1]for z in matches)==[i+1 for i,z in enumerate(old)if z[6]]
 for ni,oi,d,orb,k in matches:
  u,v=r[ni-1],old[oi-1];assert u[0]==v[0]==d and u[5]==v[5]==orb and u[4]==v[4]and 1<=k<=(n-1)//2
 if str(n)not in sets:continue
 H=W/f'full{n}';md=lit((H/'small_hecke_jets.m').read_text(),'SourceMetadata');assert {v[0]for v in md}=={i+1 for i,z in enumerate(r)if z[6]and z[0]in sets[str(n)]};tasks=set()
 for i,u in enumerate(md):
  for j in range(i,len(md)):
   v=md[j]
   if u[1]+v[1]not in([20,21]if n==61 else[21]):continue
   for off in range(math.gcd(u[2],v[2])):
    if i==j and off>u[2]//2:continue
    tasks.add((u[0],v[0],off))
 a=json.loads((H/'pair_sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions'];pairs=[v for v in a['results']if not isinstance(v['source'][0],list)];triples=[v for v in a['results']if isinstance(v['source'][0],list)];assert {tuple(v['source'])for v in pairs}==tasks and len(pairs)==len(tasks)
 m=(n-1)//2;seen=set();orb={v[0]:v[2]for v in md if v[1]==7}
 for rec in triples:
  key=tuple(tuple(v)for v in rec['source']);assert len(key)==3 and key==tuple(sorted(key));assert all(si in orb and 0<=p<orb[si]for si,p in key)
  # Anchor one point of the smallest source at zero. All residual shifts are
  # stabilizers of that source's closed orbit. This is independent of the
  # producer's search over all m simultaneous translates.
  first=key[0][0];normal=[]
  for si,p in key:
   if si==first:
    for shift in range(-p,m-p,orb[first]):normal.append(tuple(sorted((sj,(q+shift)%orb[sj])for sj,q in key)))
  canonical=min(normal);assert canonical not in seen;seen.add(canonical)
 if n in[59,61,67,71,73]:
  fixed=0
  for t in range(m):
   cycles=collections.Counter()
   for length in orb.values():cycles[length//math.gcd(t,length)]+=math.gcd(t,length)
   a1,a2,a3=[cycles[i]for i in[1,2,3]];fixed+=math.comb(a1+2,3)+a1*a2+a3
  assert fixed%m==0 and fixed//m==len(triples)
 else:assert not triples
 out.append({'p':n,'pair_orbits':len(pairs),'triple_orbits':len(triples),'triple_count_independent_Burnside':n in[59,61,67,71,73]})
for n,ds in[(73,{12,15}),(89,{10}),(109,{12}),(113,{14}),(127,{14})]:
 a=json.loads((W/f'full{n}/mixed_sieve.json').read_text());assert a['status']=='PASS'and not a['exceptions'];r=src(W,n);assert {z['source']for z in a['results']}=={i+1 for i,z in enumerate(r)if z[6]and z[0]in ds}
(W/'support_inputs_verified.json').write_text(json.dumps({'status':'PASS','source_matches':len(Ns),'pair_and_triple_cases':out,'mixed_new_levels':[73,89,109,113,127]},indent=2)+'\n');print('S21_SUPPORT_INPUTS_COMPLETE',sum(r['pair_orbits']+r['triple_orbits']for r in out),flush=True)
