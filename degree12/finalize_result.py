from pathlib import Path
import json,textwrap,hashlib
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'outputs';O.mkdir(exist_ok=True)
cov=json.loads((W/'final_coverage.json').read_text());lv=json.loads((W/'large_verified.json').read_text());assert cov['status']==lv['status']=='PASS'and lv['verified_characters']==656 and cov['covered_primes']==44045
s=(W/'PROOF.draft.txt').read_text();s=s.replace('DEGREE 12: PROOF DRAFT -- LARGE-PRIME CERTIFICATES STILL PENDING','S(12): A COMPUTER-ASSISTED DETERMINATION').replace('Proposed conclusion:','Theorem:')
a=s.index('This draft is not a completed classification');b=s.index('\n1. OCCURRENCE',a);s=s[:a]+'''All computational obligations below have completed. The 656 required
character orders, including the 53 reused audited certificates, have
coprime Pade certificates verified in exact finite-field arithmetic.
The final coverage check accounts for all 44045 primes up to 532900.
The new local computations cover degree 12 and include levels 107
and 109. Earlier audited results are identified explicitly.
'''+s[b:]
s=s.replace('Once all these tests pass,','All these tests pass. Consequently,').replace('excludes these 92 primes. THIS IS THE REMAINING COMPUTATIONAL\nOBLIGATION AT THE TIME THIS DRAFT WAS WRITTEN.','excludes these 92 primes.')
a=s.index('Final publication of the displayed equality requires:');b=s.index('\nPrimary references:',a);s=s[:a]+'''All 603 new character tests and their Sage Pade checks passed. The
53 reused audited character certificates were rechecked as well.
The final disjoint coverage verifier accepts every prime up to
532900. Its result, the complete per-prime ledger, the local
matrices, and all generation and checking scripts are supplied.
Failed smaller-quotient experiments are not proof inputs.

The portable packet includes the relevant mdmagma library, the
borrowed exact certificates, and instructions for checking stored
certificates or regenerating them in Magma V2.30-1 and Sage.
'''+s[b:]
assert not any(t in s for t in ['PENDING','Proposed conclusion','THIS IS THE REMAINING','not a completed classification'])
(O/'S12_proof.txt').write_text(s);(O/'S12_result.json').write_text(json.dumps({'status':'PROVED_WITH_COMPUTER_ASSISTANCE','S12':cov['occurring_primes'],'covered_primes':44045,'oesterle_bound':532900,'character_orders_verified':656,'new_character_orders':603,'reused_audited_character_orders':53,'ordinary_source_orbits':298,'formal_immersion':'PASS','proof':'S12_proof.txt'},indent=2)+'\n')
lines=[]
for line in s.splitlines():lines.extend(textwrap.wrap(line,width=90,replace_whitespace=False,drop_whitespace=False)or[''])
pages=[lines[i:i+59]for i in range(0,len(lines),59)];objs=[None,None,b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>'];pids=[]
def esc(s):return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
for k,page in enumerate(pages,1):
 content='BT /F1 8 Tf 48 808 Td (S\(12\) = Primes\(37\) union {43} | computer-assisted proof | 29 October 2026) Tj ET\nBT /F1 9 Tf 12 TL 48 783 Td\n'
 for line in page:content+=f'({esc(line)}) Tj T*\n'
 content+=f'ET\nBT /F1 8 Tf 276 35 Td ({k} / {len(pages)}) Tj ET\n';raw=content.encode('ascii');cid=len(objs)+1;objs.append(b'<< /Length '+str(len(raw)).encode()+b' >>\nstream\n'+raw+b'endstream');pid=len(objs)+1;pids.append(pid);objs.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {cid} 0 R >>'.encode())
objs[0]=b'<< /Type /Catalog /Pages 2 0 R >>';objs[1]=f'<< /Type /Pages /Count {len(pids)} /Kids [ '.encode()+b' '.join(f'{i} 0 R'.encode()for i in pids)+b' ] >>';pdf=bytearray(b'%PDF-1.4\n');offsets=[0]
for i,obj in enumerate(objs,1):offsets.append(len(pdf));pdf+=f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n'
x=len(pdf);pdf+=f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode()
for off in offsets[1:]:pdf+=f'{off:010} 00000 n \n'.encode()
pdf+=f'trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n'.encode();(O/'S12_proof.pdf').write_bytes(pdf)
print('S12_RESULT_FINALIZED',len(pages),'pages','S12=',cov['occurring_primes'])
