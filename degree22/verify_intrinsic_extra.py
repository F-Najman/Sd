from pathlib import Path
import json
from intrinsic_model import Model,compare,results
W=Path(__file__).resolve().parent
M=Model(71);compare(M,'full_cusps71',[M.hecke(q)-M.D**M.log(q)-(q%2)*M.I for q in[2,3,5,7]if M.hecke(q)is not None])
M=Model(127);compare(M,'full_cusps127',M.operators(M.root,[2,3,5,7]))
(W/'intrinsic_full_cusps_extra.json').write_text(json.dumps({'status':'PASS','results':results},indent=2)+'\n')
