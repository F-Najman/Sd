from pathlib import Path
import re,json,hashlib
W=Path(__file__).resolve().parent;O=W.parent/'degree19'
def pols(p):return{(int(a),int(b)):re.sub(r'\s+','',c)for a,b,c in re.findall(r'FiniteFIPolynomials\[<(\d+),(\d+)>\]:=(.*?);',p.read_text(),re.S)}
a,b=pols(W/'finite_FI_polynomials.m'),pols(O/'finite_FI_polynomials.m');keys=[(67,2),(67,3),(67,5),(73,2),(73,3),(73,5),(79,2),(83,2),(89,2),(97,5),(103,2)];assert all(a[k]==b[k]for k in keys)
(W/'finite_FI_inheritance_verified.json').write_text(json.dumps({'status':'PASS','parent':'../degree19/finite_FI_polynomials.m','active_polynomials':[{'p':p,'hecke_index':n,'identical_integral_polynomial':True}for p,n in keys],'unused_raw_cases':[53,101]},indent=2)+'\n');print('S20_FINITE_FI_INHERITANCE_PASS',len(keys),flush=True)
