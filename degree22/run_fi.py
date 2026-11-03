from pathlib import Path
import subprocess,concurrent.futures,json,time
W=Path(__file__).resolve().parent;H=W/'FI'
jobs=[(59, 29, '2', '3', 'fast'), (73, 12, '2,3,5', '3,5,7', 'combined'), (79, 39, '2', '3', 'fast'), (83, 41, '2', '3', 'fast'), (103, 17, '2', '3', 'fast'), (107, 53, '2', '3', 'alpha_fast'), (109, 54, '2', '3', 'alpha_fast'), (113, 56, '2', '3', 'alpha_fast'), (131, 13, '2', '3', 'alpha_fast'), (137, 68, '2', '3', 'alpha_fast'), (139, 69, '2', '3', 'alpha_fast')]
def one(j):
 n,i,t,q,method=j;stem=f'FI{n}_i8'if n==97 else f'FI{n}';p=H/(stem+'.txt');log=H/(stem+'_export.log');script=W/('export_combined_FI.m'if method=='combined'else f'export_FI_{method}.m')
 with log.open('w')as f:r=subprocess.run(['magma','-b',f'P:={n}',f'Ind:={i}',f'Tn:={t}',f'Q:={q}',f'Out:={p}',str(script)],stdout=f,stderr=subprocess.STDOUT)
 s=log.read_text();ok='DECIC_FI_EXPORT_COMPLETE'in s and not any(x in s for x in ['User error','Runtime error','Assertion failed']);
 if ok:subprocess.run(['python',str(W/'compress_FI.py'),str(p)],check=True)
 print('S22_FI_EXPORT',n,ok,flush=True);return {'N':n,'status':'PASS'if ok else'FAIL'}
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:rs=list(ex.map(one,jobs))
(W/'fi_exports.json').write_text(json.dumps(rs,indent=2)+'\n')
