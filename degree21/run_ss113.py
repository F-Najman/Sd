from pathlib import Path
import subprocess
W=Path(__file__).resolve().parent;H=W/'full113';S=W/'ss113'
with(H/'ss_export.log').open('w')as f:r=subprocess.run(['magma','-b','Start:=1','End:=1',str(H/'stage2_ss.m')],stdout=f,stderr=subprocess.STDOUT)
s=(H/'ss_export.log').read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s
(S/'hecke_jets.m').write_bytes((H/'ss_jets_1.m').read_bytes())
with(S/'sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'ss_sieve.py'),'113'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
print('S21_SS113_OBSTRUCTION_COMPLETE',flush=True)
