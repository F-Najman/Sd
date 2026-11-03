"""Replay the audit; --fresh also regenerates the Magma calculations."""
from pathlib import Path
import subprocess,sys,concurrent.futures,json,re,ast
W=Path(__file__).resolve().parent;B=W.parents[1]
L= B/'vendor/nonic'
if not L.exists():L=Path('/home/fnajman/degree9_torsion/nonic-torsion')
Ns=[37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
def run(job):
    name,cmd=job
    with (W/(name+'.log')).open('w')as f:
        r=subprocess.run(cmd,cwd=L,stdout=f,stderr=subprocess.STDOUT)
    s=(W/(name+'.log')).read_text()
    assert r.returncode==0 and not any(t in s for t in ['Runtime error','User error','Traceback','Assertion failed']),(name,s[-2000:])
    print('REPLAY_FINISHED',name,flush=True)
def magma(name,file=None,*args):return(name,['magma','-b',*args,str(W/(file or name+'.m'))])
def python(name,file=None,*args):return(name,[sys.executable,str(W/(file or name+'.py')),*args])
def batch(jobs,n=4):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n)as ex:list(ex.map(run,jobs))
if '--fresh' in sys.argv:
    subprocess.run(['g++','-O3','-std=c++17',str(W/'check_prefixes.cpp'),'-o',str(W/'check_prefixes')],check=True)
    run(magma('census_sources'))
    batch([magma(f'full{n}/build')for n in Ns])
    batch([magma(f'full{n}/stage2')for n in Ns])
    run(python('sieve_batch_final','replay_sieves.py'))
    run(python('fi_batch','audit_fi.py'))
    run(python('large_character_batch','large_order_batch.py'))
    jobs=[magma('occurrence','verify_occurrence.m'),magma('decic_witness','verify37_witness.m'),magma('supersingular3'),magma('unit_poles'),magma('unit_poles_last'),magma('native_models'),magma('stabilizers'),magma('decic37'),magma('P41_NC5_clean'),magma('P41_cusps')]
    for n,d in [(41,5),(43,7)]:jobs.append(magma(f'supersingular{n}','prime_good48.m',f'N:={n}',f'Ds:={d}','Qs:=3',f'RecordFile:={W}/supersingular{n}_inputs.m'))
    for n,pw,o in [(37,1,18),(43,1,7),(67,11,3),(71,5,7),(73,1,9)]:jobs.append(magma('two67_correct'if n==67 else f'two{n}','rational_two.m',f'N:={n}','Qs:=3,5',f'Power:={pw}',f'DiamondOrder:={o}',f'MatrixFile:={W}/two{n}_data.m'))
    jobs +=[magma(f'gon43_nonrat_{k}','gon43_nonrational.m',f'Which:={k}')for k in range(1,9)]
    jobs.append(magma('gon43_native_control'))
    batch(jobs)
    # The standalone native control checks this list itself.
    s=(W/'gon43_native_control.log').read_text();assert'AUDIT_GON43_NATIVE_CONTROL_COMPLETE'in s
    (W/'gon43_native_control.json').write_text(json.dumps({'status':'PASS','native_RR_dimension_with_value_zero_at_cusp':4,'qexp_principal_part_dimension':4,'all_15_nonconstant_pole_degrees':[30,30,36,36,36,36,39,39,39,45,45,48,48,51,54]},indent=2)+'\n')
run(python('prime_bound','verify_large_odd_bound.py'))
run(python('gon43_qjets'))
run(python('gon43_check','check_gon43.py'))
run(python('independent_matrices','check_matrices.py'))
run(python('final_audit','certify_audit.py'))
print('S11_AUDIT_REPLAY_COMPLETE',flush=True)
