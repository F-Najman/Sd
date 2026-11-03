from pathlib import Path
import hashlib,json,zipfile
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs'
names=['verify_bound.py','derickx_stoll_table2.txt','verify_witnesses.m','verify37_witness.m','prime_bound.json','prime_bound.log','occurrence.log','occurrence37.log','certify_audit10.py','final_result.json','final_audit.log','render_proof.py','package_update.py']
files={f'work/audit10/{n}':W/n for n in names}
for ext in['pdf','txt']:files[f'outputs/S10_proof_audited.{ext}']=O/f'S10_proof_audited.{ext}'
readme='''S(10) audit update, 28 October 2026.

Read outputs/S10_proof_audited.pdf. Its raw local certificates are in
S11_audited_certificates.zip, identified by the hash in dependency.json.
Extract both packets in the same root directory. Run the S(11) packet's
relocate.py if moving to a different computer, and adjust the library
path in the S(10) occurrence scripts for native regeneration.

  python work/audit10/certify_audit10.py

The updated writeup incorporates the approved independent-agent audit
clarifications. The original review and evidence are separately supplied
as S10_S11_independent_audit.pdf and S10_S11_independent_audit.zip.
No raw mathematical certificate was changed by the writeup revision.
'''
manifest={n:hashlib.sha256(p.read_bytes()).hexdigest()for n,p in files.items()}
dep={'archive':'S11_audited_certificates.zip','sha256':hashlib.sha256((O/'S11_audited_certificates.zip').read_bytes()).hexdigest()}
p=O/'S10_audit_update.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED)as z:
 z.writestr('README.txt',readme);z.writestr('SHA256.json',json.dumps(manifest,indent=2));z.writestr('dependency.json',json.dumps(dep,indent=2))
 for n,q in files.items():z.write(q,n)
with zipfile.ZipFile(p)as z:
 assert z.testzip()is None
 for n,h in manifest.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
print('S10_UPDATED_ARCHIVE_VERIFIED',p.stat().st_size,'bytes')
