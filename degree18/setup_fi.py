from pathlib import Path
W=Path(__file__).resolve().parent;O=W.parent/'degree17';(W/'FI').mkdir(exist_ok=True)
for name in ['export_FI_fast.m','export_combined_FI.m','export_FI_alpha_fast.m']:
 s=(O/name).read_text().replace('d:=17','d:=18').replace(str(O),str(W)).replace('[103,107,109,113,127]','[103,107,109,113,127,131]');(W/name).write_text(s)
s=(O/'run_fi.py').read_text().replace("jobs=[(41, 20, '2,3,6', '3,5,7', 'combined'), (43, 21, '2', '3,5,7', 'combined'), ","jobs=[").replace("(113, 56, '2', '3', 'alpha_fast')]","(113, 56, '2', '3', 'alpha_fast'), (127,21,'2','3','alpha_fast'), (131,13,'2','3','alpha_fast')]").replace('S17_','S18_')
(W/'run_fi.py').write_text(s)
s=(O/'check_fi.py').read_text().replace('d==17','d==18').replace('d+8*','d+9*').replace('range(7,11)','range(7,12)').replace('min(first,8)','min(first,9)').replace('r!=17','r!=18').replace("else[41,43,47","else[47").replace(',109,113]',',109,113,127,131]')
(W/'check_fi.py').write_text(s)
for p in [53,61,73,127]:
 s=(O/f'relative{p}.m').read_text().replace('work/degree17','work/degree18').replace('c:=17-ssdeg','c:=18-ssdeg').replace('S17_','S18_');(W/f'relative{p}.m').write_text(s)
s=(O/'check_relative.py').read_text().replace('c=17-d','c=18-d').replace('width==17','width==18').replace('rr!=17-r','rr!=18-r').replace("'expected_rank':17-r","'expected_rank':18-r");(W/'check_relative.py').write_text(s)
