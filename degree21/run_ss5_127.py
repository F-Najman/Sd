from pathlib import Path
import subprocess
W=Path(__file__).resolve().parent;H=W/'full127';S=W/'ss5_127'
with(H/'ss5_export.log').open('w')as f:r=subprocess.run(['magma','-b','Start:=20','End:=25',str(H/'stage2_ss5.m')],stdout=f,stderr=subprocess.STDOUT)
s=(H/'ss5_export.log').read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s
(S/'hecke_jets.m').write_bytes((H/'ss5_jets_20.m').read_bytes())
with(S/'sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'ss5_sieve.py'),'127'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0;print('S21_SS5_127_COMPLETE',flush=True)
