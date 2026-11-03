"""Adapt the bundled source paths after extracting the certificate archive."""
from pathlib import Path
import sys
B=Path(__file__).resolve().parents[2]
old='/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a'
library='/home/fnajman/degree9_torsion/nonic-torsion'
for root in [B/'work/audit11']:
    for p in root.rglob('*'):
        if p.suffix not in ['.py','.m','.magma'] or p.name=='relocate.py':continue
        s=p.read_text();t=s.replace(old,str(B)).replace(library,str(B/'vendor/nonic'))
        if s!=t:p.write_text(t)
print('S11_CERTIFICATE_PATHS_RELOCATED',B)
