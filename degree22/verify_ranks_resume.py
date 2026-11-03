"""Independent Sage ranks of every newly retained obstruction matrix."""
from pathlib import Path
import json,gzip,time,hashlib
from sage.all import matrix,GF,ZZ
W=Path(__file__).resolve().parent;F=GF(2);tt=time.monotonic();Ns=json.loads((W/'local_levels.json').read_text())['levels'];sets=json.loads((W/'small_jet_jobs.json').read_text())['degree_sets'];tasks=[(f'full{n}','')for n in Ns]+[('full163','')]+[(f'full{n}','pair_')for n in map(int,sets)]+[('full163','pair_')]+[(f'full{n}','mixed_')for n in[73,89,109,113,127]]+[('ss89',''),('ss5_89',''),('ss7_89','')];done={}
# Reuse completed independent Sage checks only after matching exact archive hashes.
oldlog=(W/'verify_ranks.log').read_text()
if(W/'independent_rank_progress.json').exists():
 for rec in json.loads((W/'independent_rank_progress.json').read_text()):
  key=(rec['folder'],''if rec['kind']=='ordinary'else rec['kind']);assert key in tasks and key not in done and rec['status']=='PASS'
  folder,kind=key;archive=W/folder/(kind+'matrices.json.gz');a=json.loads((W/folder/(kind+'sieve.json')).read_text())
  assert hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()==rec['matrix_archive_sha256']and a['nonprincipal']==rec['matrices']and a['dimension']==rec['rank']
  assert rec['matrix_archive_sha256']in oldlog
  done[key]=rec
print('S22_INDEPENDENT_RANK_CACHE_BYTE_VERIFIED',len(done),flush=True)
while len(done)<len(tasks):
 progress=False
 for folder,kind in tasks:
  if(folder,kind)in done:continue
  H=W/folder;log=H/('mixed_new_sieve.log'if kind=='mixed_'else kind+'sieve.log');p=H/(kind+'matrices.json.gz');jp=H/(kind+'sieve.json')
  if not(p.exists()and log.exists()and'AUDIT_FULL_SIEVE_COMPLETE'in log.read_text()):continue
  a=json.loads(jp.read_text());ms=json.load(gzip.open(p,'rt'));assert len(ms)==a['nonprincipal'];seen=set()
  for v in ms:
   key=json.dumps(v['source']);assert key not in seen;seen.add(key);rows=[ZZ(int(z,16))for z in v['rows']];assert len(rows)==a['dimension'];A=matrix(F,[z.digits(2,padto=v['columns'])for z in rows]);assert A.ncols()==v['columns']and A.rank()==a['dimension']==v['rank']
  rec={'folder':folder,'kind':kind or'ordinary','matrices':len(ms),'rank':a['dimension'],'status':'PASS','matrix_archive_sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()};done[folder,kind]=rec;progress=True;print('S22_RANK_INDEPENDENT_PASS',rec,'elapsed',round(time.monotonic()-tt,1),flush=True);(W/'independent_rank_progress.json').write_text(json.dumps(list(done.values()),indent=2)+'\n')
 if not progress:time.sleep(20)
out={'status':'PASS','results':sorted(done.values(),key=lambda z:(z['folder'],z['kind'])),'matrices':sum(v['matrices']for v in done.values())};(W/'independent_rank_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('S22_ALL_NEW_OBSTRUCTION_MATRICES_VERIFIED',out['matrices'],flush=True)
