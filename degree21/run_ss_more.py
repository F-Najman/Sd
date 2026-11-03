from pathlib import Path
import sys,subprocess
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W));from unit_arithmetic import lit
for n,ds in [(73,[6]),(109,[9,12]),(127,[14])]:
 H=W/f'full{n}';S=W/f'ss{n}';rs=lit((W/f'sources{n}.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ids=[i+1 for i,z in enumerate(rs)if not z[6]and z[0]in ds];a,b=min(ids),max(ids)
 with(H/'ss_export.log').open('w')as f:r=subprocess.run(['magma','-b',f'Start:={a}',f'End:={b}',str(H/'stage2_ss.m')],stdout=f,stderr=subprocess.STDOUT)
 s=(H/'ss_export.log').read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s
 (S/'hecke_jets.m').write_bytes((H/f'ss_jets_{a}.m').read_bytes())
 with(S/'sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'ss_sieve.py'),str(n)],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0;print('S21_SS_OBSTRUCTION_BATCH_COMPLETE',n,flush=True)
