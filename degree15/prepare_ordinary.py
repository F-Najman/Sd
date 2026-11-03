from pathlib import Path
W=Path(__file__).resolve().parent;O=W.parent/'degree13';template=(O/'full113/stage2.m').read_text();census=(W/'census_sources.m').read_text();xykey=census[census.index('function XYKey'):census.index('records:=')]
ns=[41,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
for n in ns:
 O=W.parent/("degree13"if n==41 else"degree14")
 s=template.replace(str(W.parent/"degree13"),str(W)).replace('full113',f'full{n}').replace('sources113',f'sources{n}')
 pos=s.index('load "'+str(W/f'sources{n}.m')+'";')
 s=s[:pos]+xykey+f'''load "{O}/full{n}/hecke_jets.m";
OldMetadata:=SourceMetadata;OldRecords:=SourceRecords;OldHecke:=SourceHeckeRecords;used:={{Integers()|}};
'''+s[pos:]
 needle=' E,P:=SimplifyPoint(E,P);sr,sd:=RecordPoint(E,P);'
 extra=''' if rec[1] le (N eq 41 select 13 else 14) then
  good:=[];
  for oi in[1..#OldRecords]do
   if OldMetadata[oi][2]ne rec[1]or OldMetadata[oi][3]ne rec[6]or OldMetadata[oi][4]ne rec[5]then continue;end if;
   os:=OldRecords[oi];OF:=ext<GF(2)|PF!os[1]>;oxy:=[OF!PF!v:v in os[5]];okey:=XYKey(oxy[1],oxy[2]);
   found:=false;for k in[1..N-1]do uv:=TateNormalForm_xy(E,k*P);if XYKey(uv[1],uv[2])eq okey then found:=true;break;end if;end for;
   if found then Append(~good,oi);end if;
  end for;assert #good eq 1;oi:=good[1];assert oi notin used;Include(~used,oi);
  Append(~SourceRecords,OldRecords[oi]);Append(~SourceHeckeRecords,OldHecke[oi]);Append(~SourceMetadata,<si,rec[1],rec[6],rec[5]>);
  printf "S15_OLD_ORBIT_REUSE_VERIFIED N=%o source=%o old_source=%o degree=%o\\n",N,si,OldMetadata[oi][1],rec[1];continue;
 end if;
'''
 assert needle in s;s=s.replace(needle,extra+needle)
 needle='PrintFile("'+str(W/f'full{n}/hecke_jets.m')
 s=s.replace(needle,'assert #used eq #OldRecords;\n'+needle)
 (W/f'full{n}/stage2.m').write_text(s)
s=(O/'run_ordinary.py').read_text();a=s.index('ns=');b=s.index('\ndef one',a);s=s[:a]+'ns='+repr(ns)+s[b:];s=s.replace('max_workers=5','max_workers=6');(W/'run_ordinary.py').write_text(s)

exec((W/"optimize_large_jets.py").read_text(),{"__file__":str(W/"optimize_large_jets.py")})
