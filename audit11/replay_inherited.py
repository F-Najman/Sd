from pathlib import Path
import concurrent.futures,subprocess,json,time
W=Path(__file__).resolve().parent;L=Path('/home/fnajman/degree9_torsion/nonic-torsion')
jobs={'67':L/'P67/certify_67_readonly.py','71':L/'P71/certify_71_readonly.py','73':L/'P73/certify_73_readonly.py','79':L/'P79_P89/certify_79_readonly.py','83':L/'P83/certify_83_readonly.py','89':L/'P79_P89/certify_89_readonly.py','37_two':L/'P37/replay_rational_two.py','71_two':L/'P71/replay_special7_two.py'}
def run(z):
 name,script=z;t=time.monotonic()
 with open(W/f'inherited_{name}.log','w')as f:r=subprocess.run(['python',str(script)],cwd=L,stdout=f,stderr=subprocess.STDOUT)
 out={'case':name,'exit':r.returncode,'elapsed':time.monotonic()-t};print('INHERITED_REPLAY',out,flush=True);return out
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rs=list(ex.map(run,jobs.items()))
 (W/'inherited_replay_results.json').write_text(json.dumps(rs,indent=2)+'\n')
