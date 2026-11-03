SetQuitOnError(true);SetColumns(0);SetMemoryLimit(16*10^9);
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree17/full47/hecke_jets.m";
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree18/inherited47.m";
oldToNew:=AssociativeArray();for v in InheritedOrbitMatches do oldToNew[v[2]]:=v[1];end for;
keep:=[k:k in[1..#SourceMetadata]|SourceMetadata[k][2]le 12];
M:=[*<oldToNew[SourceMetadata[k][1]],SourceMetadata[k][2],SourceMetadata[k][3],SourceMetadata[k][4]>:k in keep*];
R:=[*SourceRecords[k]:k in keep*];T:=[*SourceHeckeRecords[k]:k in keep*];
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree18/full47/small_hecke_jets.m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",M,R,T):Overwrite:=true);
print "S18_SMALL_HEKKE_EXPORT_COMPLETE";quit;
