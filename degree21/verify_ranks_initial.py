"""Independent Sage ranks of every newly retained obstruction matrix."""
from pathlib import Path
import json,gzip,time,hashlib
from sage.all import matrix,GF,ZZ
W=Path(__file__).resolve().parent;F=GF(2);tt=time.monotonic();Ns=json.loads((W/'local_levels.json').read_text())['levels'];sets=json.loads((W/'small_jet_jobs.json').read_text())['degree_sets'];tasks=[(f'full{n}','')for n in Ns]+[(f'full{n}','pair_')for n in map(int,sets)]+[(f'full{n}','mixed_')for n in[73,89,109,113,127]]+[(f'ss{n}','')for n in[73,109,113,127]]+[('ss5_127',''),('ss7_127',''),('ss127','mixed_nc_')];done={}
while len(done)<len(tasks):
 progress=False
 for folder,kind in tasks:
  if(folder,kind)in done:continue
  H=W/folder;log=H/(kind+'sieve.log');p=H/(kind+'matrices.json.gz');jp=H/(kind+'sieve.json')
  if not(p.exists()and log.exists()and'AUDIT_FULL_SIEVE_COMPLETE'in log.read_text()):continue
  a=json.loads(jp.read_text());ms=json.load(gzip.open(p,'rt'));assert len(ms)==a['nonprincipal'];seen=set()
  for v in ms:
   key=json.dumps(v['source']);assert key not in seen;seen.add(key);rows=[ZZ(int(z,16))for z in v['rows']];assert len(rows)==a['dimension'];A=matrix(F,[z.digits(2,padto=v['columns'])for z in rows]);assert A.ncols()==v['columns']and A.rank()==a['dimension']==v['rank']
  rec={'folder':folder,'kind':kind or'ordinary','matrices':len(ms),'rank':a['dimension'],'status':'PASS','matrix_archive_sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()};done[folder,kind]=rec;progress=True;print('S21_RANK_INDEPENDENT_PASS',rec,'elapsed',round(time.monotonic()-tt,1),flush=True);(W/'independent_rank_progress.json').write_text(json.dumps(list(done.values()),indent=2)+'\n')
 if not progress:time.sleep(20)
out={'status':'PASS','results':sorted(done.values(),key=lambda z:(z['folder'],z['kind'])),'matrices':sum(v['matrices']for v in done.values())};(W/'independent_rank_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('S21_ALL_NEW_OBSTRUCTION_MATRICES_VERIFIED',out['matrices'],flush=True)
