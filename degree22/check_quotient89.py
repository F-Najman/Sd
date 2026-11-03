from pathlib import Path
import json,time,itertools,gzip,hashlib,sys
from sage.all import GF,matrix
from unit_arithmetic import lit,matbits,bits,xorrows,decode_record,transform
W=Path(__file__).resolve().parent
while not(W/'ss89/hecke_jets.m').exists()or not(W/'frobenius89_verified.json').exists():time.sleep(10)
s=(W/'quotient89_cusps_data.m').read_text();V=lit(s,'Q89InvariantBasis');rc=lit(s,'Q89CanonicalRC');nc=lit(s,'Q89CanonicalNC');VB=[bits(r)for r in V];assert len(V)==27 and len(rc)==len(nc)==4
text=(W/'full89/units_data.m').read_text();D=matbits(text,'DiamondMatrix');Q=matbits(text,'qcoeffs');Db=[1<<i for i in range(287)];Dp=[]
for k in range(4):Dp.append(Db);Db=[xorrows(r,D)for r in Db]
assert all(xorrows(r,Db)==r for r in VB)
VM=matrix(GF(2),V);DM=matrix(GF(2),[[r>>j&1 for j in range(287)]for r in D]);assert VM.rank()==27 and(DM**4-matrix.identity(GF(2),287)).left_kernel().dimension()==27
# Independently certify that the complete invariant canonical system is nonhyperelliptic.
YQ=[xorrows(r,Q)for r in VB];products=[]
def pmul(a,b):
 out=0
 while b:
  k=(b&-b).bit_length()-1;out^=a<<k;b&=b-1
 return out
for i in range(27):
 for j in range(i,27):products.append(pmul(YQ[i],YQ[j]))
P=max(v.bit_length()for v in YQ);mask=(1<<P)-1;products=[v&mask for v in products]
A=matrix(GF(2),[[v>>j&1 for j in range(P)]for v in products]);assert A.rank()==78
# The independent Frobenius traces account for every point over F2,F4,F8,F16.
assert json.loads((W/'frobenius89_verified.json').read_text())['status']=='PASS'
tr=[0]*4
for n,pol,d,AA,c,cs in lit((W/'frobenius89_data.m').read_text(),'Frob89Data'):
 if n in[1,2,4]:tr=[a+int(b)for a,b in zip(tr,cs[:4])]
assert[2**f+1-tr[f-1]for f in range(1,5)]==[8,38,8,38]
records=lit((W/'ss89/hecke_jets.m').read_text(),'SourceRecords');meta=lit((W/'ss89/hecke_jets.m').read_text(),'SourceMetadata');ss=[];keys=set()
for rec,mm in zip(records,meta):
 v=decode_record(rec);F=v['F'];assert F.d==22
 zeta=next(z for a in range(2,30)if (z:=F.pow(a,((1<<22)-1)//3))not in[0,1]);assert F.pow(zeta,3)==1;enc={0:0,1:1,zeta:2,zeta^1:3}
 for k in range(mm[2]):
  zz=transform(F,v['jets'],Dp[k]);vv=transform(F,zz,VB);j=next(i for i,row in enumerate(vv)if row[1]);scale=F.inv(vv[j][1]);values=[enc[row[0]]for row in vv];der=[enc[F.mul(row[1],scale)]for row in vv]
  square=lambda x:0 if x==0 else(1 if x==1 else(3 if x==2 else 2));key=min(tuple(values),tuple(square(a)for a in values));assert key not in keys;keys.add(key);ss.append([[values[i],der[i]]for i in range(27)])
assert len(ss)==15
cusps=rc+nc;assert len({tuple(row[0]for row in J)for J in cusps})==8
mats=[]
def cols_rc(i,m):return[sum(cusps[i][a][j]<<a for a in range(27))for j in range(m)]
def cols_ss(i,m):return[sum(((ss[i][a][j]>>b)&1)<<a for a in range(27))for j in range(m)for b in[0,1]]
def check(label,cols):
 assert len(cols)==4;M=matrix(GF(2),[[v>>i&1 for i in range(27)]for v in cols]);assert M.rank()==4,label;mats.append({'case':label,'columns':list(map(hex,cols))})
for cc in itertools.combinations_with_replacement(range(8),4):
 cols=[]
 for c in sorted(set(cc)):cols+=cols_rc(c,cc.count(c))
 check(['four_cusps',list(cc)],cols)
for a in range(15):
 for cc in itertools.combinations_with_replacement(range(8),2):
  cols=cols_ss(a,1)
  for c in sorted(set(cc)):cols+=cols_rc(c,cc.count(c))
  check(['SS2_plus_two_cusps',a,list(cc)],cols)
for a,b in itertools.combinations_with_replacement(range(15),2):check(['two_SS2',a,b],cols_ss(a,2)if a==b else cols_ss(a,1)+cols_ss(b,1))
assert len(mats)==990
with gzip.open(W/'quotient89_gonality_matrices.json.gz','wt')as f:json.dump(mats,f)
# The actual finite-image maps kill all cusps; check every Sym2 cusp disk.
cc=lit(s,'Q89RC')+lit(s,'Q89NC');cusp2=[]
for a,b in itertools.combinations_with_replacement(range(8),2):
 cols=[sum(cc[a][i][j]<<i for i in range(len(cc[a])))for j in range(2)]if a==b else[sum(cc[k][i][0]<<i for i in range(len(cc[k])))for k in[a,b]];M=matrix(GF(2),[[v>>i&1 for i in range(len(cc[0]))]for v in cols]);assert M.rank()==2,(a,b);cusp2.append([a,b])
out={'status':'PASS','degree':22,'quotient':'X1(89)/H11','genus':27,'nonhyperelliptic_canonical_product_rank':78,'F2_to_F16_point_counts':[8,38,8,38],'complete_points_degree_at_most4':{'rational_cusps':8,'supersingular_degree2':15,'other':0},'effective_divisors_degree4_checked':990,'gonality_F2_lower_bound':5,'gonality_Q_lower_bound':5,'absolute_formal_immersion_cusp_pairs':36,'matrix_archive_sha256':hashlib.sha256((W/'quotient89_gonality_matrices.json.gz').read_bytes()).hexdigest()};(W/'quotient89_verified.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_QUOTIENT89_GONALITY_AND_CUSP_DISKS_PROVED',out,flush=True)
