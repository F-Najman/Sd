from pathlib import Path
import sys,re,shutil,json
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'work/degree17'
sys.path.insert(0,str(O));from unit_arithmetic import lit
ns=[47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]
for name in ['unit_arithmetic.py','full_sieve.py','compress_FI.py','finite_FI_polynomials.m','relation_check','check_prefixes','relative_prefixes']:
 shutil.copyfile(O/name,W/name)
for name in ['check_prefixes','relation_check','relative_prefixes']:(W/name).chmod(0o755)
t=(O/'full113/stage2.m').read_text();head=t[:t.index('function XYKey')]
head=head.replace('128 div d','144 div d')
body=t[t.index(' E,P:=SimplifyPoint(E,P);sr,sd:=RecordPoint(E,P);d:=rec[1];'):t.index('assert #used eq #OldRecords;')]
jobs=[]
for n in ns:
 H=W/f'full{n}';H.mkdir(exist_ok=True);shutil.copyfile(O/f'full{n}/units_data.m',H/'units_data.m')
 s=head.replace(str(O/'full113/units_data.m'),str(H/'units_data.m'))
 s+=f'load "{W}/sources{n}.m";assert AuditN eq N;\nSourceRecords:=[**];SourceHeckeRecords:=[**];SourceMetadata:=[**];\nfor si in[StringToInteger(Start)..Min(StringToInteger(End),#AuditSources)]do\n rec:=AuditSources[si];if not rec[7]or rec[1]ne 18 then continue;end if;\n PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];assert N*P eq E!0 and P ne E!0;\n'
 s+=body.replace('S17_','S18_')
 s+=f'PrintFile("{H}/hecke_jets_" cat Start cat ".m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",SourceMetadata,SourceRecords,SourceHeckeRecords):Overwrite:=true);\nprintf "AUDIT_ACTUAL_HECKE_JETS_COMPLETE N=%o sources=%o elapsed=%o\\n",N,#SourceRecords,Cputime(tt);quit;\n'
 (H/'stage2_chunk.m').write_text(s)
 rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ids=[i+1 for i,r in enumerate(rs)if r[6]and r[0]==18]
 for k in range(0,len(ids),8):jobs.append({'N':n,'start':ids[k],'end':ids[min(k+7,len(ids)-1)]})
 print(n,'new ordinary sources',len(ids))
(W/'new_ordinary_jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
# Build the new level 131 with a conservative q precision and explicitly computed pole degrees.
H=W/'full131';H.mkdir(exist_ok=True)
s=(B/'work/degree14/full127/build_frozen.m').read_text().replace('N:=127;g:=610;QPrec:=2888;TatePrec:=3488;','N:=131;g:=651;QPrec:=3300;TatePrec:=3900;').replace('Md^63','Md^65').replace(str(B/'work/degree14/full127/units_data.m'),str(H/'units_data.m'))
s=s.replace('low:=Min(0,Min(Valuation(xu),Valuation(yu))+1)','low:=Min(0,Min(Valuation(xu),Valuation(yu))+1)')
pos=s.index('ux2,uy2:=TateUnits(DiamondRoot);')
s=s[:pos]+'''vv:=[<Valuation(a),Valuation(b)> where a,b:=TateUnits(k):k in[1..(N-1)div 2]];
px:=&+[Max(0,-v[1]):v in vv];py:=&+[Max(0,-v[2]):v in vv];
assert RelPrec-1 gt 2*g-2+Max(px,py);
printf "S18_MODULAR_UNIT_POLE_DEGREES p=%o x=%o y=%o valuations=%o\\n",N,px,py,vv;
'''+s[pos:]
s=s.replace('(N-1)div 2,211,221,','(N-1)div 2,px,py,').replace('2*g-2+221','2*g-2+Max(px,py)').replace('[211,221]','[px,py]')
(H/'build.m').write_text(s)
