from pathlib import Path
import subprocess,concurrent.futures
W=Path(__file__).resolve().parent;O=W.parent/'degree17'
ns=[47,53,59,61,67,71,73,79,83,89,113,127]
for n in ns:
 H=W/f'full{n}';out=H/'small_hecke_jets.m';s=f'''SetQuitOnError(true);SetColumns(0);SetMemoryLimit(16*10^9);
load "{O}/full{n}/hecke_jets.m";
load "{W}/inherited{n}.m";
oldToNew:=AssociativeArray();for v in InheritedOrbitMatches do oldToNew[v[2]]:=v[1];end for;
keep:=[k:k in[1..#SourceMetadata]|SourceMetadata[k][2]le 12];
M:=[*<oldToNew[SourceMetadata[k][1]],SourceMetadata[k][2],SourceMetadata[k][3],SourceMetadata[k][4]>:k in keep*];
R:=[*SourceRecords[k]:k in keep*];T:=[*SourceHeckeRecords[k]:k in keep*];
PrintFile("{out}",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",M,R,T):Overwrite:=true);
print "S18_SMALL_HEKKE_EXPORT_COMPLETE";quit;
''';(H/'export_small.m').write_text(s)
def one(n):
 H=W/f'full{n}'
 with(H/'export_small.log').open('w')as f:r=subprocess.run(['magma','-b',str(H/'export_small.m')],stdout=f,stderr=subprocess.STDOUT)
 ok='S18_SMALL_HEKKE_EXPORT_COMPLETE'in(H/'export_small.log').read_text();print(n,ok,flush=True);assert ok
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:list(ex.map(one,ns))
