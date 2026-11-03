SetQuitOnError(true);SetColumns(0);
load "work/degree18/full131/hecke_jets_1.m";SM:=SourceMetadata;SR:=SourceRecords;SH:=SourceHeckeRecords;
load "work/degree18/full131/hecke_jets_9.m";SM:=SM cat SourceMetadata;SR:=SR cat SourceRecords;SH:=SH cat SourceHeckeRecords;
keep:=[k:k in[1..#SM]|SM[k][2]le 11];assert #keep eq 12;
PrintFile("work/degree18/full131/small_hecke_jets.m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",[*SM[k]:k in keep*],[*SR[k]:k in keep*],[*SH[k]:k in keep*]):Overwrite:=true);
print "S18_SMALL_HEKKE_EXPORT_COMPLETE";quit;
