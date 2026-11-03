from pathlib import Path
import textwrap,shutil
B=Path(__file__).resolve().parents[2];O=B/'outputs';s=(O/'S11_proof_audited.txt').read_text();s.encode('ascii');lines=[]
for line in s.splitlines():lines.extend(textwrap.wrap(line,width=90,replace_whitespace=False,drop_whitespace=False)or[''])
pages=[lines[i:i+59]for i in range(0,len(lines),59)];objs=[None,None,b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>'];pids=[]
def esc(s):return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
for k,page in enumerate(pages,1):
 content='BT /F1 8 Tf 48 808 Td (S\(11\) = Primes\(31\) | audited computer-assisted proof | 28 October 2026) Tj ET\n'
 content+='BT /F1 9 Tf 12 TL 48 783 Td\n'
 for line in page:content+=f'({esc(line)}) Tj T*\n'
 content+=f'ET\nBT /F1 8 Tf 276 35 Td ({k} / {len(pages)}) Tj ET\n';raw=content.encode('ascii');cid=len(objs)+1;objs.append(b'<< /Length '+str(len(raw)).encode()+b' >>\nstream\n'+raw+b'endstream');pid=len(objs)+1;pids.append(pid);objs.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {cid} 0 R >>'.encode())
objs[0]=b'<< /Type /Catalog /Pages 2 0 R >>';objs[1]=f'<< /Type /Pages /Count {len(pids)} /Kids [ '.encode()+b' '.join(f'{i} 0 R'.encode()for i in pids)+b' ] >>';pdf=bytearray(b'%PDF-1.4\n');offsets=[0]
for i,obj in enumerate(objs,1):offsets.append(len(pdf));pdf+=f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n'
x=len(pdf);pdf+=f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode()
for off in offsets[1:]:pdf+=f'{off:010} 00000 n \n'.encode()
pdf+=f'trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n'.encode();(O/'S11_proof_audited.pdf').write_bytes(pdf)
for ext in['pdf','txt']:shutil.copy2(O/f'S11_proof_audited.{ext}',O/f'S11_proof.{ext}')
shutil.copy2(B/'work/audit11/final_result.json',O/'S11_result.json')
print('S11_AUDITED_PROOF_RENDERED',len(pages),'pages',len(pdf),'bytes')
