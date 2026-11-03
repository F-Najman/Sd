from pathlib import Path
W=Path(__file__).resolve().parent;s=(W/'full_sieve.py').read_text();s=s.replace('if N in[41,47,59,71]:alpha={0:1}','if N in[41,47,59,71]:alpha={0:1}\nassert N in[41,43,73];alpha={2:1,0:-1}if N==41 else({3:1,0:-1}if N==43 else{4:1,0:-1})')
s=s.replace('for md,so,targets in zip(meta,S,TS):\n si,d,orb,jpol=md;dd={}', 'for md,so,targets in zip(meta,S,TS):\n si,d,orb,jpol=md\n if d not in({8,9,10,11}if N==41 else({8,9}if N==43 else{7,9,10})):continue\n dd={}')
s=s.replace("H/'sieve.json'","H/'mixed_sieve.json'").replace("H/'matrices.json.gz'","H/'mixed_matrices.json.gz'");(W/'mixed_sieve.py').write_text(s)
