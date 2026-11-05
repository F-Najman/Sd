"""Independent dense-operator fixtures, including actual eight-lane execution."""
from pathlib import Path
import subprocess,json,ast,re,hashlib
O=Path(__file__).resolve().parent;W=O.parent;D=O/'simd_fixtures';D.mkdir(exist_ok=True);results=[]
for kind in ['balanced','unbalanced','anchored']:
 for q in [101,65537,6297589,16777213,536870909,1073741789,4294967291]:
  nr=60;edges=[(3*b+i,3*b+(i+1)%3)for b in range(20)for i in range(3)];ns=len(edges);A=[[0]*ns for _ in range(nr)]
  for j,(r,s)in enumerate(edges):A[r][j]=1;A[s][j]=q-1
  for b in range(0,20,2):
   if kind=='unbalanced':A[edges[3*b+2][1]][3*b+2]=2
   if kind=='anchored':A[edges[3*b+2][1]][3*b+2]=0
  R=[[(int(i==j)+sum(A[r][i]*A[r][j]for r in range(nr)))%q for j in range(ns)]for i in range(ns)];nnz=sum(a!=0 for row in R for a in row);stem=D/f'{kind}_{q}';graph=stem.with_suffix('.graph');prep=stem.with_suffix('.prepared');rank=stem.with_suffix('.rank.json');vg=stem.with_suffix('.graph_verified.json');plan=stem.with_suffix('.plan');vf=stem.with_suffix('.free_verified.json');sf=stem.with_suffix('.sequence.m')
  with graph.open('w')as f:
   f.write(f'{q} 53 13 {ns} {nr} {nnz} 2 0 1\n')
   for row in A+R:
    aa=[(j,a)for j,a in enumerate(row)if a];f.write(str(len(aa))+' '+' '.join(f'{j} {a}'for j,a in aa)+'\n')
  def run(cmd):
   cp=subprocess.run(list(map(str,cmd)),capture_output=True,text=True);assert cp.returncode==0,(cmd,cp.stdout,cp.stderr)
  run([O/'prepare_graph',graph,prep,rank]);run(['python3',O/'verify_graph.py',graph,prep,rank,vg]);run(['python3',O/'prepare_free.py',graph,prep,rank,plan]);run(['python3',O/'verify_free.py',graph,prep,rank,vg,plan,vf]);run([W/'krylov_simd',plan,sf])
  lines=prep.read_text().splitlines();qq,nd,k,nn=map(int,lines[0].split());v=list(map(int,lines[1].split()));u=list(map(int,lines[2].split()));expected=[]
  for st in range(2*k):expected.append(sum(a*b for a,b in zip(v,u))%q);v=[sum(v[i]*R[i][j]for i in range(ns))%q for j in range(ns)]
  actual=ast.literal_eval(re.search(r'sequence:=(.*?);',sf.read_text(),re.S)[1]);assert actual==expected
  header=list(map(int,plan.read_text().splitlines()[0].split()));assert header[6]>=8
  results.append({'kind':kind,'q':q,'terms':2*k,'free_dimension':header[6],'all_terms_equal_to_naive_full_operator':True});print('S22_SIMD_FIXTURE_PASS',kind,q,flush=True)
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
(O/'simd_fixtures_verified.json').write_text(json.dumps({'status':'PASS','not_modular_symbols_proof_premises':True,'tests':results,'source_sha256':sha(W/'krylov_simd.cpp'),'binary_sha256':sha(W/'krylov_simd')},indent=2)+'\n')
