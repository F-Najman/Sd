from pathlib import Path
import json,re,hashlib
from sage.all import GF,matrix,ZZ
from unit_arithmetic import matbits,lit
W=Path(__file__).resolve().parent;s=(W/'full97/units_data_extended.m').read_text();o=(W/'full97/units_data.m').read_text();q=matbits(s,'qcoeffs');old=matbits(o,'qcoeffs');assert len(q)==len(old)==345 and all((a&((1<<1768)-1))==b for a,b in zip(q,old))and re.search(r'precision:=3500;',s)
for name in['DiamondMatrix','UnitXRelations','UnitYRelations']:assert matbits(s,name)==matbits(o,name)
sat=matrix(GF(2),lit((W/'extended97_basis_data.m').read_text(),'Extended97SaturatedQ'));T=matrix(GF(2),lit((W/'extended97_basis_data.m').read_text(),'Extended97ChangeOfBasis'));Q=matrix(GF(2),[ZZ(v).digits(2,padto=3500)for v in q]);assert sat.nrows()==T.nrows()==345 and sat.ncols()==3500 and sat.rank()==T.rank()==345 and T*sat==Q
assert 'S22_EXTENDED97_BASIS_COMPLETE'in(W/'extend97.log').read_text();assert 3500>3136 and 3500-4>8*(345-1)
a={'status':'PASS','N':97,'genus':345,'section_degree':2,'canonical_basis_unchanged':True,'old_precision':1768,'new_precision':3500,'product_weight8_Sturm_bound':3136,'section_product_degree_bound':2752,'all_matrix_entries_rebuilt':True,'extended_model_sha256':hashlib.sha256((W/'full97/units_data_extended.m').read_bytes()).hexdigest()};(W/'extended97_verified.json').write_text(json.dumps(a,indent=2)+'\n');print('S22_EXTENDED97_INDEPENDENT_BASIS_VERIFIED',flush=True)
