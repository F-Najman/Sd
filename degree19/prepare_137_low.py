from pathlib import Path
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;H=W/'full137';s=(H/'hecke_jets_1.m').read_text();m=lit(s,'SourceMetadata');inds=[i for i,r in enumerate(m)if r[1]in[8,9]];assert len(inds)==4
vals={k:lit(s,k)for k in ['SourceMetadata','SourceRecords','SourceHeckeRecords']}
def mag(v):
 if isinstance(v,tuple):return '<'+','.join(map(mag,v))+'>'
 if isinstance(v,list):return '['+','.join(map(mag,v))+']'
 return str(v)
(H/'small_hecke_jets.m').write_text('\n'.join(k+':=[*'+','.join(mag(v[i])for i in inds)+'*];'for k,v in vals.items())+'\n')
s=(W.parent/'degree18/pair_low131.py').read_text().replace('not in[16,17]','not in[16,17,18,19]');(W/'pair_low137.py').write_text(s)
