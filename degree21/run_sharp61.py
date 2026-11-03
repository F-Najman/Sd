from pathlib import Path
import subprocess
W=Path(__file__).resolve().parent
for stem in['strange_eigenvalues61','verify_sharp61_finite','full_cusps61_sharp']:
 with(W/(stem+('_native.log'if stem=='verify_sharp61_finite'else'.log'))).open('w')as f:r=subprocess.run(['magma','-b',str(W/(stem+'.m'))],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,stem
with(W/'check_full_cusps61_sharp.log').open('w')as f:r=subprocess.run(['python3',str(W/'check_relative_all.py'),'full_cusps61_sharp'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
with(W/'verify_sharp61_finite.log').open('w')as f:r=subprocess.run(['sage',str(W/'verify_sharp61_finite.py')],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
print('S21_SHARP61_FINITE_AND_CUSP_DONE',flush=True)
