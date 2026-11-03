from pathlib import Path
import subprocess
W=Path(__file__).resolve().parent
for n,stem in[(61,'full_cusps61'),(89,'full_cusps89'),(97,'full_cusps97_sharp')]:
 with(W/(stem+'.log')).open('w')as f:r=subprocess.run(['magma','-b',f'P:={n}',str(W/(stem+'.m'))],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0
 with(W/('check_'+stem+'.log')).open('w')as f:r=subprocess.run(['python3',str(W/'check_relative_all.py'),stem],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0;print('S21_FULL_CANONICAL_CUSP_CHECK_FINISHED',n,flush=True)
