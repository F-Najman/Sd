from pathlib import Path
import json
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;O=W.parent/'degree18'
# Match old representatives before reusing their Hecke jets in new combinations.
for n in [47,53,59,61,67,71,73,83,89,113,127,131]:
 H=W/f'full{n}';old=(O/f'full{n}/small_hecke_jets.m').read_text();meta=lit(old,'SourceMetadata');src=lit(old,'SourceRecords');trg=lit(old,'SourceHeckeRecords');mp=lit((W/f'inherited{n}.m').read_text(),'InheritedOrbitMatches');idx={r[1]:r[0]for r in mp};keep=[i for i,m in enumerate(meta)if m[1]<=13];values={'SourceMetadata':[(idx[meta[i][0]],)+meta[i][1:]for i in keep],'SourceRecords':[src[i]for i in keep],'SourceHeckeRecords':[trg[i]for i in keep]}
 # Python tuples/list syntax converts directly into the Magma data-only format.
 def mag(v):
  if isinstance(v,tuple):return '<'+','.join(map(mag,v))+'>'
  if isinstance(v,list):return '[*'+','.join(map(mag,v))+'*]'
  return str(v)
 (H/'small_hecke_jets.m').write_text('\n'.join(k+':='+mag(v)+';'for k,v in values.items())+'\n')
 print('S19_SMALL_JETS_INHERITED',n,len(keep),flush=True)
