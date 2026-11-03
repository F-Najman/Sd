from pathlib import Path
import psutil,math,time,json
W=Path(__file__).resolve().parent;needle=str(W);last=None
for p in psutil.process_iter():
 try:p.cpu_percent(None)
 except psutil.Error:pass
while not(W/'STOP_RESOURCE_WATCH').exists():
 time.sleep(30);own=[];external=0.0
 for p in psutil.process_iter(['pid','cmdline','name']):
  try:
   args=p.info['cmdline']or[];isown=any(a.startswith(needle)or a.startswith('work/degree21/')for a in args)
   if isown:own.append(p)
   else:external+=p.cpu_percent(None)/100
  except psutil.Error:pass
 limit=max(2,min(24,30-math.ceil(external)));cpus=list(range(limit))
 for p in own:
  try:p.cpu_affinity(cpus);p.nice(8)
  except psutil.Error:pass
 a={'status':'ACTIVE','external_cpu_estimate':external,'S21_affinity':cpus,'nice':8,'target_idle_logical_cpus':2,'processes':len(own)};(W/'resource_allocation.json').write_text(json.dumps(a,indent=2)+'\n')
 if last!=limit:print('S21_CPU_AFFINITY',limit,'external',round(external,1),'processes',len(own),flush=True);last=limit
