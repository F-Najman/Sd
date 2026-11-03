from pathlib import Path
import time
W=Path(__file__).resolve().parent
while not all((W/f'{name}_profiles_verified.json').exists()for name in['full_cusps61_sharp','full_cusps89','full_cusps97_sharp']):time.sleep(10)
# Reuse only the independent Sage relation-space checker, not producer code.
s=(W/'verify_profile_spaces.py').read_text().split('cases=')[0];exec(compile(s,str(W/'verify_profile_spaces.py'),'exec'))
for args in[('full_cusps61_sharp',21,0,0,1,4),('full_cusps89',21,0,0,1,5),('full_cusps97_sharp',21,0,0,1,5)]:check_case(*args)
(W/'profile_spaces_full_new_verified.json').write_text(json.dumps({'status':'PASS','degree':21,'results':out},indent=2)+'\n');print('S21_PROFILE_SPACES_FULL_NEW_COMPLETE',flush=True)
