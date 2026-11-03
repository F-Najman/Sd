"""Losslessly pack the innermost binary coefficient lists of raw Magma records.
Input is the original exporter format: every field element is a bit list.
The operation is one regex pass, so newly formed outer integer lists are
never visited. No compact form is written back over the raw certificate.
"""
import re
_rx=re.compile(r'\[\s*[01](?:\s*,\s*[01])*\s*\]')
def compact(s):return _rx.sub(lambda m:str(int(''.join(re.findall('[01]',m[0]))[::-1],2)),s)
