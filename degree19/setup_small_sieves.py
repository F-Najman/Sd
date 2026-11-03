from pathlib import Path
W=Path(__file__).resolve().parent;O=W.parent/'degree18'
for name in ['pair_sieve.py','mixed_sieve.py']:
 s=(O/name).read_text();a=s.index('def pmul(');b=s.index('def tensor(',a);pm=(W/'full_sieve.py').read_text();pa=pm.index('from sage.libs.ntl');pb=pm.index('def tensor(',pa);s=s[:a]+pm[pa:pb]+s[b:]
 if name=='pair_sieve.py':s=s.replace('in[7,8,9,10,11]','in[7,8,9,10,11,12]').replace('!=18','!=19')
 if name=='mixed_sieve.py':s=s.replace('(12 if N==73 else 11)','(13 if N==73 else 12)')
 (W/name).write_text(s)
