from pathlib import Path
W=Path(__file__).resolve().parent;O=W.parent/'degree18'
for name in ['relative53.m','relative61.m','relative73.m','relative73_nc.m','relative127.m']:
 s=(O/name).read_text().replace('work/degree18/','work/degree19/').replace('S18_','S19_').replace('c:=18-ssdeg','c:=19-ssdeg')
 if name=='relative73_nc.m':s=s.replace('c:=9;','c:=10;')
 if name=='relative127.m':s=s.replace('0,2);','0,3);').replace('1,2,g,2','1,2,g,3')
 (W/name).write_text(s)
s=(O/'verify_relative_cusps_intrinsic.py').read_text().replace('1:19','1:20').replace('range(18)','range(19)').replace('18-ind','19-ind').replace('r==17','r==18').replace("'relative_rank':17","'relative_rank':18")
(W/'verify_relative_cusps_intrinsic.py').write_text(s)
# Compare actual finite point orbits, independent of random census representatives.
t=(O/'match_inherited.m').read_text().replace('work/degree17/','work/degree18/').replace('work/degree18/sources','work/degree19/sources').replace('work/degree18/inherited','work/degree19/inherited').replace('r[1]eq 18','r[1]eq 19').replace('S18_','S19_')
for n in [47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131]:
 s=t.replace('eval Read(Sprintf("work/degree18/sources%o.m",p));',f'load "work/degree18/sources{n}.m";').replace('eval Read(Sprintf("work/degree19/sources%o.m",p));',f'load "work/degree19/sources{n}.m";')
 (W/f'match{n}.m').write_text(s)
