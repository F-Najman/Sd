"""Fresh exact elliptic-factor inputs for the uniform density exclusions."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from run_genus5_batch import checked

ROOT = Path(__file__).resolve().parent


def run(n):
    directory = ROOT/'elliptic_input_replays'/f'N{n}'
    directory.mkdir(parents=True,exist_ok=True)
    script = 'small_density_elliptic.m' if n in [37,57] else 'elliptic_factors.m'
    checked(['magma','-b',f'N:={n}',str(ROOT/script)],directory,'calculation.log','SUCCESS')
    text = (directory/'calculation.log').read_text()
    if n in [37,57]:
        bound = 12 if n==37 else 8
        assert f'CERTIFIED minimum_positive_elliptic_degree={bound}' in text
        conclusion = dict(minimum_positive_elliptic_degree=bound)
    else:
        assert f'N={n} genus=' in text
        assert 'CERTIFIED: no positive-rank elliptic factors' in text
        conclusion = dict(no_positive_rank_elliptic_factors=True)
    sources = ['run_elliptic_input_audit.py',script,'run_genus5_batch.py',
               'ELLIPTIC_DEGREE_EXCLUSIONS.md','DEBARRE_FAHLAOUI_OBSTRUCTION.md']
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    certificate = dict(level=n,status='EXACT_ELLIPTIC_INPUT',conclusion=conclusion,
                       source_sha256={s:digest(ROOT/s) for s in sources},
                       artifact_sha256={'calculation.log':digest(directory/'calculation.log')})
    (directory/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('SUCCESS replayed elliptic input',n,flush=True)


if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(run,[37,57,73,109,125]))
