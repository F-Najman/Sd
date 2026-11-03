"""Replay the full rank-zero Petri-lifting certificate (Sage's Python).

Usage: sage -python run_petri_certificate.py MODEL_KEY --prime 5
Quartic witnesses must already exist, but their search is not trusted:
the verifier checks the listed rational divisors and all assertions afresh.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(key, prime):
    directory = ROOT/'hilbert_jobs'/key
    model = json.loads((directory/'result.json').read_text())
    row = json.loads((directory/'curve.json').read_text())
    assert model['model_verified'] and model['id'] == row['id']
    assert row['level'] % prime != 0
    for filename,value in model['source_sha256'].items():
        assert digest(ROOT/filename) == value
    for filename,value in model['artifact_sha256'].items():
        assert digest(directory/filename) == value
    integral = directory/'integral_model'
    assert (integral/'quartic_witnesses.m').exists()
    subprocess.run([sys.executable,str(ROOT/'integral_relations.py'),str(directory)],check=True)
    checked(['magma','-b',str(ROOT/'verify_canonical_hilbert.m')],integral,
            'petri_geometry_Q.log','SUCCESS: canonical model identified by Hilbert polynomial')
    checked(['magma','-b',f'N:={row["level"]}',f'g:={row["genus"]}',
             'delta:='+','.join(map(str,row['delta'])),str(ROOT/'intermediate_central_value.m')],
            integral,'petri_rank.log','SUCCESS intermediate central-value test')
    assert 'central_zero=false' in (integral/'petri_rank.log').read_text()
    checked(['magma','-b',f'p:={prime}',str(ROOT/'verify_petri_lifting.m')],integral,
            'petri_lifting.log','SUCCESS complete Petri lifting checks')
    sources = ['run_petri_certificate.py','integral_relations.py','export_canonical.py',
               'verify_canonical_hilbert.m','intermediate_central_value.m',
               'verify_petri_lifting.m','PETRI_LIFTING_CERTIFICATE.md']
    artifacts = [directory/name for name in model['artifact_sha256']]
    artifacts += [directory/'result.json']
    artifacts += [integral/name for name in ['relations.json','canonical_input.m','saturation.json',
                  'quartic_witnesses.m','petri_geometry_Q.log','petri_rank.log','petri_lifting.log']]
    result = dict(id=row['id'],prime=prime,status='FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO',
                  source_sha256={name:digest(ROOT/name) for name in sources},
                  artifact_sha256={str(path.relative_to(ROOT)):digest(path) for path in artifacts})
    (integral/'petri_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SUCCESS complete Petri rank-zero finiteness certificate',row['id'],flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('--prime',type=int,required=True)
    args = parser.parse_args()
    run(args.key,args.prime)
