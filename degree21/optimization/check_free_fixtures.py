from pathlib import Path
import subprocess,json,ast,re
O=Path(__file__).resolve().parent;W=O.parent;D=O/'free_fixtures';D.mkdir(exist_ok=True);results=[]
for kind,q in [('balanced',101),('unbalanced',4294967291),('anchored',4294967291)]:
 nr=6;edges=[(i,(i+1)%6)for i in range(6)]+[(i,i+3)for i in range(3)];ns=len(edges);A=[[0]*ns for _ in range(nr)]
 for j,(r,s)in enumerate(edges):A[r][j]=1;A[s][j]=q-1
 if kind=='unbalanced':A[edges[-1][1]][ns-1]=2
 if kind=='anchored':A[edges[-1][1]][ns-1]=0
 R=[[(int(i==j)+sum(A[r][i]*A[r][j]for r in range(nr)))%q for j in range(ns)]for i in range(ns)];nnz=sum(a!=0 for row in R for a in row);stem=D/kind;graph=stem.with_suffix('.graph');prep=stem.with_suffix('.prepared');rank=stem.with_suffix('.rank.json');vg=stem.with_suffix('.graph_verified.json');plan=stem.with_suffix('.plan');vf=stem.with_suffix('.free_verified.json');sf=stem.with_suffix('.sequence.m')
 with graph.open('w')as f:
  f.write(f'{q} 53 13 {ns} {nr} {nnz} 2 0 1\n')
  for row in A+R:
   aa=[(j,a)for j,a in enumerate(row)if a];f.write(str(len(aa))+' '+' '.join(f'{j} {a}'for j,a in aa)+'\n')
 def run(cmd):
  cp=subprocess.run(list(map(str,cmd)),capture_output=True,text=True);assert cp.returncode==0,(cmd,cp.stdout,cp.stderr)
 run([O/'prepare_graph',graph,prep,rank]);run(['python3',O/'verify_graph.py',graph,prep,rank,vg]);run(['python3',O/'prepare_free.py',graph,prep,rank,plan]);run(['python3',O/'verify_free.py',graph,prep,rank,vg,plan,vf]);run([W/'krylov_free',plan,sf])
 lines=prep.read_text().splitlines();qq,nd,k,nn=map(int,lines[0].split());v=list(map(int,lines[1].split()));u=list(map(int,lines[2].split()));expected=[]
 for st in range(2*k):expected.append(sum(a*b for a,b in zip(v,u))%q);v=[sum(v[i]*R[i][j]for i in range(ns))%q for j in range(ns)]
 actual=ast.literal_eval(re.search(r'sequence:=(.*?);',sf.read_text(),re.S)[1]);assert actual==expected;cert=json.loads(vf.read_text());results.append({'kind':kind,'q':q,'terms':2*k,'all_terms_equal_to_naive_full_operator':True,'uint128_row_fallback_exercised':not cert['safe_uint64_free_rows'],'uint128_winding_fallback_exercised':not cert['safe_uint64_winding']});print('S21_FREE_FIXTURE_PASS',kind,q,flush=True)
(O/'free_fixtures_verified.json').write_text(json.dumps({'status':'PASS','not_modular_symbols_proof_premises':True,'tests':results},indent=2)+'\n')
