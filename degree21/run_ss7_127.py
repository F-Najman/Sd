from pathlib import Path
import subprocess
W=Path(__file__).resolve().parent;H=W/'full127';S=W/'ss7_127'
with(H/'ss7_export.log').open('w')as f:r=subprocess.run(['magma','-b','Start:=23','End:=24',str(H/'stage2_ss7.m')],stdout=f,stderr=subprocess.STDOUT)
s=(H/'ss7_export.log').read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s
(S/'hecke_jets.m').write_bytes((H/'ss7_jets_23.m').read_bytes())
with(S/'sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'ss7_sieve.py'),'127'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0;print('S21_SS7_127_COMPLETE',flush=True)
