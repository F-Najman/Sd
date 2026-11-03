from pathlib import Path
W=Path(__file__).resolve().parent
p=W/'full137/stage2_chunk.m';s=p.read_text().replace('Min(8,152 div d)','Min(d le 12 select 8 else 3,152 div d)');p.write_text(s)
s=(W/'full73/stage2_chunk.m').read_text().replace('rec[1]ne 19','rec[1]ne 13').replace('N eq 101 select 4 else 3','8').replace('/hecke_jets_','/extra_jets_');(W/'full73/extra13.m').write_text(s)
H=W/'full163';H.mkdir(exist_ok=True);s=(W/'full137/build.m').read_text().replace('N:=137;g:=715;QPrec:=3500;TatePrec:=4100;','N:=163;g:=1027;QPrec:=5000;TatePrec:=5600;').replace('Md^68','Md^81').replace('/full137/','/full163/');(H/'build.m').write_text(s)
