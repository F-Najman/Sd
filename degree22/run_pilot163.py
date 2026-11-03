from pathlib import Path
import shutil,subprocess
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;H=W/'pilot163';H.mkdir(exist_ok=True);shutil.copy2(W/'full163/units_data.m',H/'units_data.m');parts=[]
for name in['SourceMetadata','SourceRecords','SourceHeckeRecords']:
 vals=[]
 for st in range(1,353,8):
  s=(W/f'full163/hecke_jets_{st}.m').read_text();v=s.split(name+':=',1)[1].split(';',1)[0].strip();assert v.startswith('[*')and v.endswith('*]');vals.append(v[2:-2].strip())
 parts.append(name+':=[*'+','.join(v for v in vals if v)+'*];')
text='\n'.join(parts)+'\n';assert len(lit(text,'SourceMetadata'))==352;(H/'hecke_jets.m').write_text(text)
s=(W/'full_sieve.py').read_text().replace("H=W/f'full{N}'","H=W/'pilot163'");(W/'pilot163_sieve.py').write_text(s)
with(H/'sieve.log').open('w')as f:r=subprocess.run(['sage',str(W/'pilot163_sieve.py'),'163'],stdout=f,stderr=subprocess.STDOUT)
print('S22_PILOT163_COMPUTATION_FINISHED',r.returncode,flush=True)
