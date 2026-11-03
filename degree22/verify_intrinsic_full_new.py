from pathlib import Path
import json,time,re
from sage.all import GF,matrix
from intrinsic_model import Model,compare,results
W=Path(__file__).resolve().parent
while not all((W/f'{name}_data.m').exists()for name in['full_cusps61_sharp','full_cusps89','full_cusps97_sharp']):time.sleep(10)
for p in[61,89,97]:
 M=Model(p)
 if p==89:compare(M,'full_cusps89',M.operators(M.root,[2,3,5,7]));continue
 ev=(W/('strange_eigenvalues61_data.m'if p==61 else'strange_eigenvalues_data.m')).read_text();AA=[]
 for n in[2,3,5,7]:
  T=M.hecke(n)
  if T is None:continue
  cc=[int(x)for x in re.search(r'StrangeHeckeEigenvalues\[<'+str(p)+','+str(n)+r'>\]:=\[([^\]]*)\]',ev)[1].split(',')];beta=T-sum((GF(2)(a)*M.D**j for j,a in enumerate(cc)),matrix(GF(2),M.g,M.g))
  for q in[3,5,7]:
   U=M.hecke(q)
   if U is not None:AA.append((M.D-M.I)*beta*(U-M.D**M.log(q)-GF(2)(q)*M.I))
 compare(M,f'full_cusps{p}_sharp',AA)
(W/'intrinsic_full_new_verified.json').write_text(json.dumps({'status':'PASS','results':results},indent=2)+'\n');print('S22_INTRINSIC_FULL_NEW_COMPLETE',flush=True)
