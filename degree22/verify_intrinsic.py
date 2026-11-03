from pathlib import Path
import json,re,time
from sage.all import GF,matrix
from intrinsic_model import Model,compare,results,start
W=Path(__file__).resolve().parent
for p in [61,73,97,101,109,113,127]:
 M=Model(p)
 if p==53:
  A=M.operators(10,[2,3,5,7]);compare(M,'relative53',A,13,12);compare(M,'full_cusps53',A)
 elif p==61:
  A=M.operators(3,[2,3,5,7]);compare(M,'relative61',A,15,12);compare(M,'relative61_ss20',A,20,16)
 elif p==73:
  A=M.operators(2,[2,3,5,7]);compare(M,'relative73',A,6,6);compare(M,'relative73_nc',A,9,8,nc=True)
 elif p in[97,101]:
  ev=(W/'strange_eigenvalues_data.m').read_text();A=[];kh=16 if p==97 else 1
  for n in[2,3,5,7]:
   T=M.hecke(n)
   if T is None:continue
   cc=[int(x)for x in re.search(r'StrangeHeckeEigenvalues\[<'+str(p)+','+str(n)+r'>\]:=\[([^\]]*)\]',ev)[1].split(',')];beta=T-sum((GF(2)(a)*M.D**j for j,a in enumerate(cc)),matrix(GF(2),M.g,M.g))
   for q in[3,5,7]:
    U=M.hecke(q)
    if U is not None:A.append((M.D**kh-M.I)*beta*(U-M.D**M.log(q)-GF(2)(q)*M.I))
  compare(M,'relative97_sharp'if p==97 else'full_cusps101_sharp',A,16 if p==97 else 0,16 if p==97 else 0)
 elif p==109:compare(M,'relative109',M.operators(93,[2,3,5,7]),9,8)
 elif p==113:compare(M,'relative113_ordinary',M.operators(40,[2,3,5]),8,7,True,7)
 else:
  # The combined relative case is checked in verify_quotients.py.
  pass
(W/'intrinsic_relative_independent.json').write_text(json.dumps({'status':'PASS','degree':22,'results':results},indent=2)+'\n')
