"""Lossless verified storage of completed native chunks; combined inputs stay raw."""
from pathlib import Path
import gzip,hashlib,json,time,shutil,fcntl
W=Path(__file__).resolve().parent;lock=(W/'archive_native.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);dstmeta=W/'native_chunk_archives.json';old=json.loads(dstmeta.read_text())if dstmeta.exists()else{};records={z['path']:z for z in old.get('records',[])};jobs=json.loads((W/'new_ordinary_jobs.json').read_text())+json.loads((W/'ordinary163_jobs.json').read_text());start=time.monotonic()
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(status):
 a={'status':status,'chunks':len(records),'required':len(jobs),'raw_bytes':sum(v['raw_bytes']for v in records.values()),'compressed_bytes':sum(v['compressed_bytes']for v in records.values()),'records':list(records.values())};t=dstmeta.with_suffix('.json.tmp');t.write_text(json.dumps(a,indent=2)+'\n');t.replace(dstmeta)
while len(records)<len(jobs):
 changed=0
 for j in jobs:
  n,st=j['N'],j['start']
  if n==163 and 'S22_ALL_163_ORDINARY_JETS_COMPLETE'not in(W/'run_ordinary163.log').read_text():continue
  H=W/f'full{n}';p=H/f'hecke_jets_{st}.m';key=str(p.relative_to(W));log=H/f'chunk_{st}.log'
  if key in records:continue
  if not log.exists():continue
  s=log.read_text()
  if'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'not in s:continue
  assert not any(z in s for z in['Runtime error','User error','Assertion failed']),str(log)
  dst=p.with_suffix('.m.gz');tmp=dst.with_suffix('.gz.tmp');rawhash=hashlib.sha256();rawlen=0
  if p.exists():
   with p.open('rb')as src,tmp.open('wb')as out:
    with gzip.GzipFile(filename='',mode='wb',fileobj=out,compresslevel=3,mtime=0)as gz:
     while b:=src.read(1024*1024):rawhash.update(b);rawlen+=len(b);gz.write(b)
   tmp.replace(dst)
  else:
   assert dst.exists(),str(p)
   with gzip.open(dst,'rb')as src:
    while b:=src.read(1024*1024):rawhash.update(b);rawlen+=len(b)
  verify=hashlib.sha256()
  with gzip.open(dst,'rb')as src:
   while b:=src.read(1024*1024):verify.update(b)
  assert verify.hexdigest()==rawhash.hexdigest()
  rec={'path':key,'archive':str(dst.relative_to(W)),'N':n,'start':st,'end':j['end'],'raw_sha256':rawhash.hexdigest(),'archive_sha256':sha(dst),'raw_bytes':rawlen,'compressed_bytes':dst.stat().st_size,'native_log_sha256':sha(log),'native_source_sha256':sha(H/'stage2_chunk.m'),'decompressed_bytes_independently_rehashed':True};records[key]=rec;write('ACTIVE')
  if p.exists():p.unlink()
  changed+=1
  if len(records)%100==0:print('S22_NATIVE_ARCHIVE_VERIFIED',len(records),'/',len(jobs),'seconds',round(time.monotonic()-start,1),flush=True)
 if changed:print('S22_NATIVE_ARCHIVE_SWEEP',len(records),changed,'seconds',round(time.monotonic()-start,1),flush=True)
 if len(records)<len(jobs):time.sleep(30)
write('PASS');print('S22_ALL_NATIVE_CHUNKS_ARCHIVED_AND_VERIFIED',len(records),flush=True)
