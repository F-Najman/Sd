from pathlib import Path
import json,textwrap
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs';a=json.load(open(W/'final_coverage.json'));assert a['status']=='PASS'
s=(W/'PROOF.txt').read_text();(O/'S14_proof.txt').write_text(s);(O/'S14_result.json').write_text(json.dumps({k:v for k,v in a.items()if k!='cases'}|{'status':'PROVED_WITH_COMPUTER_ASSISTANCE','proof':'S14_proof.txt'},indent=2)+'\n')
lines=[]
for l in s.splitlines():lines.extend(textwrap.wrap(l,width=90,replace_whitespace=False,drop_whitespace=False)or[''])
pages=[lines[i:i+59]for i in range(0,len(lines),59)];objs=[None,None,b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>'];pids=[]
def esc(t):return t.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
for k,page in enumerate(pages,1):
 c='BT /F1 8 Tf 48 808 Td (S\\(14\\) = Primes\\(43\\) | computer-assisted proof | 29 October 2026) Tj ET\nBT /F1 9 Tf 12 TL 48 783 Td\n'
 for l in page:c+=f'({esc(l)}) Tj T*\n'
 c+=f'ET\nBT /F1 8 Tf 276 35 Td ({k} / {len(pages)}) Tj ET\n';b=c.encode('ascii');ci=len(objs)+1;objs.append(b'<< /Length '+str(len(b)).encode()+b' >>\nstream\n'+b+b'endstream');pi=len(objs)+1;pids.append(pi);objs.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {ci} 0 R >>'.encode())
objs[0]=b'<< /Type /Catalog /Pages 2 0 R >>';objs[1]=f'<< /Type /Pages /Count {len(pids)} /Kids [ '.encode()+b' '.join(f'{i} 0 R'.encode()for i in pids)+b' ] >>';pdf=bytearray(b'%PDF-1.4\n');off=[0]
for i,obj in enumerate(objs,1):off.append(len(pdf));pdf+=f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n'
x=len(pdf);pdf+=f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode()
for v in off[1:]:pdf+=f'{v:010} 00000 n \n'.encode()
pdf+=f'trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n'.encode();(O/'S14_proof.pdf').write_bytes(pdf);print('S14_RESULT_FINALIZED',len(pages),'pages')
