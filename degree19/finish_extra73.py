from pathlib import Path
import subprocess
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;H=W/'full73';p=H/'extra_jets_1.m';s=(H/'extra13.log').read_text();assert 'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in s
old=(H/'small_hecke_jets.m').read_text();new=p.read_text();parts=[]
for name in ['SourceMetadata','SourceRecords','SourceHeckeRecords']:
 def inner(s):
  v=s.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');return v[2:-2].strip()
 parts.append(name+':=[*'+','.join(v for v in [inner(old),inner(new)]if v)+'*];')
out='\n'.join(parts)+'\n';assert len(lit(out,'SourceMetadata'))==len(lit(old,'SourceMetadata'))+len(lit(new,'SourceMetadata'));(H/'small_hecke_jets.m').write_text(out)
with(H/'mixed_sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'mixed_sieve.py'),'73'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
